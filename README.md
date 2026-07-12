# API Marketplace Developer Platform

A full-stack API Marketplace platform built with **FastAPI**, **PostgreSQL**, and **React** that allows developers to publish APIs, consumers to subscribe and use APIs securely, and administrators to manage the entire platform.

---

## Features

### Authentication

- JWT Authentication
- Google OAuth Login
- Email Verification
- Password Hashing
- Role-Based Access Control

---

### User Management

- Register/Login
- Update Profile
- Delete Account
- View Users
- Developer Role
- Consumer Role
- Admin Role

---

### API Marketplace

- Publish APIs
- Update APIs
- Delete APIs
- Browse APIs
- Search APIs
- Filter APIs
- API Categories
- Pricing Support

---

### API Keys

- Generate API Keys
- Regenerate API Keys
- Revoke API Keys

---

### API Usage

- Track API Requests
- Developer Usage Analytics
- Consumer Usage Analytics

---

### Reviews

- Add Reviews
- Edit Reviews
- Delete Reviews
- Average Ratings

---

### API Discovery

- Top Rated APIs
- Recently Added APIs

---

### Dashboards

Developer Dashboard

- Total APIs
- Subscribers
- API Requests

Consumer Dashboard

- Active Subscriptions
- API Requests
- Recent Activity

Admin Dashboard

- Users
- APIs
- Requests
- Subscriptions

---

### Admin Panel

- View Users
- Change User Roles
- Enable Users
- Disable Users
- Delete Reviews
- Platform Analytics

---

## Tech Stack

### Backend

- FastAPI
- SQLAlchemy
- PostgreSQL
- JWT Authentication
- OAuth
- Pydantic

### Frontend

- React
- Vite
- Axios

### Database

- PostgreSQL

---

## Project Structure

```
backend/
│
├── database/
├── routers/
├── schemas/
├── services/
├── utils/
├── main.py
├── config.py
├── requirements.txt
└── .env

frontend/

README.md
```

---

## Installation

Clone the repository

```bash
git clone <repository-url>
```

Move into project

```bash
cd api-marketplace-developer
```

Backend

```bash
cd backend
```

Create virtual environment

```bash
python -m venv venv
```

Activate

Linux

```bash
source venv/bin/activate
```

Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run server

```bash
uvicorn main:app --reload
```

---

## Environment Variables

Create a `.env` file inside `backend/`

```env
DATABASE_URL=
SECRET_KEY=
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

EMAIL_ADDRESS=
EMAIL_PASSWORD=

GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
```

---

## API Documentation

Swagger UI

```
http://127.0.0.1:8000/docs
```

ReDoc

```
http://127.0.0.1:8000/redoc
```

---

## Future Improvements

- Stripe Payment Integration
- API Subscription Billing
- API Rate Limiting
- Docker Support
- Kubernetes Deployment
- CI/CD Pipeline
- Redis Caching
- Webhooks
- Notifications

---

## License

MIT License

---

## Author

Suraj M