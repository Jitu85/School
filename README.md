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

## Getting Started

See [DEVELOPMENT.md](DEVELOPMENT.md) for setup instructions.

## License

© 2026 ABHIJIT KUMAR MISRA. All rights reserved.