import os
content = """# Django Settings
SECRET_KEY=***
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Settings (use localhost for local dev without Docker)
DB_NAME=school_db
DB_USER=postgres
DB_PASSWORD=jitu
DB_HOST=localhost
DB_PORT=5432

# Redis Settings
REDIS_URL=redis://localhost:***@school.local

# File Storage
USE_S3=False
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=***
AWS_S3_REGION_NAME=

# Payment Gateway
PAYMENT_GATEWAY_KEY=
PAYMENT_GATEWAY_SECRET=*** Error Tracking (Sentry)
SENTRY_DSN=

# Admin Settings
ADMIN_URL=admin/
"""
with open('.env', 'w') as f:
    f.write(content)