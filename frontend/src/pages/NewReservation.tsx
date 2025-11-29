import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { reservationsAPI, ratePlansAPI, locationsAPI, paymentsAPI } from '@/api/services';
import type { RatePlan, Location, PriceCalculation } from '@/types';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select } from '@/components/ui/select';
import { Alert, AlertDescription } from '@/components/ui/alert';

export const NewReservation: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { vehicle, startDate: initialStartDate, endDate: initialEndDate, locationId: initialLocationId } = location.state || {};

  const [ratePlans, setRatePlans] = useState<RatePlan[]>([]);
  const [locations, setLocations] = useState<Location[]>([]);
  const [formData, setFormData] = useState({
    vehicleId: vehicle?.id || '',
    ratePlanId: '',
    pickupLocationId: initialLocationId || '',
    dropoffLocationId: initialLocationId || '',
    startDate: initialStartDate || '',
    endDate: initialEndDate || '',
    includeInsurance: false,
    specialRequests: '',
  });
  const [priceCalculation, setPriceCalculation] = useState<PriceCalculation | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    loadData();
  }, []);

  useEffect(() => {
    if (formData.vehicleId && formData.ratePlanId && formData.startDate && formData.endDate) {
      calculatePrice();
    }
  }, [formData]);

  const loadData = async () => {
    try {
      const [ratePlansData, locationsData] = await Promise.all([
        ratePlansAPI.getAll(),
        locationsAPI.getAll(),
      ]);
      setRatePlans(ratePlansData.filter(rp => rp.is_active));
      setLocations(locationsData);

      if (ratePlansData.length > 0) {
        setFormData(prev => ({ ...prev, ratePlanId: ratePlansData[0].id.toString() }));
      }
    } catch (error) {
      console.error('Failed to load data:', error);
    }
  };

  const calculatePrice = async () => {
    try {
      const price = await reservationsAPI.calculatePrice({
        vehicle_id: parseInt(formData.vehicleId),
        rate_plan_id: parseInt(formData.ratePlanId),
        pickup_location_id: parseInt(formData.pickupLocationId),
        dropoff_location_id: parseInt(formData.dropoffLocationId),
        start_date: formData.startDate,
        end_date: formData.endDate,
        include_insurance: formData.includeInsurance,
      });
      setPriceCalculation(price);
      setError('');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to calculate price');
      setPriceCalculation(null);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const reservation = await reservationsAPI.create({
        vehicle_id: parseInt(formData.vehicleId),
        rate_plan_id: parseInt(formData.ratePlanId),
        pickup_location_id: parseInt(formData.pickupLocationId),
        dropoff_location_id: parseInt(formData.dropoffLocationId),
        start_date: formData.startDate,
        end_date: formData.endDate,
        include_insurance: formData.includeInsurance,
        special_requests: formData.specialRequests || undefined,
      });

      // Process payment
      if (priceCalculation) {
        await paymentsAPI.create({
          reservation_id: reservation.id,
          amount: priceCalculation.total_price,
          payment_method: 'credit_card',
        });
      }

      navigate('/dashboard');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to create reservation');
    } finally {
      setLoading(false);
    }
  };

  if (!vehicle) {
    return (
      <div className="container mx-auto py-8 px-4">
        <Alert variant="destructive">
          <AlertDescription>No vehicle selected. Please browse vehicles first.</AlertDescription>
        </Alert>
        <Button onClick={() => navigate('/browse')} className="mt-4">
          Browse Vehicles
        </Button>
      </div>
    );
  }

  return (
    <div className="container mx-auto py-8 px-4 max-w-4xl">
      <h1 className="text-3xl font-bold mb-8">Create Reservation</h1>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Vehicle Details</CardTitle>
          </CardHeader>
          <CardContent className="space-y-2">
            <p><span className="font-semibold">Vehicle:</span> {vehicle.year} {vehicle.make} {vehicle.model}</p>
            <p><span className="font-semibold">Type:</span> {vehicle.vehicle_type}</p>
            <p><span className="font-semibold">Daily Rate:</span> ${vehicle.daily_rate.toFixed(2)}</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Reservation Form</CardTitle>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              {error && (
                <Alert variant="destructive">
                  <AlertDescription>{error}</AlertDescription>
                </Alert>
              )}

              <div className="space-y-2">
                <Label htmlFor="ratePlan">Rate Plan</Label>
                <Select
                  id="ratePlan"
                  value={formData.ratePlanId}
                  onChange={(e) => setFormData({ ...formData, ratePlanId: e.target.value })}
                  required
                >
                  {ratePlans.map((plan) => (
                    <option key={plan.id} value={plan.id}>
                      {plan.name} ({plan.discount_percentage}% discount)
                    </option>
                  ))}
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="pickupLocation">Pickup Location</Label>
                <Select
                  id="pickupLocation"
                  value={formData.pickupLocationId}
                  onChange={(e) => setFormData({ ...formData, pickupLocationId: e.target.value })}
                  required
                >
                  <option value="">Select location</option>
                  {locations.map((loc) => (
                    <option key={loc.id} value={loc.id}>
                      {loc.name}
                    </option>
                  ))}
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="dropoffLocation">Dropoff Location</Label>
                <Select
                  id="dropoffLocation"
                  value={formData.dropoffLocationId}
                  onChange={(e) => setFormData({ ...formData, dropoffLocationId: e.target.value })}
                  required
                >
                  <option value="">Select location</option>
                  {locations.map((loc) => (
                    <option key={loc.id} value={loc.id}>
                      {loc.name}
                    </option>
                  ))}
                </Select>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="startDate">Start Date</Label>
                  <Input
                    id="startDate"
                    type="date"
                    value={formData.startDate}
                    onChange={(e) => setFormData({ ...formData, startDate: e.target.value })}
                    min={new Date().toISOString().split('T')[0]}
                    required
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="endDate">End Date</Label>
                  <Input
                    id="endDate"
                    type="date"
                    value={formData.endDate}
                    onChange={(e) => setFormData({ ...formData, endDate: e.target.value })}
                    min={formData.startDate}
                    required
                  />
                </div>
              </div>

              <div className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  id="includeInsurance"
                  checked={formData.includeInsurance}
                  onChange={(e) => setFormData({ ...formData, includeInsurance: e.target.checked })}
                  className="rounded"
                />
                <Label htmlFor="includeInsurance">Include Insurance</Label>
              </div>

              <div className="space-y-2">
                <Label htmlFor="specialRequests">Special Requests (optional)</Label>
                <Input
                  id="specialRequests"
                  value={formData.specialRequests}
                  onChange={(e) => setFormData({ ...formData, specialRequests: e.target.value })}
                  placeholder="Any special requirements..."
                />
              </div>

              {priceCalculation && (
                <Card>
                  <CardHeader>
                    <CardTitle className="text-lg">Price Breakdown</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-1 text-sm">
                    <div className="flex justify-between">
                      <span>Base Price ({priceCalculation.rental_days} days):</span>
                      <span>${priceCalculation.base_price.toFixed(2)}</span>
                    </div>
                    {priceCalculation.discount_amount > 0 && (
                      <div className="flex justify-between text-green-600">
                        <span>Discount:</span>
                        <span>-${priceCalculation.discount_amount.toFixed(2)}</span>
                      </div>
                    )}
                    {priceCalculation.one_way_fee_amount > 0 && (
                      <div className="flex justify-between">
                        <span>One-Way Fee:</span>
                        <span>${priceCalculation.one_way_fee_amount.toFixed(2)}</span>
                      </div>
                    )}
                    {priceCalculation.insurance_amount > 0 && (
                      <div className="flex justify-between">
                        <span>Insurance:</span>
                        <span>${priceCalculation.insurance_amount.toFixed(2)}</span>
                      </div>
                    )}
                    <div className="flex justify-between font-bold text-lg pt-2 border-t">
                      <span>Total:</span>
                      <span>${priceCalculation.total_price.toFixed(2)}</span>
                    </div>
                  </CardContent>
                </Card>
              )}

              <Button type="submit" className="w-full" disabled={loading || !priceCalculation}>
                {loading ? 'Processing...' : 'Confirm & Pay'}
              </Button>
            </form>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};
