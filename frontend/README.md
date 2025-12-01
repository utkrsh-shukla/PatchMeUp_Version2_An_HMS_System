# Hospital Management System V2 - Frontend

VueJS SPA frontend for Hospital Management System with role-based routing and JWT authentication.

## Features

- **Vue 3** with Composition API
- **Vue Router** with authentication guards
- **Vuex** for state management
- **Axios** with JWT token interceptors
- **Bootstrap 5** for styling
- **Vite** for fast development

## Project Structure

```
src/
├── api/                  # API service layer
│   ├── axios.js         # Configured Axios instance
│   ├── auth.js          # Auth API
│   ├── admin.js         # Admin API
│   ├── doctor.js        # Doctor API
│   └── patient.js       # Patient API
├── components/          # Reusable components
│   ├── Navbar.vue
│   ├── Footer.vue
│   ├── StatCard.vue
│   └── LoadingSpinner.vue
├── router/              # Vue Router config
│   └── index.js
├── store/               # Vuex store
│   ├── index.js
│   └── modules/
│       ├── auth.js
│       ├── admin.js
│       ├── doctor.js
│       └── patient.js
├── views/               # Page components
│   ├── Home.vue
│   ├── auth/
│   ├── admin/
│   ├── doctor/
│   └── patient/
├── assets/
│   └── main.css         # Custom styles
├── App.vue              # Root component
└── main.js              # App entry point
```

## Setup

1. **Install dependencies:**
```bash
cd v2/frontend
npm install
```

2. **Start development server:**
```bash
npm run dev
```

Frontend will be available at `http://localhost:8080`

3. **Make sure backend API is running** at `http://localhost:5000`

## Build for Production

```bash
npm run build
```

## Default URLs

- **Home**: http://localhost:8080
- **Login**: http://localhost:8080/login
- **Register**: http://localhost:8080/register
- **Admin Dashboard**: http://localhost:8080/admin/dashboard
- **Doctor Dashboard**: http://localhost:8080/doctor/dashboard
- **Patient Dashboard**: http://localhost:8080/patient/dashboard

## Authentication

JWT tokens are stored in localStorage and automatically included in API requests via Axios interceptors.

## Route Guards

- `/admin/*` - Requires admin role
- `/doctor/*` - Requires doctor role
- `/patient/*` - Requires patient role
- `/login`, `/register` - Guest only (redirects if authenticated)

## API Integration

All API calls go through the service layer in `src/api/`. The Axios instance automatically:
- Adds JWT token to headers
- Handles token refresh on 401
- Redirects to login on auth failure

## Color Theme

- Primary: #DC143C (Crimson Red)
- Secondary: #F5F5DC (Beige)
- Uses custom CSS variables for consistency
