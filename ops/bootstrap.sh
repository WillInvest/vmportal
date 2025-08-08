#!/usr/bin/env bash
set -euo pipefail

APP_USER=${APP_USER:-vmportal}
APP_DIR=${APP_DIR:-/home/${APP_USER}/vmportal}
ENV_NAME=${ENV_NAME:-vmportal}

# 0) System deps
sudo apt-get update
sudo apt-get install -y nginx curl git

# 1) Conda (Miniforge) if missing
if ! command -v conda >/dev/null 2>&1; then
  curl -fsSL https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh -o /tmp/mf.sh
  bash /tmp/mf.sh -b -p "$HOME/miniforge3"
  eval "$("$HOME/miniforge3/bin/conda" shell.bash hook)"
fi
eval "$(conda shell.bash hook)"

# 2) Create env
conda env create -f "${APP_DIR}/ops/environment.yml" -n "${ENV_NAME}" || true
conda activate "${ENV_NAME}"
pip install --no-input gunicorn python-dotenv

# 3) App settings
cp -n "${APP_DIR}/ops/.env.example" "${APP_DIR}/.env" || true

# 4) Django prep
cd "${APP_DIR}"
python manage.py migrate
python manage.py collectstatic --noinput

# 5) Systemd service
sudo install -m 644 "${APP_DIR}/ops/gunicorn-vmportal.service" /etc/systemd/system/gunicorn-vmportal.service
sudo systemctl daemon-reload
sudo systemctl enable gunicorn-vmportal
sudo systemctl restart gunicorn-vmportal

# 6) Nginx site
sudo install -m 644 "${APP_DIR}/ops/nginx.vmportal.conf" /etc/nginx/sites-available/vmportal
sudo ln -sf /etc/nginx/sites-available/vmportal /etc/nginx/sites-enabled/vmportal
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl reload nginx

echo "✅ Bootstrap done. Now edit ${APP_DIR}/.env (DJANGO_ALLOWED_HOSTS, DJANGO_SECRET_KEY), then: sudo systemctl restart gunicorn-vmportal"
