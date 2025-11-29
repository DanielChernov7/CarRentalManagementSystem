import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import MainLayout from './layouts/MainLayout';
import HomePage from './pages/HomePage';
import CarsPage from './pages/CarsPage';
import RentalsPage from './pages/RentalsPage';
import LoginPage from './pages/LoginPage';
import { ROUTES } from './constants';

// Create a query client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
      retry: 1,
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path={ROUTES.HOME} element={<MainLayout />}>
            <Route index element={<HomePage />} />
            <Route path={ROUTES.CARS} element={<CarsPage />} />
            <Route path={ROUTES.RENTALS} element={<RentalsPage />} />
            <Route path={ROUTES.LOGIN} element={<LoginPage />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;
