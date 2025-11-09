# CertifyPro

A lightweight system to track tax-professional certifications (CPA, EA, etc.), renewal dates, and documents. Built with **FastAPI + SQLite** (backend) and **React + TypeScript + CSS** (frontend).

## Features (MVP)
- User management: create/view users (name, email, role, department)
- Certification CRUD: type, number, issue/expiry dates, state
- Auto status:
  - **Active**: > 30 days before expiry
  - **Expiring Soon**: ≤ 30 days
  - **Expired**: past expiry
- Dashboard stats (total/active/expiring/expired)
- Search & filter (name, type, status) *(endpoint provided; UI optional)*
- Document upload (PDF/image) linked to a certification

## Tech Stack
- **Backend:** FastAPI, SQLAlchemy, Pydantic v2, SQLite
- **Frontend:** React, TypeScript, Axios (no UI framework), plain CSS
