# School Management System - Faults & Inconsistencies Report

This document records the design inconsistencies, configuration faults, security vulnerabilities, and database schema deviations discovered during a thorough inspection of the project.

---

## 1. High-Impact Issues & Configuration Faults

### 1.1 Inaccessible Core API Endpoints (Broken Routing)
* **Status:** Resolved
* **File:** [backend/config/urls.py](file:///c:/Users/HP/Documents/GitHub/School/backend/config/urls.py)
* **Details:** The master URL configuration has been updated and now correctly mounts the core application routes via `path('api/v1/core/', include('apps.core.urls'))`.
* **Resolution:** Core ViewSets are now fully accessible, enabling programmatic management of schools, campuses, academic years, terms, roles, permissions, settings, audit trails, and attachments.

### 1.2 Missing Multi-Tenancy Controls (`school_id`)
* **Status:** Resolved
* **File:** [backend/apps/admissions/models.py](file:///c:/Users/HP/Documents/GitHub/School/backend/apps/admissions/models.py)
* **Details:** Section 5 of the Master Plan states: *"Every operational table must include school_id and row-level school filtering in backend querysets."*
* **Resolution:** 
  1. `Enquiry` and `Application` models now include `school` (foreign key to `School`) and `campus` (foreign key to `Campus`) fields.
  2. Viewsets filter querysets dynamically by the user's active school membership via `get_queryset()`.
  3. Form submission API entries automatically resolve school defaults or active request contexts in `perform_create()`.

### 1.3 Permissive API Endpoints (`AllowAny` Bypass)
* **Status:** Resolved
* **File:** [backend/apps/admissions/views.py](file:///c:/Users/HP/Documents/GitHub/School/backend/apps/admissions/views.py)
* **Details:** Both `EnquiryViewSet` and `ApplicationViewSet` were configured with `permission_classes = [permissions.AllowAny]`.
* **Resolution:** Enforced `IsAuthenticated` for all list, detail, and editing operations. Left only the public submission (`create` action) as `AllowAny` to support public forms.

### 1.4 Incomplete Admissions Form Submissions (Required School Field Omission)
* **Status:** Resolved
* **File:** [frontend/app/admissions/enquiries/new/page.tsx](file:///c:/Users/HP/Documents/GitHub/School/frontend/app/admissions/enquiries/new/page.tsx), [frontend/app/admissions/applications/new/page.tsx](file:///c:/Users/HP/Documents/GitHub/School/frontend/app/admissions/applications/new/page.tsx)
* **Details:** The backend requires a valid `school_id`, but the frontend forms did not submit school details.
* **Resolution:** Configured the backend serializers to treat `school` and `campus` fields as optional in the payload, resolving and populating them automatically during save using the user context or seeded defaults.

---

## 2. Incomplete Modules & Structural Stubs

### 2.1 16 Backend Applications Are Completely Empty Stubs
* **Status:** Deferred to Subsequent Phases
* **Folder:** [backend/apps/](file:///c:/Users/HP/Documents/GitHub/School/backend/apps)
* **Details:** Local Django apps for student registers, markings, payrolls, etc. contain placeholder comments.
* **Status Note:** These stubs represent deferred modules (Phases 2-5 of the Master Plan). Base database structures for `students` (`Student`, `Guardian`, `StudentGuardian`) have been implemented to support the Admissions relational requirements.

### 2.2 Missing Frontend Modules & Navigation Shell
* **Status:** Deferred to Subsequent Phases
* **Folder:** [frontend/app/](file:///c:/Users/HP/Documents/GitHub/School/frontend/app)
* **Details:** Frontend only contains routes for the Admissions module.
* **Status Note:** Main home cards remain placeholders for subsequent feature integrations.

---

## 3. Security & Authentication Stack Divergence

### 3.1 JWT Token Leakage Vulnerability
* **Status:** Resolved
* **File:** [backend/config/settings.py](file:///c:/Users/HP/Documents/GitHub/School/backend/config/settings.py)
* **Details:** SimpleJWT was configured as the default authenticator, violating the secure HttpOnly cookie requirement.
* **Resolution:** Removed SimpleJWT and configured standard Django `SessionAuthentication`. Configured SameSite (`Lax`) and HttpOnly session cookies in settings.

### 3.2 Unauthenticated Frontend Requests
* **Status:** Resolved
* **Files:** 
  * [frontend/app/admissions/page.tsx](file:///c:/Users/HP/Documents/GitHub/School/frontend/app/admissions/page.tsx)
  * [frontend/app/admissions/enquiries/new/page.tsx](file:///c:/Users/HP/Documents/GitHub/School/frontend/app/admissions/enquiries/new/page.tsx)
  * [frontend/app/admissions/applications/new/page.tsx](file:///c:/Users/HP/Documents/GitHub/School/frontend/app/admissions/applications/new/page.tsx)
* **Resolution:** Added checking for operator authentication status in `AdmissionsDashboard`, a premium login interface at `/login`, and configured `credentials: 'include'` on all fetch operations to pass session cookies.

---

## 4. Database Schema & Modeling Deficiencies

### 4.1 Flat Parent/Guardian Data Model
* **Status:** Resolved
* **File:** [backend/apps/admissions/models.py](file:///c:/Users/HP/Documents/GitHub/School/backend/apps/admissions/models.py)
* **Details:** Parent info was stored as flat fields in the `Application` model.
* **Resolution:** Replaced flat text fields with `ForeignKey` references to the relational `Guardian` model. Implemented lookup-or-create parsing logic in `ApplicationSerializer.create()` to avoid duplicate database entries for sibling enrollments.

### 4.2 Race Conditions in Application Number Generator
* **Status:** Resolved
* **File:** [backend/apps/admissions/models.py](file:///c:/Users/HP/Documents/GitHub/School/backend/apps/admissions/models.py) (save method)
* **Details:** Calculations used `count() + 1` which is prone to concurrency race conditions.
* **Resolution:** Updated `save()` to query the thread-safe `NumberSequence` table using a row-level transaction database lock (`select_for_update`).

### 4.3 Missing Attachment References for Uploads
* **Status:** Resolved
* **File:** [backend/apps/admissions/models.py](file:///c:/Users/HP/Documents/GitHub/School/backend/apps/admissions/models.py)
* **Details:** Uploaded documents were CharFields.
* **Resolution:** Replaced flat fields with foreign key references targeting the `core.Attachment` model.
