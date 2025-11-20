# Software Requirements Specification (SRS)
## Warehouse and Inventory Management System - MVP

**Version:** 1.0  
**Date:** November 20, 2024  
**Project Team:** Chandralekha S, Akshaya N, S Sridevi  
**Contact:** chandralekha508@gmail.com | +91 7022897595

---

## 1. Introduction

### 1.1 Purpose
This document specifies the requirements for developing a Minimum Viable Product (MVP) of a Warehouse and Inventory Management System for pharmaceutical inventory management. The system enables role-based access for administrators and staff to manage medicine inventory, record sales, and generate basic analytical insights.

### 1.2 Scope
The MVP will deliver a Flask-based web application with the following core capabilities:
- Role-based user authentication (Admin/Staff)
- Medicine inventory management (CRUD operations)
- Barcode-based medicine scanning and sales recording
- Basic statistical analytics and reporting
- Low stock alerts and dashboard visualizations

### 1.3 Definitions and Acronyms
- **CRUD**: Create, Read, Update, Delete
- **MVP**: Minimum Viable Product
- **SQLAlchemy**: Python SQL toolkit and ORM
- **Bootstrap**: Frontend CSS framework
- **Flask**: Python web framework
- **SRS**: Software Requirements Specification

### 1.4 Out of Scope for MVP
- Email notifications (future enhancement)
- Complex ML algorithms (CatBoost, XGBoost)
- Mobile app development
- Multi-warehouse support
- Real-time inventory synchronization
- Advanced user role management beyond Admin/Staff

---

## 2. System Overview

### 2.1 System Architecture
```
┌─────────────────────────────────────────────────┐
│           Presentation Layer (Browser)          │
│  (Bootstrap + HTML Templates + JavaScript)      │
└─────────────────┬───────────────────────────────┘
                  │
┌─────────────────┴───────────────────────────────┐
│           Application Layer (Flask)             │
│  - Authentication & Authorization               │
│  - Business Logic                               │
│  - Route Handlers                               │
└─────────────────┬───────────────────────────────┘
                  │
┌─────────────────┴───────────────────────────────┐
│         Data Layer (SQLAlchemy + SQLite)        │
│  - User Model                                   │
│  - Medicine Model                               │
│  - Sale Model                                   │
└─────────────────────────────────────────────────┘
```

### 2.2 Technology Stack
- **Backend**: Flask (Python 3.8+)
- **ORM**: SQLAlchemy
- **Database**: SQLite 3
- **Frontend**: Bootstrap 5.x, HTML5, CSS3, JavaScript (ES6+)
- **Barcode Scanning**: QuaggaJS or html5-qrcode library
- **Charts/Graphs**: Chart.js
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF

---

## 3. Functional Requirements

### 3.1 User Management

#### 3.1.1 User Registration
**FR-UM-001**: The system shall allow new users to register with the following fields:
- Username (unique, alphanumeric, 3-20 characters)
- Email (unique, valid email format)
- Password (minimum 8 characters, hashed using bcrypt/werkzeug.security)
- Role (Admin or Staff)

**Acceptance Criteria:**
- Duplicate usernames/emails are rejected with appropriate error messages
- Passwords are stored as hashed values only
- Successful registration redirects to login page

#### 3.1.2 User Login
**FR-UM-002**: The system shall authenticate users based on username/email and password.

**Acceptance Criteria:**
- Valid credentials grant access with session management
- Invalid credentials display error message
- Session persists across page navigation
- Logout functionality clears session

#### 3.1.3 Role-Based Access Control
**FR-UM-003**: The system shall implement two user roles:

| Feature | Admin Access | Staff Access |
|---------|-------------|--------------|
| Dashboard (Analytics) | Full Access | Limited (Low Stock, Top Selling) |
| Manage Products | Full CRUD | Read Only |
| Predictive Insights | Full Access | No Access |
| Alternative Medicines | Full CRUD | Read Only |
| Sell Medicines | Yes | Yes |
| Reports | Full Access | No Access |
| Manage Users | Yes | No |
| Barcode Scanning | Yes | Yes |

### 3.2 Medicine Inventory Management

#### 3.2.1 Medicine Data Model
**FR-MIM-001**: Each medicine record shall contain:
- **medicine_id** (Primary Key, Auto-increment)
- **name** (String, required, max 200 characters)
- **description** (Text, optional)
- **manufacturer** (String, required, max 200 characters)
- **category** (String, required, one of: Allergy, Cold and Mild Flu, Cough, Dermatology, Eye/ENT, Fever, Pain Relief, Vitamins, Women Hygiene)
- **quantity** (Integer, required, default 0)
- **price** (Decimal, required, precision 10.2)
- **expiry_date** (Date, required, format: YYYY-MM-DD)
- **stock** (Integer, required, default 0)
- **reorder_level** (Integer, required, default 10)
- **barcode** (String, unique, required, 13 characters for EAN-13 format)
- **created_at** (DateTime, auto-generated)
- **updated_at** (DateTime, auto-updated)

#### 3.2.2 Medicine Categories
**FR-MIM-002**: The system shall support 9 predefined medicine categories with minimum 10 medicines each:
1. Allergy (10+ medicines)
2. Cold and Mild Flu (10+ medicines)
3. Cough (10+ medicines)
4. Dermatology (10+ medicines)
5. Eye/ENT (10+ medicines)
6. Fever (10+ medicines)
7. Pain Relief (10+ medicines)
8. Vitamins (10+ medicines)
9. Women Hygiene (10+ medicines)

**Total medicines in seed data: 100**

#### 3.2.3 Add Medicine
**FR-MIM-003**: Admins shall be able to add new medicines via a form with validation:
- All required fields must be filled
- Barcode must be unique (13-digit numeric)
- Expiry date must be future date
- Price and quantities must be positive numbers
- Category must match predefined list

#### 3.2.4 Edit Medicine
**FR-MIM-004**: Admins shall be able to edit existing medicine records with same validation rules as add.

#### 3.2.5 Delete Medicine
**FR-MIM-005**: Admins shall be able to delete medicine records with confirmation dialog.
- Soft delete preferred (mark as inactive) if sales history exists
- Hard delete allowed if no sales history

#### 3.2.6 View Medicines
**FR-MIM-006**: The system shall display medicines in a paginated, searchable table with:
- Category-based filtering
- Search by name/manufacturer
- Sort by name, price, stock, expiry date
- Display: Name, Category, Manufacturer, Qty, Price, Expiry, Stock, Reorder Level, Barcode
- Action buttons: Edit, Delete (Admin only)

#### 3.2.7 Low Stock Alerts
**FR-MIM-007**: The system shall identify and display medicines where `stock <= reorder_level`:
- Dashboard popup alert on login (for Admin and Staff)
- Visual indicator (red badge) on medicine list
- Count of low stock items on dashboard

### 3.3 Alternative Medicine Management

#### 3.3.1 Alternative Medicine Data Model
**FR-AMM-001**: Each alternative medicine record shall link to a primary medicine and contain:
- **alternative_id** (Primary Key, Auto-increment)
- **primary_medicine_id** (Foreign Key to Medicine)
- **alternative_medicine_id** (Foreign Key to Medicine)
- **reason** (Text, optional - e.g., "Same active ingredient", "Similar therapeutic effect")
- **priority** (Integer, 1-10, for ranking alternatives)

#### 3.3.2 View Alternative Medicines
**FR-AMM-002**: The system shall display 5-10 alternative medicines for each primary medicine grouped by category.

**Display format:**
```
Primary Medicine: Dolo 650mg
Alternatives:
1. Crocin 650mg (Same: Paracetamol)
2. Calpol 650mg (Same: Paracetamol)
3. Metacin 650mg (Same: Paracetamol)
[... 5-10 alternatives total]
```

#### 3.3.3 Manage Alternatives (Admin Only)
**FR-AMM-003**: Admins shall be able to:
- Add alternative medicine mappings
- Edit priority/reason
- Delete alternative mappings
- View all alternatives in category-wise lists

### 3.4 Sales Management

#### 3.4.1 Sale Data Model
**FR-SM-001**: Each sale record shall contain:
- **sale_id** (Primary Key, Auto-increment)
- **medicine_id** (Foreign Key to Medicine)
- **user_id** (Foreign Key to User - staff who made sale)
- **quantity_sold** (Integer, required, > 0)
- **total_price** (Decimal, calculated as: medicine.price × quantity_sold)
- **sale_date** (DateTime, auto-generated)

#### 3.4.2 Record Sale via Barcode
**FR-SM-002**: Staff and Admin shall be able to record sales by:
1. Scanning barcode using web camera (QuaggaJS library)
2. System auto-fills medicine details based on barcode
3. User enters quantity to sell
4. System validates:
   - Quantity available in stock (qty >= quantity_sold)
   - Medicine not expired (expiry_date > current_date)
5. On confirmation:
   - Create Sale record
   - Update Medicine.stock (decrement by quantity_sold)
   - Display success message with receipt summary

**Barcode Scanner Requirements:**
- Support EAN-13 format (13-digit barcodes)
- Real-time camera preview
- Sound feedback on successful scan
- Manual barcode entry fallback option

#### 3.4.3 Record Sale via Medicine List
**FR-SM-003**: Alternative to barcode scanning, users can:
- Browse medicine list (category-filtered)
- Select medicine
- Enter quantity
- Complete sale with same validation as FR-SM-002

#### 3.4.4 Sale Receipt Display
**FR-SM-004**: After successful sale, display receipt with:
- Medicine name
- Quantity sold
- Unit price
- Total price
- Date & time
- Staff name
- Print option (browser print)

### 3.5 Dashboard & Analytics

#### 3.5.1 Admin Dashboard
**FR-DA-001**: Admin dashboard shall display:

**Key Metrics Cards:**
- Total Sales (₹) - Sum of all sale.total_price
- Total Medicines - Count of active medicines
- Low Stock Items - Count where stock <= reorder_level
- Total Transactions - Count of sales

**Visualizations:**
1. **Top Selling Medicines (Pie Chart)**
   - Top 5 medicines by quantity sold
   - Chart.js implementation
   - Interactive tooltips

2. **Seasonal Sales Chart (Bar Chart)**
   - Sales grouped by season:
     - Winter: Dec, Jan, Feb
     - Spring: Mar, Apr, May
     - Summer: Jun, Jul, Aug
     - Monsoon: Sep, Oct, Nov
   - X-axis: Seasons, Y-axis: Total Sales (₹)

3. **Low Stock Alert Popup**
   - Modal dialog on dashboard load
   - List of medicines with stock <= reorder_level
   - Dismiss option

#### 3.5.2 Staff Dashboard
**FR-DA-002**: Staff dashboard shall display:
- Low Stock Warning (count + list)
- Top Selling Medicines Graph (bar chart, top 10)
- Quick access to Sell page and Scan page

### 3.6 Predictive Insights (Admin Only)

#### 3.6.1 Seasonal Forecast
**FR-PI-001**: Display high and low demand medicines per season based on historical sales.

**Calculation Method:**
- Group sales by season (last 12 months)
- Calculate average sales per medicine per season
- Rank medicines by average sales
- Display top 5 (high demand) and bottom 5 (low demand) per season

#### 3.6.2 Monthly Summary
**FR-PI-002**: Display monthly sales and expenditure with date range filter.

**Features:**
- Date range picker (Start Date, End Date)
- Table display:
  - Month-Year
  - Total Sales (₹)
  - Total Transactions
  - Average Transaction Value
- CSV export option

**Calculation:**
```
Total Sales = SUM(sale.total_price WHERE sale_date BETWEEN start_date AND end_date)
Total Transactions = COUNT(sale.sale_id WHERE sale_date BETWEEN start_date AND end_date)
Average Transaction = Total Sales / Total Transactions
```

#### 3.6.3 Top Medicines by Month
**FR-PI-003**: Display most sold medicines for each month (last 12 months).

**Display Format:**
- Table with columns: Month, Medicine Name, Quantity Sold, Total Sales (₹)
- Top 3 medicines per month
- Sorted by month (most recent first)

#### 3.6.4 Next Month Prediction
**FR-PI-004**: Predict next month's sales based on previous 3 months using moving average.

**Calculation Method:**
```python
# Simple Moving Average (SMA)
month_1_sales = total_sales(current_month - 1)
month_2_sales = total_sales(current_month - 2)
month_3_sales = total_sales(current_month - 3)

predicted_sales = (month_1_sales + month_2_sales + month_3_sales) / 3
```

**Display:**
- Predicted sales amount (₹)
- Confidence note: "Based on 3-month moving average"
- Previous 3 months actual sales for comparison

#### 3.6.5 Forecast Visualization
**FR-PI-005**: Line chart showing monthly sales trend for last 12 months + next month prediction.

**Chart Features:**
- X-axis: Month-Year
- Y-axis: Total Sales (₹)
- Historical data: Solid line
- Predicted data: Dashed line (different color)
- Chart.js implementation
- Interactive tooltips

### 3.7 Reports

#### 3.7.1 Sales Report
**FR-RP-001**: Admin shall generate sales reports with filters:

**Filters:**
- Start Date (date picker)
- End Date (date picker)
- Category (dropdown, optional)
- Medicine (dropdown, optional)

**Report Display:**
- Total Transactions
- Total Sales (₹)
- Average Transaction Value
- Table: Sale Date, Medicine Name, Category, Quantity, Total Price, Staff Name

**Export:**
- CSV export button
- File format: `sales_report_YYYYMMDD_HHMMSS.csv`
- Include all filtered data

#### 3.7.2 Inventory Report
**FR-RP-002**: Admin shall view current inventory status.

**Report Sections:**
1. **Expiring Soon** - Medicines expiring within 30 days
2. **Low Stock** - Medicines where stock <= reorder_level
3. **Category-wise Stock** - Grouped by category with total stock and value

**Export:** CSV option available

### 3.8 Barcode Scanning

#### 3.8.1 Scan Page
**FR-BS-001**: Dedicated scan page with:
- Camera preview area (full width, responsive)
- Start/Stop scanning buttons
- Manual barcode entry input field
- Detected barcode display
- Auto-redirect to sell page with medicine pre-selected after successful scan

**Technical Implementation:**
- Use QuaggaJS or html5-qrcode library
- Request camera permissions on page load
- Support rear camera preference on mobile devices
- Display error message if camera access denied

### 3.9 About & Information Pages

#### 3.9.1 About Page
**FR-AP-001**: Static page containing:
- System description (2-3 paragraphs about warehouse management features)
- Team members:
  - Chandralekha S
  - Akshaya N
  - S Sridevi
- Contact information:
  - Email: chandralekha508@gmail.com
  - Phone: +91 7022897595
- Social media placeholders:
  - Instagram icon (link: TBD)
  - Play Store icon (link: TBD)

#### 3.9.2 Footer
**FR-AP-002**: All pages shall include footer with:
- Copyright notice: "© 2024 Warehouse Inventory Management System. All rights reserved."
- Link to About page
- Social media icons
- Contact information

---

## 4. Non-Functional Requirements

### 4.1 Performance
**NFR-P-001**: Page load time shall not exceed 3 seconds on local network.  
**NFR-P-002**: Database queries shall be optimized with appropriate indexes.  
**NFR-P-003**: Barcode scanning shall detect code within 2 seconds under good lighting.

### 4.2 Security
**NFR-S-001**: Passwords shall be hashed using bcrypt or werkzeug.security with minimum cost factor 12.  
**NFR-S-002**: SQL injection protection via SQLAlchemy ORM parameterized queries.  
**NFR-S-003**: XSS protection via Flask template auto-escaping.  
**NFR-S-004**: CSRF protection via Flask-WTF tokens.  
**NFR-S-005**: Session management with secure, httponly cookies.

### 4.3 Usability
**NFR-U-001**: UI shall be responsive (mobile, tablet, desktop) using Bootstrap grid.  
**NFR-U-002**: Forms shall provide inline validation with clear error messages.  
**NFR-U-003**: Confirmation dialogs required for delete operations.  
**NFR-U-004**: Loading indicators displayed during async operations.

### 4.4 Reliability
**NFR-R-001**: Database transactions shall be atomic (commit/rollback).  
**NFR-R-002**: System shall handle concurrent users (minimum 10 simultaneous users).  
**NFR-R-003**: Error logging implemented for debugging (Flask logging to file).

### 4.5 Maintainability
**NFR-M-001**: Code shall follow PEP 8 style guide for Python.  
**NFR-M-002**: Functions shall be documented with docstrings.  
**NFR-M-003**: Database migrations managed via Flask-Migrate (Alembic).  
**NFR-M-004**: Configuration separated from code (config.py file).

### 4.6 Browser Compatibility
**NFR-B-001**: Support for:
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

---

## 5. Database Schema

### 5.1 Entity Relationship Diagram

```
┌─────────────────┐         ┌──────────────────────┐         ┌─────────────────┐
│      User       │         │      Medicine        │         │  Alternative    │
├─────────────────┤         ├──────────────────────┤         │    Medicine     │
│ user_id (PK)    │         │ medicine_id (PK)     │◄────────┤─────────────────┤
│ username        │         │ name                 │         │ alternative_id  │
│ email           │         │ description          │         │ primary_med_id  │
│ password_hash   │         │ manufacturer         │         │ alt_med_id      │
│ role            │         │ category             │         │ reason          │
│ created_at      │         │ quantity             │         │ priority        │
└────────┬────────┘         │ price                │         └─────────────────┘
         │                  │ expiry_date          │
         │                  │ stock                │
         │                  │ reorder_level        │
         │                  │ barcode              │
         │                  │ created_at           │
         │                  │ updated_at           │
         │                  └──────────┬───────────┘
         │                             │
         │      ┌──────────────────────┘
         │      │
         │      │
         ▼      ▼
    ┌─────────────────┐
    │      Sale       │
    ├─────────────────┤
    │ sale_id (PK)    │
    │ medicine_id(FK) │
    │ user_id (FK)    │
    │ quantity_sold   │
    │ total_price     │
    │ sale_date       │
    └─────────────────┘
```

### 5.2 Table Specifications

#### User Table
```sql
CREATE TABLE user (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(200) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK(role IN ('Admin', 'Staff')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Medicine Table
```sql
CREATE TABLE medicine (
    medicine_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    manufacturer VARCHAR(200) NOT NULL,
    category VARCHAR(50) NOT NULL CHECK(category IN (
        'Allergy', 'Cold and Mild Flu', 'Cough', 'Dermatology', 
        'Eye/ENT', 'Fever', 'Pain Relief', 'Vitamins', 'Women Hygiene'
    )),
    quantity INTEGER NOT NULL DEFAULT 0,
    price DECIMAL(10,2) NOT NULL,
    expiry_date DATE NOT NULL,
    stock INTEGER NOT NULL DEFAULT 0,
    reorder_level INTEGER NOT NULL DEFAULT 10,
    barcode VARCHAR(13) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CHECK(price >= 0),
    CHECK(quantity >= 0),
    CHECK(stock >= 0),
    CHECK(reorder_level >= 0)
);

CREATE INDEX idx_medicine_category ON medicine(category);
CREATE INDEX idx_medicine_barcode ON medicine(barcode);
CREATE INDEX idx_medicine_expiry ON medicine(expiry_date);
CREATE INDEX idx_medicine_stock ON medicine(stock);
```

#### Sale Table
```sql
CREATE TABLE sale (
    sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
    medicine_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    quantity_sold INTEGER NOT NULL,
    total_price DECIMAL(10,2) NOT NULL,
    sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (medicine_id) REFERENCES medicine(medicine_id),
    FOREIGN KEY (user_id) REFERENCES user(user_id),
    CHECK(quantity_sold > 0),
    CHECK(total_price >= 0)
);

CREATE INDEX idx_sale_date ON sale(sale_date);
CREATE INDEX idx_sale_medicine ON sale(medicine_id);
CREATE INDEX idx_sale_user ON sale(user_id);
```

#### Alternative Medicine Table
```sql
CREATE TABLE alternative_medicine (
    alternative_id INTEGER PRIMARY KEY AUTOINCREMENT,
    primary_medicine_id INTEGER NOT NULL,
    alternative_medicine_id INTEGER NOT NULL,
    reason TEXT,
    priority INTEGER DEFAULT 5 CHECK(priority BETWEEN 1 AND 10),
    FOREIGN KEY (primary_medicine_id) REFERENCES medicine(medicine_id),
    FOREIGN KEY (alternative_medicine_id) REFERENCES medicine(medicine_id),
    UNIQUE(primary_medicine_id, alternative_medicine_id)
);

CREATE INDEX idx_alt_primary ON alternative_medicine(primary_medicine_id);
```

---

## 6. User Interface Requirements

### 6.1 Template Structure
```
templates/
├── base.html                 # Base template with navbar, footer
├── home.html                 # Landing page
├── auth/
│   ├── login.html           # Login page
│   └── register.html        # Registration page
├── admin/
│   ├── admin_dashboard.html
│   ├── manage_products.html
│   ├── manage_users.html
│   ├── predictive_insights.html
│   ├── reports.html
│   └── medicines.html       # Alternative medicines
├── staff/
│   └── staff_dashboard.html
└── shared/
    ├── sell_medicines.html
    ├── scan.html
    ├── receipts.html
    ├── products.html         # View all products
    └── about.html
```

### 6.2 Navigation Menu

**Admin Menu:**
- Dashboard
- Manage Products
- Alternative Medicines
- Predictive Insights
- Sell
- Scan
- Reports
- Manage Users (Admin only)
- About
- Logout

**Staff Menu:**
- Dashboard
- Products (View only)
- Sell
- Scan
- About
- Logout

### 6.3 Color Scheme & Styling
- Primary color: #007bff (Bootstrap blue)
- Success: #28a745 (green for success messages, in-stock)
- Warning: #ffc107 (yellow for low stock alerts)
- Danger: #dc3545 (red for errors, critical stock)
- Font: System font stack (Bootstrap default)
- Responsive breakpoints: Bootstrap standard (576px, 768px, 992px, 1200px)

### 6.4 Form Validation
All forms shall implement:
- Client-side validation (HTML5 + JavaScript)
- Server-side validation (Flask-WTF)
- Error messages displayed above form fields in red
- Success messages displayed as dismissible alerts

---

## 7. API Endpoints (Flask Routes)

### 7.1 Authentication Routes
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/` | Home/Landing page | Public |
| GET/POST | `/login` | User login | Public |
| GET/POST | `/register` | User registration | Public |
| GET | `/logout` | User logout | Authenticated |

### 7.2 Dashboard Routes
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/admin/dashboard` | Admin dashboard | Admin |
| GET | `/staff/dashboard` | Staff dashboard | Staff |

### 7.3 Medicine Management Routes
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/medicines` | View all medicines | Authenticated |
| GET/POST | `/medicines/add` | Add new medicine | Admin |
| GET/POST | `/medicines/edit/<id>` | Edit medicine | Admin |
| POST | `/medicines/delete/<id>` | Delete medicine | Admin |
| GET | `/medicines/category/<category>` | Filter by category | Authenticated |

### 7.4 Alternative Medicine Routes
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/alternatives` | View alternatives | Authenticated |
| GET/POST | `/alternatives/add` | Add alternative | Admin |
| POST | `/alternatives/delete/<id>` | Delete alternative | Admin |

### 7.5 Sales Routes
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/sell` | Sell page (list view) | Staff, Admin |
| POST | `/sell/record` | Record sale | Staff, Admin |
| GET | `/scan` | Barcode scan page | Staff, Admin |
| POST | `/scan/process` | Process scanned barcode | Staff, Admin |
| GET | `/receipt/<sale_id>` | View receipt | Staff, Admin |

### 7.6 Analytics & Reports Routes
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/predictive-insights` | Predictive analytics page | Admin |
| GET | `/reports` | Sales reports | Admin |
| POST | `/reports/export` | Export CSV | Admin |

### 7.7 API Endpoints (AJAX)
| Method | Endpoint | Description | Returns |
|--------|----------|-------------|---------|
| GET | `/api/medicine/<barcode>` | Get medicine by barcode | JSON |
| GET | `/api/dashboard/stats` | Dashboard statistics | JSON |
| GET | `/api/sales/monthly` | Monthly sales data | JSON |
| GET | `/api/forecast/next-month` | Next month prediction | JSON |

---

## 8. Seed Data Specification

### 8.1 Sample Dataset Structure
Create a seed data file (`seed_data.py`) with 100 medicines distributed as follows:

#### Category Distribution:
1. **Allergy** (11 medicines)
   - Cetirizine, Loratadine, Fexofenadine, Levocetirizine, Desloratadine, Diphenhydramine, Chlorpheniramine, Hydroxyzine, Montelukast, Beclomethasone, Budesonide

2. **Cold and Mild Flu** (11 medicines)
   - Paracetamol, Phenylephrine, Pseudoephedrine, Guaifenesin, Acetaminophen combinations, Ambroxol, Bromhexine, Cetirizine+Phenylephrine, Dextromethorphan combos, Zinc supplements, Vitamin C tablets

3. **Cough** (11 medicines)
   - Dextromethorphan, Codeine, Guaifenesin, Ambroxol, Bromhexine, Honey-based syrups, Terbutaline, Salbutamol, Levosalbutamol, Theophylline, Chlorpheniramine

4. **Dermatology** (11 medicines)
   - Betamethasone, Hydrocortisone, Clotrimazole, Ketoconazole, Mupirocin, Fusidic acid, Benzoyl peroxide, Tretinoin, Calamine lotion, Povidone-iodine, Silver sulfadiazine

5. **Eye/ENT** (11 medicines)
   - Moxifloxacin eye drops, Ofloxacin eye drops, Ciprofloxacin ear drops, Chloramphenicol, Timolol, Latanoprost, Tropicamide, Phenylephrine eye drops, Sodium chloride drops, Tear substitutes, Wax softeners

6. **Fever** (11 medicines)
   - Paracetamol 500mg, Paracetamol 650mg, Ibuprofen, Mefenamic acid, Diclofenac, Aspirin, Nimesulide, Paracetamol suspensions (various brands), Ibuprofen suspensions

7. **Pain Relief** (12 medicines)
   - Ibuprofen, Diclofenac, Aceclofenac, Piroxicam, Tramadol, Ketorolac, Etoricoxib, Naproxen, Indomethacin, Paracetamol+Ibuprofen combos, Diclofenac gel, Capsaicin cream

8. **Vitamins** (11 medicines)
   - Vitamin D3, Vitamin B Complex, Vitamin C, Multivitamin tablets, Calcium+Vitamin D3, Iron+Folic acid, Vitamin E, Vitamin A, Omega-3, Biotin, Zinc supplements

9. **Women Hygiene** (11 medicines)
   - Clotrimazole pessaries, Metronidazole vaginal gel, Fluconazole, Mefenamic acid, Tranexamic acid, Norethisterone, Iron supplements, Folic acid, Calcium supplements, Cranberry supplements, Probiotics

### 8.2 Sample Medicine Records Format
```python
# Example seed data structure
medicines = [
    {
        "name": "Cetirizine 10mg",
        "description": "Antihistamine for allergy relief",
        "manufacturer": "Cipla Ltd",
        "category": "Allergy",
        "quantity": 150,
        "price": 45.00,
        "expiry_date": "2026-06-30",
        "stock": 150,
        "reorder_level": 20,
        "barcode": "8901234567890"
    },
    # ... 99 more medicines
]
```

### 8.3 Alternative Medicine Mapping
For the alternative medicines feature, create mappings for common medicines:

**Example Alternative Mappings:**
```python
alternatives = [
    # Paracetamol alternatives
    {
        "primary": "Dolo 650mg",
        "alternatives": ["Crocin 650mg", "Calpol 650mg", "Metacin 650mg", 
                        "Pacimol 650mg", "Pyrigesic 650mg"]
    },
    # Cetirizine alternatives
    {
        "primary": "Zyrtec 10mg",
        "alternatives": ["Alerid 10mg", "Cetriz 10mg", "Okacet 10mg", 
                        "Allercet 10mg", "Cetipen 10mg"]
    },
    # ... more mappings for at least 20 primary medicines
]
```

### 8.4 Seed Data Generation Script
Create `seed_database.py` script that:
1. Checks if database is empty
2. Creates default admin user (username: admin, password: admin123)
3. Creates test staff user (username: staff, password: staff123)
4. Inserts 100 medicine records
5. Creates alternative medicine mappings
6. Prints success message with login credentials

---

## 9. Implementation Guidelines

### 9.1 Project Structure
```
warehouse_inventory/
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── seed_database.py            # Seed data script
├── requirements.txt            # Python dependencies
├── models/
│   ├── __init__.py
│   ├── user.py                # User model
│   ├── medicine.py            # Medicine model
│   └── sale.py                # Sale model
├── routes/
│   ├── __init__.py
│   ├── auth.py                # Authentication routes
│   ├── admin.py               # Admin routes
│   ├── staff.py               # Staff routes
│   └── api.py                 # API endpoints
├── static/
│   ├── css/
│   │   └── custom.css         # Custom styles
│   ├── js/
│   │   ├── scanner.js         # Barcode scanning logic
│   │   ├── charts.js          # Chart.js configurations
│   │   └── main.js            # General JavaScript
│   └── images/
│       └── logo.png
├── templates/
│   └── [as specified in section 6.1]
└── warehouse.db               # SQLite database (generated)
```

### 9.2 Dependencies (requirements.txt)
```
Flask==2.3.3
Flask-SQLAlchemy==3.0.5
Flask-Login==0.6.2
Flask-WTF==1.1.1
WTForms==3.0.1
email-validator==2.0.0
python-dotenv==1.0.0
```

### 9.3 Development Steps

**Phase 1: Setup & Models (Days 1-2)**
1. Initialize Flask project structure
2. Configure SQLAlchemy and database
3. Create User, Medicine, Sale models
4. Test database operations with sample data

**Phase 2: Authentication (Day 3)**
5. Implement user registration
6. Implement login/logout with Flask-Login
7. Add role-based access control decorators

**Phase 3: Medicine Management (Days 4-5)**
8. Create medicine CRUD operations
9. Implement search and filter functionality
10. Add low stock alert logic
11. Create seed data script and populate database

**Phase 4: Sales Module (Days 6-7)**
12. Implement sell page (list view)
13. Integrate barcode scanning (QuaggaJS)
14. Add sale recording logic with stock updates
15. Create receipt display page

**Phase 5: Dashboards (Days 8-9)**
16. Build admin dashboard with statistics
17. Implement Chart.js visualizations
18. Build staff dashboard
19. Add low stock popup alerts

**Phase 6: Analytics & Reporting (Days 10-11)**
20. Implement seasonal forecast calculations
21. Create monthly summary with filters
22. Add next month prediction (moving average)
23. Build reports page with CSV export

**Phase 7: Alternative Medicines (Day 12)**
24. Create alternative medicine management
25. Display alternatives grouped by category
26. Add CRUD operations for alternatives

**Phase 8: UI Polish & Testing (Days 13-14)**
27. Implement responsive design
28. Add loading indicators and form validations
29. Create about page with team info
30. End-to-end testing and bug fixes

### 9.4 Testing Checklist
- [ ] User registration with duplicate detection
- [ ] Login with valid/invalid credentials
- [ ] Admin can access all features
- [ ] Staff has restricted access
- [ ] Medicine CRUD operations work correctly
- [ ] Stock updates after sales
- [ ] Barcode scanning detects EAN-13 codes
- [ ] Low stock alerts display correctly
- [ ] Charts render with accurate data
- [ ] Date filters work in reports
- [ ] CSV export downloads correctly
- [ ] Moving average prediction calculates accurately
- [ ] Alternative medicine mappings display correctly
- [ ] Responsive design on mobile/tablet
- [ ] Form validations work (client & server side)

---

## 10. Deployment Instructions

### 10.1 Local Development Setup
```bash
# 1. Clone repository
git clone <repository-url>
cd warehouse_inventory

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Initialize database and seed data
python seed_database.py

# 5. Run application
python app.py

# 6. Access at http://localhost:5000
```

### 10.2 Default Login Credentials
- **Admin:** username: `admin`, password: `admin123`
- **Staff:** username: `staff`, password: `staff123`

### 10.3 Configuration Variables
In `config.py`:
```python
SECRET_KEY = 'your-secret-key-here'  # Change in production
SQLALCHEMY_DATABASE_URI = 'sqlite:///warehouse.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SESSION_COOKIE_SECURE = False  # True in production with HTTPS
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
```

---

## 11. Future Enhancements (Post-MVP)

1. **Email Notifications**
   - Low stock email alerts
   - Expiry date reminders
   - Daily/weekly sales summaries

2. **Advanced ML Models**
   - Implement XGBoost for demand forecasting
   - Seasonal ARIMA for time series prediction
   - Customer segmentation

3. **Mobile Application**
   - React Native app for Android/iOS
   - Offline mode for sales recording
   - Push notifications

4. **Multi-warehouse Support**
   - Warehouse management with transfers
   - Location-based inventory tracking

5. **Supplier Management**
   - Supplier contact management
   - Purchase order generation
   - Auto-reorder based on reorder levels

6. **Advanced Reporting**
   - Profit margin analysis
   - Dead stock identification
   - ABC analysis for inventory

---

## 12. Glossary

| Term | Definition |
|------|------------|
| Barcode | Machine-readable code (EAN-13 format) for product identification |
| CRUD | Create, Read, Update, Delete operations |
| Moving Average | Statistical calculation averaging data over time periods |
| Reorder Level | Minimum stock quantity triggering restock alert |
| Seasonal Forecast | Prediction of demand patterns based on seasons |
| Seed Data | Initial dataset for testing and demonstration |
| SQLAlchemy | Python ORM for database operations |
| SQLite | Lightweight file-based relational database |

---

## 13. Approval & Sign-off

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Project Lead | Chandralekha S | | |
| Team Member | Akshaya N | | |
| Team Member | S Sridevi | | |
| Instructor/Advisor | | | |

---

**Document Version Control:**
- Version 1.0 - November 20, 2024 - Initial MVP SRS

**Contact for Clarifications:**
- Email: chandralekha508@gmail.com
- Phone: +91 7022897595

---

*End of Software Requirements Specification Document*
