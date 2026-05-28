# AI-Powered ERP & Accounting Management System

An intelligent web application for small businesses to manage products, inventory, sales, purchases, expenses, and accounting operations with AI-powered assistance.

## 🎯 Project Overview

This is a mini ERP (Enterprise Resource Planning) system combined with accounting management features and an AI assistant. Perfect for small businesses that need integrated inventory, sales, and financial tracking.

### ✨ Key Features
- **Authentication System** (Admin, Accountant, Employee roles)
- **Product Management** (add, edit, delete, track stock)
- **Sales System** (invoices, automatic stock reduction)
- **Purchase Management** (supplier tracking, incoming stock)
- **Accounting System** (revenue, expenses, profits, taxes)
- **Dashboard** (sales charts, profit analysis, low stock alerts)
- **AI Assistant** (financial queries, predictions, expense classification)

## 🛠️ Technology Stack

### Backend
- **Python 3.12+**
- **FastAPI** - Modern async web framework
- **SQLAlchemy** - ORM
- **PostgreSQL** - Database

### Frontend
- **HTML5, CSS3, JavaScript**
- **Bootstrap** - Responsive design
- **Chart.js** - Data visualization

### AI & Data
- **pandas** - Data analysis
- **scikit-learn** - Machine learning
- **OpenAI API** - AI assistant

## 📁 Project Structure

```
ai-erp-system/
├── app/
│   ├── models/
│   ├── routes/
│   ├── services/
│   ├── schemas/
│   ├── auth/
│   └── ai/
├── database_schema/
├── frontend/
├── requirements.txt
└── README.md
```

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/israanecib/ai-erp-system.git
cd ai-erp-system
```

### 2. Setup Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Database
```bash
CREATE DATABASE erp_db;
CREATE USER erp_admin WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE erp_db TO erp_admin;
```

### 5. Configure Environment
```bash
cp .env.example .env
# Edit .env with your credentials
```

### 6. Run Server
```bash
uvicorn app.main:app --reload
```

Access: http://localhost:8000/api/docs

## 📊 Database Schema

Core tables:
- **users** - User accounts with roles
- **products** - Product inventory
- **customers** - Customer information
- **suppliers** - Supplier information
- **sales** - Sales transactions
- **purchases** - Purchase orders
- **expenses** - Business expenses
- **invoices** - Generated invoices

See [ER Diagram](database_schema/er_diagram.md) for relationships.

## 📅 Development Phases

### Phase 1: Foundation (Weeks 1-3)
- Week 1: Authentication system ⏳
- Week 2: Product management
- Week 3: Inventory system

### Phase 2: Business Logic (Weeks 4-6)
- Week 4: Sales system
- Week 5: Purchase system
- Week 6: Accounting module

### Phase 3: Analytics & AI (Weeks 7-8)
- Week 7: Dashboard with charts
- Week 8: AI assistant integration

See [Development Roadmap](DEVELOPMENT_ROADMAP.md) for details.

## 📚 Guides

- **Setup**: [SETUP_GUIDE.md](SETUP_GUIDE.md)
- **Roadmap**: [DEVELOPMENT_ROADMAP.md](DEVELOPMENT_ROADMAP.md)
- **Database**: [ER Diagram](database_schema/er_diagram.md)

## 🔐 Security

- JWT-based authentication
- Role-based access control
- Password hashing with bcrypt
- CORS middleware

## 🤝 Contributing

1. Create feature branch
2. Commit changes
3. Push to branch
4. Open Pull Request

## 📄 License

MIT License

## 👤 Author

**israanecib**

---

**Status**: 🚀 In Development - Phase 1 (Week 1)

**Next**: Complete authentication system