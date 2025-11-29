import React, { useState, useEffect } from 'react';
import { useAuth } from '@/context/AuthContext';
import { reservationsAPI } from '@/api/services';
import type { Reservation } from '@/types';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Alert, AlertDescription } from '@/components/ui/alert';

export const Dashboard: React.FC = () => {
  const { user } = useAuth();
  const [reservations, setReservations] = useState<Reservation[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadReservations();
  }, []);

  const loadReservations = async () => {
    try {
      const data = await reservationsAPI.getMy();
      setReservations(data);
    } catch (error) {
      console.error('Failed to load reservations:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = async (id: number) => {
    if (!confirm('Are you sure you want to cancel this reservation?')) {
      return;
    }

    try {
      await reservationsAPI.cancel(id);
      loadReservations();
    } catch (error: any) {
      alert(error.response?.data?.detail || 'Failed to cancel reservation');
    }
  };

  const getStatusBadge = (status: string) => {
    const colors: Record<string, string> = {
      pending: 'bg-yellow-100 text-yellow-800',
      confirmed: 'bg-blue-100 text-blue-800',
      active: 'bg-green-100 text-green-800',
      completed: 'bg-gray-100 text-gray-800',
      cancelled: 'bg-red-100 text-red-800',
    };
    return (
      <span className={`px-2 py-1 rounded-full text-xs font-semibold ${colors[status] || ''}`}>
        {status.toUpperCase()}
      </span>
    );
  };

  return (
    <div className="container mx-auto py-8 px-4">
      <div className="mb-8">
        <h1 className="text-3xl font-bold">Customer Dashboard</h1>
        <p className="text-gray-600 mt-2">Welcome back, {user?.full_name}!</p>
      </div>

      <Card className="mb-8">
        <CardHeader>
          <CardTitle>My Reservations</CardTitle>
          <CardDescription>View and manage your vehicle reservations</CardDescription>
        </CardHeader>
        <CardContent>
          {loading ? (
            <div className="text-center py-8">Loading reservations...</div>
          ) : reservations.length === 0 ? (
            <Alert>
              <AlertDescription>
                You don't have any reservations yet. Browse vehicles to create one!
              </AlertDescription>
            </Alert>
          ) : (
            <div className="space-y-4">
              {reservations.map((reservation) => (
                <div
                  key={reservation.id}
                  className="border rounded-lg p-4 hover:shadow-md transition-shadow"
                >
                  <div className="flex justify-between items-start">
                    <div className="space-y-2">
                      <div className="flex items-center gap-2">
                        <h3 className="font-semibold">Reservation #{reservation.id}</h3>
                        {getStatusBadge(reservation.status)}
                      </div>
                      <div className="text-sm text-gray-600 space-y-1">
                        <p>
                          <span className="font-medium">Dates:</span>{' '}
                          {new Date(reservation.start_date).toLocaleDateString()} -{' '}
                          {new Date(reservation.end_date).toLocaleDateString()}
                        </p>
                        <p>
                          <span className="font-medium">Total Price:</span> $
                          {reservation.total_price.toFixed(2)}
                        </p>
                        {reservation.include_insurance && (
                          <p className="text-green-600">✓ Insurance Included</p>
                        )}
                      </div>
                    </div>
                    <div className="flex gap-2">
                      {(reservation.status === 'pending' || reservation.status === 'confirmed') && (
                        <Button
                          variant="destructive"
                          size="sm"
                          onClick={() => handleCancel(reservation.id)}
                        >
                          Cancel
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
