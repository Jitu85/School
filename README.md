# Smart School Management System

**Designed & Developed by ABHIJIT KUMAR MISRA**

A comprehensive school management system built with:
- **Frontend:** Next.js with TypeScript
- **Backend:** Django with Django REST Framework
- **Database:** PostgreSQL
- **DevOps:** Docker Compose, GitHub Actions

This system replaces scattered paper registers, manual fee books, attendance sheets, and spreadsheets with one integrated system for efficient school operations management.

## Phases of Development

1. **Phase 0:** Foundation and product setup
2. **Phase 1:** Master data, admissions and student lifecycle
3. **Phase 2:** Attendance, registers and daily operations
... (continues as per implementation plan)

## Deployment Status & Progress

### Completed
- [x] Initialized Git repository and created initial commit on the `main` branch.
- [x] Linked and pushed codebase to remote GitHub repository: `https://github.com/Jitu85/School.git`.
- [x] Hardened Django backend settings for production-grade hosting (added WhiteNoise, Gunicorn, dj-database-url, session validation, and CORS/CSRF regexes for Vercel).
- [x] Verified and compiled production builds successfully for both Django backend and Next.js frontend.
- [x] Created serverless PostgreSQL instance on Neon.tech and ran all database migrations to initialize tables.
- [x] Pre-created administrator credentials in the Neon database.

### To Be Done (Next Steps)
- [ ] Connect the remote codebase to a live hosting server (via Render or Hugging Face Spaces for the backend, and Vercel for the frontend).
- [ ] Bind environment variables (e.g. `DATABASE_URL`, `SECRET_KEY`, `DEBUG`, `NEXT_PUBLIC_API_URL`).
- [ ] Conduct final live routing tests.

## Project Development Progress

### Completed (Foundation & Admissions - Phases 0 & 1)
- [x] **API Route Mapping:** Corrected core API endpoint mounting in `backend/config/urls.py` under `/api/v1/core/`.
- [x] **Multi-Tenancy:** Implemented dynamic query filtering by `school_id` and `campus_id` for enquiries and application records.
- [x] **API Security:** Enforced authenticated controls (`IsAuthenticated`) on list/edit views, leaving only public form creation open.
- [x] **Authentication Flow:** Migrated from JWT to secure `SessionAuthentication` with SameSite=Lax and HttpOnly cookies.
- [x] **Schema Normalization:** Normalized parent/guardian models, moving from flat fields on `Application` to dynamic relational references on `Guardian`.
- [x] **Concurrency Safety:** Locked `NumberSequence` rows using database-level `select_for_update` transaction locks to prevent duplicate application IDs.
- [x] **Frontend Navigation:** Added user login panels at `/login` and routing setups for public enquiries and application forms.
- [x] **Database Seeding:** Created seeds to automatically verify and provision default school instances.

### To Be Done (Future Modules - Phases 2 to 5)
- [ ] **Phase 2 (Attendance & Daily Operations):** Daily grid markings, leave approval pipelines, class registers.
- [ ] **Phase 3 (Fee & Financials):** Invoices, dynamic fee heads, concession allocation rules, cashbook/bank ledger journals.
- [ ] **Phase 4 (Exams & Results):** Evaluation spreadsheets, grade boundaries, and QR-verifiable print layouts.
- [ ] **Phase 5 (Library, Stock, & Payroll):** Book inventory records, purchase flows, asset disposal history, and staff payroll slips.

## Database & Deployment Details

### Database (Neon PostgreSQL)
* **Provider:** Neon Serverless Postgres
* **Connection String:** `postgresql://neondb_owner:npg_7zwypsIP4KTW@ep-lucky-unit-aox8djce.c-2.ap-southeast-1.aws.neon.tech/neondb?sslmode=require`
* **Admin Superuser Credentials (Django Admin):**
  * **Email / Login:** `admin@school.com`
  * **Username:** `admin`
  * **Password:** `adminpassword`

### Backend Deployment Options

#### Option A: Render (Requires Card Verification)
1. Link the GitHub repository `https://github.com/Jitu85/School.git` to a new Web Service on Render.
2. Configure settings:
   * **Root Directory:** `backend`
   * **Build Command:** `pip install -r requirements.txt && python manage.py collectstatic --no-input`
   * **Start Command:** `gunicorn config.wsgi:application`
3. Environment Secrets:
   * `DATABASE_URL` = (Neon database connection string)
   * `DEBUG` = `False`
   * `SECRET_KEY` = (A secure random string)

#### Option B: Hugging Face Spaces (Docker - Card-Free)
1. Create a Docker Space (Blank template, CPU Basic, Public) on Hugging Face named `school-backend`.
2. Add secrets under **Settings** -> **Variables and Secrets**:
   * `DATABASE_URL` = (Neon database connection string)
   * `SECRET_KEY` = (A secure random string)
   * `DEBUG` = `False`
3. Push the `backend` subdirectory to Hugging Face:
   ```bash
   git remote add hf https://huggingface.co/spaces/YOUR_HF_USERNAME/school-backend
   git subtree push --prefix backend hf main
   ```

## Getting Started

See [DEVELOPMENT.md](DEVELOPMENT.md) for setup instructions.

## License

© 2026 ABHIJIT KUMAR MISRA. All rights reserved.