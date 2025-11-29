import React, { useState, useEffect } from 'react';
import { reservationsAPI } from '@/api/services';
import type { Reservation } from '@/types';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Alert, AlertDescription } from '@/components/ui/alert';

export const ClerkDashboard: React.FC = () => {
  const [reservations, setReservations] = useState<Reservation[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<'all' | 'confirmed' | 'active'>('confirmed');

  useEffect(() => {
    loadReservations();
  }, []);

  const loadReservations = async () => {
    try {
      const data = await reservationsAPI.getAll();
      setReservations(data);
    } catch (error) {
      console.error('Failed to load reservations:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleActivate = async (id: number) => {
    try {
      await reservationsAPI.activate(id);
      loadReservations();
      alert('Reservation activated successfully');
    } catch (error: any) {
      alert(error.response?.data?.detail || 'Failed to activate reservation');
    }
  };

  const handleComplete = async (id: number) => {
    try {
      await reservationsAPI.complete(id);
      loadReservations();
      alert('Reservation completed successfully');
    } catch (error: any) {
      alert(error.response?.data?.detail || 'Failed to complete reservation');
    }
  };

  const filteredReservations = reservations.filter((r) => {
    if (filter === 'all') return true;
    return r.status === filter;
  });

  return (
    <div className="container mx-auto py-8 px-4">
      <h1 className="text-3xl font-bold mb-8">Clerk Dashboard</h1>

      <div className="flex gap-4 mb-6">
        <Button
          variant={filter === 'all' ? 'default' : 'outline'}
          onClick={() => setFilter('all')}
        >
          All
        </Button>
        <Button
          variant={filter === 'confirmed' ? 'default' : 'outline'}
          onClick={() => setFilter('confirmed')}
        >
          Ready for Pickup
        </Button>
        <Button
          variant={filter === 'active' ? 'default' : 'outline'}
          onClick={() => setFilter('active')}
        >
          Active Rentals
        </Button>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Manage Reservations</CardTitle>
          <CardDescription>Process vehicle pickups and returns</CardDescription>
        </CardHeader>
        <CardContent>
          {loading ? (
            <div className="text-center py-8">Loading reservations...</div>
          ) : filteredReservations.length === 0 ? (
            <Alert>
              <AlertDescription>No reservations found for this filter.</AlertDescription>
            </Alert>
          ) : (
            <div className="space-y-4">
              {filteredReservations.map((reservation) => (
                <div
                  key={reservation.id}
                  className="border rounded-lg p-4 hover:shadow-md transition-shadow"
                >
                  <div className="flex justify-between items-start">
                    <div className="space-y-2">
                      <div className="flex items-center gap-2">
                        <h3 className="font-semibold">Reservation #{reservation.id}</h3>
                        <span
                          className={`px-2 py-1 rounded-full text-xs font-semibold ${
                            reservation.status === 'confirmed'
                              ? 'bg-blue-100 text-blue-800'
                              : reservation.status === 'active'
                              ? 'bg-green-100 text-green-800'
                              : 'bg-gray-100 text-gray-800'
                          }`}
                        >
                          {reservation.status.toUpperCase()}
                        </span>
                      </div>
                      <div className="text-sm text-gray-600 space-y-1">
                        <p>
                          <span className="font-medium">Customer ID:</span> {reservation.customer_id}
                        </p>
                        <p>
                          <span className="font-medium">Vehicle ID:</span> {reservation.vehicle_id}
                        </p>
                        <p>
                          <span className="font-medium">Dates:</span>{' '}
                          {new Date(reservation.start_date).toLocaleDateString()} -{' '}
                          {new Date(reservation.end_date).toLocaleDateString()}
                        </p>
                        <p>
                          <span className="font-medium">Total:</span> $
                          {reservation.total_price.toFixed(2)}
                        </p>
                      </div>
                    </div>
                    <div className="flex gap-2">
                      {reservation.status === 'confirmed' && (
                        <Button onClick={() => handleActivate(reservation.id)}>
                          Process Pickup
                        </Button>
                      )}
                      {reservation.status === 'active' && (
                        <Button onClick={() => handleComplete(reservation.id)}>
                          Process Return
                        </Button>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};
