🏥 MediTrackPros

Open-Source Hospital Workflow & Asset Management Platform

MediTrackPros is a cloud-ready, multi-tenant healthcare management system designed to help hospitals efficiently manage medical devices, inventory, compliance, patients, and operational workflows from a single unified platform.

This project is built with real hospital workflows in mind and is intended to be used, extended, and customized by hospitals, healthcare startups, and developers.

✨ Why MediTrackPros?

Hospitals often rely on:

Disconnected spreadsheets

Manual device logs

Fragmented inventory systems

Paper-based compliance tracking

MediTrackPros solves this by providing a centralized, role-based system that improves:

Operational visibility

Device safety & compliance

Maintenance planning

Inventory efficiency

🧩 Core Modules Overview
🏥 Hospital & Multi-Tenant Management

Supports multiple hospitals in a single deployment

Strict data isolation between hospitals

Subscription & plan management per hospital

Role-based access control (Admin, Engineer, Doctor, Staff)

🧑‍⚕️ Patient Management

Patient profiles with demographics

Medical history, vitals, medications

Appointments & emergency contacts

Doctor assignment & visit tracking

🛠 Medical Device Lifecycle Management

Complete device registry per hospital

QR-code based device identification

Track:

Installation

Warranty

Calibration schedules

Maintenance history

Incident reporting & service logs

NFC / QR scan support for mobile workflows

📦 Inventory & Procurement

Categorized inventory system

Stock level tracking & reorder alerts

Suppliers & purchase orders

Expiry tracking & storage location management

📋 Compliance & Audits

Compliance standards (NABH, AERB, etc.)

Audit scheduling & history

Compliance document uploads

Exportable compliance reports (CSV)

🧠 AI-Assisted Diagnostics (Experimental)

Medical image analysis using Google Gemini AI

Currently supports:

Pneumonia detection (X-ray)

Brain tumor detection (MRI)

Designed as decision-support, not diagnosis

⚠️ Disclaimer: AI results are assistive only and must be reviewed by qualified medical professionals.

📊 Operational Dashboard

Inventory health metrics

Device maintenance status

Calibration alerts

Supplier activity

Monthly trends & charts

🧱 Tech Stack
Frontend

React + TypeScript

Tailwind CSS

Shadcn/UI

Capacitor (mobile support)

Backend

Django & Django REST Framework

JWT Authentication

Role-based permissions

Modular app architecture

Database

PostgreSQL (production)

SQLite (local testing)

AI

Google Gemini AI (image analysis)

DevOps

Docker & Docker Compose

Nginx

Gunicorn

🗂 Project Structure
backend/
├── hospitals/
├── employees/
├── patient/
├── device/
├── inventory/
├── suppliers/
├── tickets/
├── compliance/
├── dashboard/
├── ml_test/
├── backend/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── Dockerfile
├── requirements.txt
└── seed.py


Each module is self-contained with:

models

serializers

views

URLs

🚀 Getting Started (Local Setup)
1️⃣ Prerequisites

Docker & Docker Compose

Python 3.10+

PostgreSQL (if running without Docker)

2️⃣ Clone the Repository
git clone https://github.com/Yogesh-MG/Meditrackpro.git
cd Meditrackpro

3️⃣ Environment Variables

Create a .env file:

DJANGO_SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=meditrack
DB_USER=postgres
DB_PASSWORD=postgres
TIME_ZONE=Asia/Kolkata

GEMINI_API_KEY=your_gemini_api_key

4️⃣ Run with Docker
docker-compose up --build


Backend will be available at:

http://localhost:8000

5️⃣ Seed Demo Data (Optional but Recommended)
docker-compose exec backend python manage.py seed


This creates:

Multiple hospitals

Employees (doctors, engineers, staff)

Devices with service logs

Inventory, suppliers, patients, compliance data

🔐 Authentication

JWT-based authentication

Token endpoints:

/api/token/

/api/token/refresh/

All APIs are protected by default.

🧪 Testing Status

Basic API testing structure in place

Extensive test coverage is a planned contribution area

🧭 Roadmap

Planned improvements:

Role-based dashboards

Real-time notifications

Audit trail logging

Advanced analytics

HL7 / FHIR integration

Offline-first mobile mode

🤝 Contributing

We welcome contributions from:

Developers

Healthcare IT teams

Biomedical engineers

How to contribute:

Fork the repo

Create a feature branch

Follow existing code patterns

Submit a pull request with clear description

⚠️ Medical & Legal Disclaimer

MediTrackPros does not replace certified hospital systems and does not provide medical diagnosis.

AI features are assistive tools only

Hospitals are responsible for compliance, validation, and regulatory approval

Use in production environments at your own discretion

📄 License

This project is released under the MIT License.
You are free to use, modify, and distribute it with attribution.

📬 Contact & Maintainer

Maintainer: Yogesh M
GitHub: https://github.com/Yogesh-MG

If you’re a hospital, startup, or researcher interested in deploying or extending this system, feel free to reach out.
