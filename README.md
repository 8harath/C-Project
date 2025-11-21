# Pharmaceutical Warehouse & Inventory Management System

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)](https://flask.palletsprojects.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3.0-purple.svg)](https://getbootstrap.com/)
[![License](https://img.shields.io/badge/License-Academic-orange.svg)](LICENSE)

A comprehensive pharmaceutical inventory management solution developed as an academic capstone project. This production-ready web application streamlines medicine tracking, sales management, and provides powerful analytics for modern pharmaceutical operations.

![Project Banner](https://img.shields.io/badge/Project-Capstone-success)

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
- [Default Login Credentials](#default-login-credentials)
- [Project Structure](#project-structure)
- [Usage Guide](#usage-guide)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [Team](#team)
- [License](#license)

---

## Features

### Core Functionality
- **Role-Based Access Control** - Secure authentication with Admin and Staff roles
- **Medicine Management** - Complete CRUD operations for pharmaceutical inventory
- **Barcode Integration** - Fast medicine identification and scanning
- **Sales Tracking** - Comprehensive sales recording and history
- **Smart Alerts** - Low stock notifications and expiry warnings
- **Analytics Dashboard** - Sales trends, forecasting, and insights
- **Export Capabilities** - Download reports in CSV format
- **Alternative Medicines** - Suggest alternatives for out-of-stock items
- **Responsive Design** - Works seamlessly on desktop, tablet, and mobile

### Advanced Features
- Seasonal demand forecasting
- Predictive analytics for inventory optimization
- Real-time stock level monitoring
- Expiry date tracking with automated alerts
- Detailed sales reports with visualizations

---

## Tech Stack

### Backend
- **Python 3.8+** - Core programming language
- **Flask 2.3.3** - Web framework
- **SQLAlchemy** - ORM for database operations
- **SQLite** - Lightweight database
- **Flask-Login** - User session management
- **WTForms** - Form validation and rendering

### Frontend
- **Bootstrap 5.3.0** - UI framework
- **Chart.js 4.4.0** - Data visualization
- **Bootstrap Icons** - Icon library
- **JavaScript (ES6+)** - Interactive features
- **Jinja2** - Template engine

---

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Python 3.8 or higher** - [Download Python](https://www.python.org/downloads/)
- **pip** - Python package installer (usually comes with Python)
- **Git** - For cloning the repository (optional)

### Check Your Python Installation

```bash
python --version
# or
python3 --version
```

Expected output: `Python 3.8.x` or higher

### Check pip Installation

```bash
pip --version
# or
pip3 --version
```

---

## Installation

### Step 1: Clone or Download the Repository

**Option A: Using Git**
```bash
git clone https://github.com/8harath/C-Project.git
cd C-Project
```

**Option B: Manual Download**
1. Download the ZIP file from the repository
2. Extract it to your desired location
3. Open terminal/command prompt in the extracted folder

### Step 2: Create a Virtual Environment (Recommended)

Creating a virtual environment isolates project dependencies from your system Python installation.

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt indicating the virtual environment is active.

### Step 3: Install Dependencies

With the virtual environment activated, install all required packages:

```bash
pip install -r requirements.txt
```

This will install:
- Flask and Flask extensions
- SQLAlchemy for database operations
- WTForms for form handling
- Other necessary dependencies

**If you encounter any errors**, try upgrading pip first:
```bash
pip install --upgrade pip
```

---

## Database Setup

### Step 1: Initialize and Seed the Database

The project includes a seeding script that creates the database and populates it with sample data:

```bash
python seed_database.py
```

**What this script does:**
- Creates all necessary database tables
- Adds default admin and staff users
- Populates the database with **100+ sample medicines** across 9 categories:
  - Allergy (11 medicines)
  - Cold and Mild Flu (11 medicines)
  - Cough (11 medicines)
  - Dermatology (11 medicines)
  - Eye/ENT (11 medicines)
  - Fever (11 medicines)
  - Pain Relief (12 medicines)
  - Vitamins (11 medicines)
  - Women Hygiene (11 medicines)
- Creates alternative medicine mappings

**Expected Output:**
```
============================================================
  Warehouse Inventory Management System - Database Seeding
============================================================

Creating users...
✓ Created admin and staff users

Creating medicines...
✓ Created 100+ medicines

Creating alternative medicine mappings...
✓ Created alternative medicine mappings

============================================================
  Database Seeding Complete!
============================================================

Default Login Credentials:
------------------------------------------------------------
  Admin:
    Username: admin
    Password: admin123

  Staff:
    Username: staff
    Password: staff123
------------------------------------------------------------

Total Medicines Created: 100+
Total Users Created: 2
```

### Step 2: Verify Database Creation

After running the seed script, you should see a new file `warehouse.db` in your project root directory.

```bash
ls -la *.db
# or on Windows
dir *.db
```

---

## Running the Application

### Step 1: Start the Flask Development Server

```bash
python app.py
```

**Expected Output:**
```
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
```

### Step 2: Access the Application

Open your web browser and navigate to:
```
http://127.0.0.1:5000
```
or
```
http://localhost:5000
```

You should see the application homepage with a professional interface.

### Step 3: Stop the Server

To stop the application, press `CTRL+C` in the terminal.

---

## Default Login Credentials

Use these credentials to access the application:

### Administrator Account
- **Username:** `admin`
- **Password:** `admin123`
- **Permissions:** Full access to all features including:
  - Add/Edit/Delete medicines
  - View analytics and reports
  - Manage sales
  - Access admin dashboard

### Staff Account
- **Username:** `staff`
- **Password:** `staff123`
- **Permissions:** Limited access:
  - View medicines
  - Record sales
  - View sales history
  - Access staff dashboard

> **Security Note:** Change these default credentials in a production environment!

---

## Project Structure

```
C-Project/
│
├── app.py                      # Application entry point
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── seed_database.py           # Database seeding script
├── README.md                   # This file
│
├── models/                     # Database models
│   ├── __init__.py
│   ├── user.py                # User model
│   ├── medicine.py            # Medicine & Alternative models
│   └── sale.py                # Sales model
│
├── routes/                     # Application routes
│   ├── __init__.py
│   ├── auth.py                # Authentication routes
│   ├── admin.py               # Admin routes
│   ├── staff.py               # Staff routes
│   ├── medicine.py            # Medicine CRUD routes
│   ├── sales.py               # Sales routes
│   ├── shared.py              # Shared routes
│   └── decorators.py          # Route decorators
│
├── forms/                      # WTForms definitions
│   ├── __init__.py
│   ├── auth_forms.py          # Authentication forms
│   └── sale_forms.py          # Sales forms
│
├── templates/                  # HTML templates
│   ├── base.html              # Base template
│   ├── home.html              # Homepage
│   ├── auth/                  # Authentication templates
│   ├── admin/                 # Admin templates
│   ├── staff/                 # Staff templates
│   ├── shared/                # Shared templates
│   ├── components/            # Reusable components
│   └── errors/                # Error pages
│
├── static/                     # Static files
│   ├── css/
│   │   └── custom.css         # Custom styles
│   └── js/
│       ├── main.js            # Main JavaScript
│       ├── scanner.js         # Barcode scanner
│       └── validation.js      # Form validation
│
├── utils/                      # Utility functions
│   ├── __init__.py
│   ├── analytics.py           # Analytics utilities
│   └── decorators.py          # Function decorators
│
└── tests/                      # Test files
    ├── __init__.py
    ├── conftest.py            # Test configuration
    ├── test_models.py         # Model tests
    └── test_routes.py         # Route tests
```

---

## Usage Guide

### For Administrators

1. **Login** with admin credentials
2. **Dashboard** - View system overview, statistics, and alerts
3. **Manage Medicines**:
   - Navigate to "Medicines" in the menu
   - Click "Add Medicine" to create new entries
   - Use search and filter options to find medicines
   - Edit or delete existing medicines
4. **View Analytics**:
   - Access "Reports" for detailed analytics
   - View sales trends and forecasts
   - Export data to CSV
5. **Record Sales**:
   - Go to "Sell Medicines"
   - Scan barcode or search manually
   - Complete the transaction
6. **Manage Alternatives**:
   - View and add alternative medicines for out-of-stock items

### For Staff

1. **Login** with staff credentials
2. **Dashboard** - View assigned tasks and statistics
3. **Browse Medicines** - Search and filter inventory
4. **Record Sales** - Process customer purchases
5. **View Sales History** - Check past transactions

---

## Troubleshooting

### Issue: "Module not found" error

**Solution:**
```bash
# Ensure virtual environment is activated
# On Windows: venv\Scripts\activate
# On macOS/Linux: source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: Database not found

**Solution:**
```bash
# Re-run the seeding script
python seed_database.py
```

### Issue: Port 5000 already in use

**Solution:**
```bash
# Kill the process using port 5000
# On Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# On macOS/Linux:
lsof -ti:5000 | xargs kill -9

# Or run on a different port
flask run --port 5001
```

### Issue: Permission denied when installing packages

**Solution:**
```bash
# Use --user flag
pip install --user -r requirements.txt

# Or run with elevated permissions (not recommended in venv)
```

### Issue: Python command not recognized

**Solution:**
- Windows: Use `py` instead of `python`
- macOS/Linux: Use `python3` instead of `python`
- Ensure Python is added to PATH during installation

### Issue: Static files (CSS/JS) not loading

**Solution:**
```bash
# Clear browser cache (Ctrl+Shift+R or Cmd+Shift+R)
# Or use incognito/private browsing mode
```

---

## Contributing

This is an academic capstone project. If you'd like to contribute or have suggestions:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## Team

This project was developed by:

- **Chandralekha S** - Project Lead & Developer
- **Akshaya N** - Developer & Designer
- **S Sridevi** - Developer & Tester

### Contact

- **Email:** chandralekha508@gmail.com
- **Phone:** +91 7022897595

---

## License

This project is developed for academic purposes as a capstone project. All rights reserved.

---

## Acknowledgments

- Built with Flask and Bootstrap
- Chart.js for beautiful visualizations
- Bootstrap Icons for UI elements
- Inspired by real-world pharmaceutical inventory management needs

---

## Screenshots

### Homepage
Professional landing page with feature highlights and clear call-to-action.

### Medicine Inventory
Browse 100+ medicines with advanced search and filtering capabilities.

### Analytics Dashboard
Comprehensive sales analytics with charts and predictive insights.

### Sales Interface
Streamlined sales recording with barcode scanning support.

---

## Future Enhancements

- Email notifications for low stock and expiring medicines
- Advanced machine learning for demand forecasting
- Mobile app development
- Multi-warehouse support
- RESTful API for third-party integrations
- Dark mode support
- Print receipt functionality

---

## Version History

- **v1.0.0** (Current) - Initial release with core features
  - Medicine inventory management
  - Sales tracking
  - Analytics and reporting
  - Role-based access control
  - 100+ sample medicines

---

**Made with ❤️ for Academic Excellence**
