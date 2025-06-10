# 3D Printing Marketplace

This repository contains the full source code and configuration for a 3D-printing marketplace web application. The platform connects providers (3D-printer owners) and customers (who request models to be printed).

## Directory Structure.

```
3dprint-marketplace/
├─ backend/
│  ├─ app/
│  │   ├─ __init__.py
│  │   ├─ models.py
│  │   ├─ routes.py
│  │   ├─ config.py
│  ├─ requirements.txt
│  ├─ Dockerfile
│  └─ .env.example
│
├─ frontend/
│  ├─ public/
│  │   └─ index.html
│  ├─ src/
│  │   ├─ assets/
│  │   ├─ components/
│  │   │   ├─ Navbar.vue
│  │   │   └─ ProviderCard.vue
│  │   ├─ pages/
│  │   │   ├─ Home.vue
│  │   │   ├─ Login.vue
│  │   │   ├─ Register.vue
│  │   │   ├─ BrowseProviders.vue
│  │   │   ├─ ProviderProfile.vue
│  │   │   ├─ MyJobs.vue
│  │   │   ├─ AssignedJobs.vue
│  │   │   ├─ JobDetail.vue
│  │   │   ├─ JobRequestForm.vue
│  │   │   ├─ MessageWindow.vue
│  │   │   └─ ReviewForm.vue
│  │   ├─ router/
│  │   │   └─ index.js
│  │   ├─ store/
│  │   │   └─ index.js
│  │   └─ App.vue
│  ├─ package.json
│  ├─ vite.config.js
│  ├─ tailwind.config.js
│  ├─ postcss.config.js
│  └─ .env.example
│
├─ nginx/
│  ├─ default.conf
│  └─ Dockerfile
│
├─ docker-compose.yml
└─ README.md
```

## Installation Instructions

1. **Clone the repository**  
   ```bash
   git clone <this_repo_url>
   cd 3dprint-marketplace
   ```

2. **Backend Setup**  
   - Copy `.env.example` to `.env` in `backend/` and fill in your values (e.g., database credentials).
   - Build and run Docker containers:
     ```bash
     docker-compose up --build
     ```
   - In a new terminal, run database migrations:
     ```bash
     docker-compose exec backend flask db upgrade
     ```
   - Seed optional test data if desired:
     ```bash
     docker-compose exec backend python seed.py
     ```

3. **Frontend Setup**  
   - Frontend is built and served by its Docker container; no additional steps needed after `docker-compose up`.
   - Access the site at `http://localhost:3000`.

4. **Nginx (Optional)**  
   - Use the `nginx` service to serve both frontend and backend under a single domain on port 80.

5. **Stopping Services**  
   ```bash
   docker-compose down
   ```

For more details on development and deployment, refer to each subdirectory's README.

Enjoy your 3D-printing marketplace!
