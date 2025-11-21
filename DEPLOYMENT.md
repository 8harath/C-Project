# Deployment Guide - Warehouse Inventory Management System

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [Production Deployment](#production-deployment)
4. [Environment Variables](#environment-variables)
5. [Database Migrations](#database-migrations)
6. [Performance Considerations](#performance-considerations)
7. [Security Checklist](#security-checklist)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### System Requirements
- Python 3.8 or higher
- pip (Python package manager)
- SQLite 3 (included with Python)
- Git (for version control)

### Optional (for production)
- Nginx or Apache (web server)
- Gunicorn or uWSGI (WSGI server)
- PostgreSQL or MySQL (recommended for production)
- SSL certificate (for HTTPS)

---

## Local Development Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd C-Project
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///warehouse.db
FLASK_ENV=development
FLASK_DEBUG=1
```

### 5. Initialize Database

```bash
# Create database and seed with sample data
python seed_database.py
```

### 6. Run the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

### Default Login Credentials
- **Admin**: username: `admin`, password: `admin123`
- **Staff**: username: `staff`, password: `staff123`

---

## Production Deployment

### 1. Prepare Production Environment

```bash
# Create production directory
mkdir -p /var/www/warehouse-inventory
cd /var/www/warehouse-inventory

# Clone repository
git clone <repository-url> .

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn  # WSGI server for production
```

### 2. Configure Environment Variables

Create a `.env` file with production settings:

```env
SECRET_KEY=<generate-strong-random-key>
DATABASE_URL=postgresql://user:password@localhost/warehouse_db
FLASK_ENV=production
FLASK_DEBUG=0
SESSION_COOKIE_SECURE=True
```

**Generate a strong secret key:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 3. Setup Production Database

#### Option A: PostgreSQL (Recommended)

```bash
# Install PostgreSQL
sudo apt-get install postgresql postgresql-contrib

# Create database and user
sudo -u postgres psql
CREATE DATABASE warehouse_db;
CREATE USER warehouse_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE warehouse_db TO warehouse_user;
\q

# Update DATABASE_URL in .env
DATABASE_URL=postgresql://warehouse_user:your_password@localhost/warehouse_db
```

#### Option B: MySQL

```bash
# Install MySQL
sudo apt-get install mysql-server

# Create database
sudo mysql
CREATE DATABASE warehouse_db;
CREATE USER 'warehouse_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON warehouse_db.* TO 'warehouse_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;

# Update DATABASE_URL in .env
DATABASE_URL=mysql+pymysql://warehouse_user:your_password@localhost/warehouse_db
```

### 4. Initialize Production Database

```bash
source venv/bin/activate
python seed_database.py
```

### 5. Setup Gunicorn

Create a systemd service file `/etc/systemd/system/warehouse.service`:

```ini
[Unit]
Description=Warehouse Inventory Management System
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/warehouse-inventory
Environment="PATH=/var/www/warehouse-inventory/venv/bin"
ExecStart=/var/www/warehouse-inventory/venv/bin/gunicorn --workers 4 --bind 127.0.0.1:8000 "app:create_app()"

[Install]
WantedBy=multi-user.target
```

Start and enable the service:

```bash
sudo systemctl start warehouse
sudo systemctl enable warehouse
sudo systemctl status warehouse
```

### 6. Configure Nginx

Create Nginx configuration file `/etc/nginx/sites-available/warehouse`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /var/www/warehouse-inventory/static;
        expires 30d;
    }
}
```

Enable the site:

```bash
sudo ln -s /etc/nginx/sites-available/warehouse /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 7. Setup SSL with Let's Encrypt

```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

---

## Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `SECRET_KEY` | Flask secret key for sessions | - | Yes |
| `DATABASE_URL` | Database connection string | `sqlite:///warehouse.db` | No |
| `FLASK_ENV` | Environment mode | `development` | No |
| `FLASK_DEBUG` | Enable debug mode | `0` | No |
| `SESSION_COOKIE_SECURE` | Use secure cookies (HTTPS only) | `False` | No |

---

## Database Migrations

### Using Flask-Migrate (Optional)

If you need to make schema changes:

```bash
# Install Flask-Migrate
pip install Flask-Migrate

# Initialize migrations
flask db init

# Create migration
flask db migrate -m "Description of changes"

# Apply migration
flask db upgrade
```

---

## Performance Considerations

### 1. Database Optimization

- **Indexes**: All frequently queried fields are indexed
- **Query Optimization**: Use eager loading for relationships
- **Connection Pooling**: Configure database connection pooling

### 2. Caching

Consider adding Redis for caching:

```bash
pip install Flask-Caching redis
```

### 3. Static Files

- Use CDN for Bootstrap, Chart.js, and other static assets
- Enable gzip compression in Nginx
- Set proper cache headers

### 4. Application Performance

- Increase Gunicorn workers based on CPU cores: `workers = (2 * cpu_cores) + 1`
- Monitor application with tools like New Relic or Datadog
- Use profiling tools to identify bottlenecks

---

## Security Checklist

- [ ] Change default admin and staff passwords
- [ ] Use strong SECRET_KEY in production
- [ ] Enable HTTPS (SSL/TLS)
- [ ] Set `SESSION_COOKIE_SECURE=True` for HTTPS
- [ ] Configure firewall (allow only HTTP/HTTPS)
- [ ] Keep dependencies updated: `pip list --outdated`
- [ ] Implement rate limiting (Flask-Limiter)
- [ ] Regular database backups
- [ ] Monitor application logs
- [ ] Use environment variables for sensitive data

---

## Troubleshooting

### Issue: Application won't start

**Solution:**
```bash
# Check logs
sudo journalctl -u warehouse -n 50

# Verify Gunicorn is running
ps aux | grep gunicorn

# Check port availability
sudo netstat -tulpn | grep 8000
```

### Issue: Database connection errors

**Solution:**
```bash
# Verify database is running
sudo systemctl status postgresql

# Check DATABASE_URL in .env
# Ensure user has proper permissions
```

### Issue: Static files not loading

**Solution:**
```bash
# Check Nginx configuration
sudo nginx -t

# Verify static file path
ls -la /var/www/warehouse-inventory/static

# Check Nginx error logs
sudo tail -f /var/log/nginx/error.log
```

### Issue: Permission denied errors

**Solution:**
```bash
# Fix ownership
sudo chown -R www-data:www-data /var/www/warehouse-inventory

# Fix permissions
sudo chmod -R 755 /var/www/warehouse-inventory
```

---

## Maintenance

### Backup Database

```bash
# SQLite
cp warehouse.db warehouse_backup_$(date +%Y%m%d).db

# PostgreSQL
pg_dump warehouse_db > warehouse_backup_$(date +%Y%m%d).sql

# MySQL
mysqldump warehouse_db > warehouse_backup_$(date +%Y%m%d).sql
```

### Update Application

```bash
cd /var/www/warehouse-inventory
source venv/bin/activate
git pull origin main
pip install -r requirements.txt
sudo systemctl restart warehouse
```

### Monitor Logs

```bash
# Application logs
sudo journalctl -u warehouse -f

# Nginx access logs
sudo tail -f /var/log/nginx/access.log

# Nginx error logs
sudo tail -f /var/log/nginx/error.log
```

---

## Support

For issues or questions:
- Email: chandralekha508@gmail.com
- Phone: +91 7022897595

---

**Last Updated:** November 21, 2024
