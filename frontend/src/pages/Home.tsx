import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '@/context/AuthContext';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Car, Calendar, Shield, DollarSign } from 'lucide-react';

export const Home: React.FC = () => {
  const { isAuthenticated } = useAuth();

  return (
    <div>
      <div className="bg-gradient-to-r from-blue-600 to-blue-800 text-white py-20">
        <div className="container mx-auto px-4 text-center">
          <h1 className="text-5xl font-bold mb-4">Welcome to Car Rental System</h1>
          <p className="text-xl mb-8">Find the perfect vehicle for your journey</p>
          {isAuthenticated ? (
            <Link to="/browse">
              <Button size="lg" variant="secondary">
                Browse Vehicles
              </Button>
            </Link>
          ) : (
            <div className="flex gap-4 justify-center">
              <Link to="/register">
                <Button size="lg" variant="secondary">
                  Get Started
                </Button>
              </Link>
              <Link to="/login">
                <Button size="lg" variant="outline" className="text-white border-white hover:bg-white hover:text-blue-800">
                  Login
                </Button>
              </Link>
            </div>
          )}
        </div>
      </div>

      <div className="container mx-auto px-4 py-16">
        <h2 className="text-3xl font-bold text-center mb-12">Why Choose Us?</h2>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <Card>
            <CardHeader>
              <Car className="h-12 w-12 text-primary mb-2" />
              <CardTitle>Wide Selection</CardTitle>
            </CardHeader>
            <CardContent>
              <CardDescription>
                Choose from sedans, SUVs, trucks, vans, and luxury vehicles
              </CardDescription>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <Calendar className="h-12 w-12 text-primary mb-2" />
              <CardTitle>Flexible Booking</CardTitle>
            </CardHeader>
            <CardContent>
              <CardDescription>
                Easy online reservation with flexible pickup and dropoff locations
              </CardDescription>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <Shield className="h-12 w-12 text-primary mb-2" />
              <CardTitle>Insurance Options</CardTitle>
            </CardHeader>
            <CardContent>
              <CardDescription>
                Optional insurance coverage for peace of mind during your rental
              </CardDescription>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <DollarSign className="h-12 w-12 text-primary mb-2" />
              <CardTitle>Best Rates</CardTitle>
            </CardHeader>
            <CardContent>
              <CardDescription>
                Competitive pricing with multiple rate plans and discounts
              </CardDescription>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};
