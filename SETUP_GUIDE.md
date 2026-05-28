# AI-Powered ERP System - Setup Guide

## Prerequisites

Before starting, install:

- ✅ **Python 3.12+**
- ✅ **PostgreSQL 13+**
- ✅ **Git**
- ✅ **VS Code** (optional)

---

## Step 1: Clone Repository

```bash
git clone https://github.com/israanecib/ai-erp-system.git
cd ai-erp-system
```

---

## Step 2: Create Virtual Environment

### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS
```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Step 4: Setup PostgreSQL Database

```sql
CREATE DATABASE erp_db;
CREATE USER erp_admin WITH PASSWORD 'your_secure_password';
ALTER ROLE erp_admin SET client_encoding TO 'utf8';
ALTER ROLE erp_admin SET default_transaction_isolation TO 'read committed';
GRANT ALL PRIVILEGES ON DATABASE erp_db TO erp_admin;
```

---

## Step 5: Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with your PostgreSQL credentials:
```env
DATABASE_URL=postgresql://erp_admin:your_password@localhost:5432/erp_db
SECRET_KEY=your-super-secret-key
```

---

## Step 6: Run Server

```bash
uvicorn app.main:app --reload
```

Access:
- **API Docs**: http://localhost:8000/api/docs
- **Health Check**: http://localhost:8000/health

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'app'"

Ensure you're in the project root with virtual environment activated:
```bash
cd ai-erp-system
source venv/bin/activate
```

### "FATAL: database 'erp_db' does not exist"

Create the database as shown in Step 4.

---

## Next Steps

Start with Phase 1, Week 1: Authentication System

See [DEVELOPMENT_ROADMAP.md](DEVELOPMENT_ROADMAP.md) for details.