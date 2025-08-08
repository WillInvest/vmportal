# VMPortal

VMPortal is a Django web application for managing and tracking applications (or any custom workflow you define). This repository includes everything you need to deploy it to a new server with minimal setup.

---

## 📂 Project Structure

```
vmportal/
├── applications/             # Main Django app
├── templates/                 # HTML templates
├── staticfiles/               # Collected static assets
├── vmportal/                  # Django project settings & URLs
├── db.sqlite3                  # Local development DB (SQLite)
├── manage.py
└── ops/                       # Deployment scripts & configs
    ├── bootstrap.sh           # Main deployment script
    ├── environment.yml        # Conda environment spec
    ├── environment.lock.yml   # Full locked env
    ├── gunicorn-vmportal.service  # Systemd service config
    └── nginx.vmportal.conf    # Nginx site config
```

---

## 🚀 Quick Start (Local Development)

1. **Clone the repository**

   ```bash
   git clone https://github.com/<your-username>/vmportal.git
   cd vmportal
   ```

2. **Create and activate Conda environment**

   ```bash
   conda env create -f ops/environment.yml -n vmportal
   conda activate vmportal
   ```

3. **Run migrations and start server**

   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```

4. Open [http://localhost:8000](http://localhost:8000) in your browser.

---

## 🌐 Deployment to a New Server

The repository includes an **automated bootstrap script** to deploy everything in one go.

**Requirements:**

* Ubuntu/Debian server
* `git` installed
* User with `sudo` privileges

### Steps:

```bash
# 1) Clone repo
git clone https://github.com/<your-username>/vmportal.git
cd vmportal

# 2) Make script executable and run
chmod +x ops/bootstrap.sh
bash ops/bootstrap.sh
```

The script will:

* Install required system packages
* Install Conda (Miniforge) if missing
* Create a Conda environment from `ops/environment.yml`
* Install Gunicorn and Python dependencies
* Run Django migrations and collect static files
* Configure and enable a `systemd` service for Gunicorn
* Configure and reload Nginx

---

## ⚙️ Environment Variables

Create a `.env` file at the project root (based on `ops/.env.example`):

```ini
DJANGO_SECRET_KEY=change-me
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=yourdomain.com,localhost
```

---

## 🛠️ Managing the Service

```bash
sudo systemctl restart gunicorn-vmportal    # Restart app
sudo systemctl status gunicorn-vmportal     # Check status
sudo journalctl -u gunicorn-vmportal -f     # View logs
```

---

## 📜 License

MIT License
