from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from datetime import date
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    role = Column(String, nullable=False)
    department = Column(String, nullable=True)

    certifications = relationship("Certification", back_populates="owner")


class Certification(Base):
    __tablename__ = "certifications"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, nullable=False)          # CPA, EA, etc.
    number = Column(String, nullable=False)
    issue_date = Column(Date, nullable=False)
    expiry_date = Column(Date, nullable=False)
    state = Column(String, nullable=False)
    document_path = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="certifications")

    @property
    def status(self) -> str:
        today = date.today()
        if isinstance(self.expiry_date, date):  # ensure it's a Python date
            if self.expiry_date < today:
                return "Expired"
            elif (self.expiry_date - today).days <= 30:
                return "Expiring Soon"
            else:
                return "Active"
        return "Unknown"