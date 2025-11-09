from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
import os
from database import Base, engine, get_db
import models
import schemas

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="CertifyPro API", description="Certification Tracking System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ---------- ROOT ----------
@app.get("/")
def root():
    return {"message": "Welcome to CertifyPro API"}

@app.get("/health")
def health_check():
    return {"status": "ok"}


# ---------- USER MANAGEMENT ----------
@app.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/users/", response_model=List[schemas.UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# ---------- CERTIFICATION CRUD ----------
@app.post("/certifications/", response_model=schemas.CertificationResponse)
def create_certification(cert: schemas.CertificationCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == cert.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    new_cert = models.Certification(**cert.dict())
    db.add(new_cert)
    db.commit()
    db.refresh(new_cert)
    return new_cert

@app.get("/certifications/", response_model=List[schemas.CertificationResponse])
def get_all_certifications(db: Session = Depends(get_db)):
    return db.query(models.Certification).all()

@app.get("/certifications/{cert_id}", response_model=schemas.CertificationResponse)
def get_certification(cert_id: int, db: Session = Depends(get_db)):
    cert = db.query(models.Certification).filter(models.Certification.id == cert_id).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Certification not found")
    return cert

@app.put("/certifications/{cert_id}", response_model=schemas.CertificationResponse)
def update_certification(cert_id: int, cert_update: schemas.CertificationUpdate, db: Session = Depends(get_db)):
    cert = db.query(models.Certification).filter(models.Certification.id == cert_id).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Certification not found")
    for key, value in cert_update.dict(exclude_unset=True).items():
        setattr(cert, key, value)
    db.commit()
    db.refresh(cert)
    return cert

@app.delete("/certifications/{cert_id}")
def delete_certification(cert_id: int, db: Session = Depends(get_db)):
    cert = db.query(models.Certification).filter(models.Certification.id == cert_id).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Certification not found")
    db.delete(cert)
    db.commit()
    return {"message": "Certification deleted successfully"}


# ---------- DASHBOARD STATS ----------
@app.get("/certifications/stats", response_model=None)
def get_dashboard_stats(db: Session = Depends(get_db)):
    days_diff = func.julianday(models.Certification.expiry_date) - func.julianday(func.date('now'))
    total = db.query(models.Certification).count()
    expired = db.query(models.Certification).filter(models.Certification.expiry_date < func.date('now')).count()
    expiring = db.query(models.Certification).filter(days_diff.between(0, 30)).count()
    active = db.query(models.Certification).filter(days_diff > 30).count()

    return {
        "total": total,
        "active": active,
        "expiring_soon": expiring,
        "expired": expired
    }

# ---------- SEARCH & FILTER ----------
@app.get("/certifications/search", response_model=List[schemas.CertificationResponse])
def search_certifications(
    name: str | None = None,
    type: str | None = None,
    state: str | None = None,
    status: str | None = None,
    db: Session = Depends(get_db)
):
    q = db.query(models.Certification).join(models.User)
    if name:
        q = q.filter(models.User.name.ilike(f"%{name}%"))
    if type:
        q = q.filter(models.Certification.type.ilike(f"%{type}%"))
    if state:
        q = q.filter(models.Certification.state.ilike(f"%{state}%"))

    if status:
        s = status.lower()
        days_left = func.julianday(models.Certification.expiry_date) - func.julianday(func.date('now'))
        if s == "expired":
            q = q.filter(models.Certification.expiry_date < func.date('now'))
        elif s == "expiring soon":
            q = q.filter(days_left.between(0, 30))
        elif s == "active":
            q = q.filter(days_left > 30)
    return q.all()


# ---------- DOCUMENT UPLOAD ----------
@app.post("/certifications/{cert_id}/upload")
def upload_certificate(cert_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    cert = db.query(models.Certification).filter(models.Certification.id == cert_id).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Certification not found")

    filename = f"cert_{cert_id}_{file.filename}"
    filepath = os.path.join(UPLOAD_DIR, filename)
    with open(filepath, "wb") as f:
        f.write(file.file.read())

    cert.document_path = filepath # type: ignore
    db.commit()
    db.refresh(cert)
    return {"message": "File uploaded successfully", "path": filepath}