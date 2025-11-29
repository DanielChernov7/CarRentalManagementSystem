import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '@/context/AuthContext';
import { Button } from '@/components/ui/button';
import { Car, LogOut, User } from 'lucide-react';

export const Layout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { user, logout, isAuthenticated } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm border-b">
        <div className="container mx-auto px-4">
          <div className="flex justify-between items-center h-16">
            <Link to="/" className="flex items-center gap-2 text-xl font-bold text-primary">
              <Car className="h-6 w-6" />
              Car Rental System
            </Link>

            <div className="flex items-center gap-4">
              {isAuthenticated ? (
                <>
                  {user?.role === 'customer' && (
                    <>
                      <Link to="/browse">
                        <Button variant="ghost">Browse Vehicles</Button>
                      </Link>
                      <Link to="/dashboard">
                        <Button variant="ghost">My Reservations</Button>
                      </Link>
                    </>
                  )}
                  {user?.role === 'admin' && (
                    <Link to="/admin">
                      <Button variant="ghost">Admin Panel</Button>
                    </Link>
                  )}
                  {user?.role === 'clerk' && (
                    <Link to="/clerk">
                      <Button variant="ghost">Clerk Panel</Button>
                    </Link>
                  )}
                  <div className="flex items-center gap-2 text-sm text-gray-600">
                    <User className="h-4 w-4" />
                    <span>{user?.full_name}</span>
                  </div>
                  <Button variant="outline" size="sm" onClick={handleLogout}>
                    <LogOut className="h-4 w-4 mr-2" />
                    Logout
                  </Button>
                </>
              ) : (
                <>
                  <Link to="/login">
                    <Button variant="ghost">Login</Button>
                  </Link>
                  <Link to="/register">
                    <Button>Register</Button>
                  </Link>
                </>
              )}
            </div>
          </div>
        </div>
      </nav>

      <main>{children}</main>

      <footer className="bg-white border-t mt-auto">
        <div className="container mx-auto px-4 py-6 text-center text-sm text-gray-600">
          <p>&copy; 2025 Car Rental Management System. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
};
