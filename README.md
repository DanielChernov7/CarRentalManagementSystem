# Car Rental Management System

A modern, full-featured car rental management system built with React, TypeScript, and Vite.

## Features

- **Modern Tech Stack**: Built with React 19, TypeScript, and Vite
- **Responsive Design**: Tailwind CSS for beautiful, mobile-first UI
- **Type Safety**: Full TypeScript support with comprehensive type definitions
- **State Management**: Zustand for efficient, lightweight state management
- **Data Fetching**: TanStack Query (React Query) for server state management
- **Routing**: React Router v7 for seamless navigation
- **Form Handling**: React Hook Form with Zod validation
- **API Integration**: Axios with interceptors for authentication

## Project Structure

```
src/
├── components/        # Reusable UI components
│   ├── Header.tsx
│   └── Footer.tsx
├── pages/            # Page components
│   ├── HomePage.tsx
│   ├── CarsPage.tsx
│   ├── RentalsPage.tsx
│   └── LoginPage.tsx
├── layouts/          # Layout components
│   └── MainLayout.tsx
├── services/         # API services
│   ├── api.ts
│   └── carService.ts
├── store/            # State management
│   └── authStore.ts
├── hooks/            # Custom React hooks
├── types/            # TypeScript type definitions
│   └── index.ts
├── utils/            # Utility functions
│   └── formatters.ts
├── constants/        # Application constants
│   └── index.ts
└── styles/           # Global styles
```

## Getting Started

### Prerequisites

- Node.js (v18 or higher)
- npm or yarn

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd CarRentalManagementSystem
```

2. Install dependencies:
```bash
npm install
```

3. Create environment file:
```bash
cp .env.example .env
```

4. Update the `.env` file with your API configuration:
```env
VITE_API_BASE_URL=http://localhost:3000/api
```

### Development

Start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:5173`

### Building for Production

```bash
npm run build
```

Preview the production build:
```bash
npm run preview
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint
- `npm run lint:fix` - Fix ESLint errors
- `npm run format` - Format code with Prettier
- `npm run format:check` - Check code formatting
- `npm run type-check` - Run TypeScript type checking

## Core Dependencies

- **React** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **React Router** - Client-side routing
- **TanStack Query** - Server state management
- **Zustand** - Global state management
- **Axios** - HTTP client
- **React Hook Form** - Form management
- **Zod** - Schema validation
- **Tailwind CSS** - Utility-first CSS framework

## Type Definitions

The project includes comprehensive TypeScript types for:

- **User**: Customer and admin user types
- **Car**: Vehicle information with categories and status
- **Rental**: Rental bookings and history
- **Payment**: Payment processing and status

See `src/types/index.ts` for full type definitions.

## API Integration

The application uses Axios with interceptors for:

- Automatic authentication token injection
- Centralized error handling
- Request/response transformations

Example API service usage:
```typescript
import { carService } from './services/carService';

const cars = await carService.getAllCars({ page: 1, pageSize: 10 });
```

## State Management

### Authentication State (Zustand)

```typescript
import { useAuthStore } from './store/authStore';

const { user, isAuthenticated, login, logout } = useAuthStore();
```

### Server State (React Query)

```typescript
import { useQuery } from '@tanstack/react-query';
import { carService } from './services/carService';

const { data, isLoading } = useQuery({
  queryKey: ['cars'],
  queryFn: () => carService.getAllCars()
});
```

## Styling

The project uses Tailwind CSS with custom utility classes:

- `.btn-primary` - Primary button styles
- `.btn-secondary` - Secondary button styles
- `.card` - Card container styles

## Contributing

1. Create a feature branch
2. Make your changes
3. Run linting and formatting: `npm run lint:fix && npm run format`
4. Commit your changes
5. Push to the branch
6. Create a Pull Request

## License

MIT
