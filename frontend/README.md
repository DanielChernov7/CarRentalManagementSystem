# Car Rental Management System - Frontend

React + TypeScript + Tailwind CSS frontend with shadcn/ui components.

## Quick Start

1. Install dependencies:
```bash
npm install
```

2. Install additional required package:
```bash
npm install tailwindcss-animate
```

3. Run development server:
```bash
npm run dev
```

Visit http://localhost:5173

## Project Structure

```
src/
├── api/             # API integration
│   ├── axios.ts     # Axios instance with interceptors
│   └── services.ts  # API service functions
├── components/      # Reusable components
│   ├── ui/          # shadcn/ui base components
│   ├── Layout.tsx
│   └── ProtectedRoute.tsx
├── context/         # React context
│   └── AuthContext.tsx
├── pages/           # Page components
│   ├── Home.tsx
│   ├── Login.tsx
│   ├── Register.tsx
│   ├── BrowseVehicles.tsx
│   ├── NewReservation.tsx
│   ├── Dashboard.tsx
│   ├── AdminDashboard.tsx
│   └── ClerkDashboard.tsx
├── types/           # TypeScript type definitions
│   └── index.ts
├── lib/             # Utilities
│   └── utils.ts
├── App.tsx          # Main application
├── main.tsx         # Entry point
└── index.css        # Global styles
```

## Features

### Customer Features
- Browse available vehicles by date range
- Filter vehicles by location and type
- Real-time price calculation
- Create and manage reservations
- Payment processing
- Reservation history

### Admin Features
- Manage vehicles (CRUD)
- Manage locations (CRUD)
- Manage rate plans (CRUD)
- View all system data

### Clerk Features
- View pending reservations
- Process vehicle pickups (activate reservations)
- Process vehicle returns (complete reservations)
- Manage inspections and damage reports

## Authentication

The app uses JWT tokens stored in localStorage. Protected routes automatically redirect to login if not authenticated.

Role-based routing ensures users can only access features appropriate to their role.

## API Integration

All API calls go through the centralized `api/services.ts` file, which provides type-safe functions for interacting with the backend.

The Axios instance includes automatic token injection and error handling.

## Building for Production

```bash
npm run build
```

The build output will be in the `dist` directory.
