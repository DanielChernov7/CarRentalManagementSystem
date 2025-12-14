import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { vehiclesAPI, locationsAPI } from '@/api/services';
import type { Location, VehicleType, VehicleStatus } from '@/types';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Alert, AlertDescription } from '@/components/ui/alert';

const vehicleTypes: VehicleType[] = ['sedan', 'suv', 'truck', 'van', 'luxury', 'economy'];
const vehicleStatuses: VehicleStatus[] = ['available', 'reserved', 'rented', 'maintenance', 'out_of_service'];

export const AddVehicle: React.FC = () => {
  const navigate = useNavigate();
  const [locations, setLocations] = useState<Location[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [formData, setFormData] = useState({
    make: '',
    model: '',
    year: new Date().getFullYear(),
    license_plate: '',
    vin: '',
    color: '',
    vehicle_type: 'sedan' as VehicleType,
    status: 'available' as VehicleStatus,
    mileage: 0,
    daily_rate: 0,
    base_location_id: '',
  });

  useEffect(() => {
    loadLocations();
  }, []);

  const loadLocations = async () => {
    try {
      const data = await locationsAPI.getAll();
      setLocations(data);
      if (data.length > 0) {
        setFormData(prev => ({ ...prev, base_location_id: data[0].id.toString() }));
      }
    } catch (error) {
      console.error('Failed to load locations:', error);
      setError('Failed to load locations');
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    // Validation
    if (!formData.base_location_id) {
      setError('Please select a base location');
      setLoading(false);
      return;
    }

    const payload = {
      make: formData.make,
      model: formData.model,
      year: parseInt(formData.year.toString()),
      license_plate: formData.license_plate,
      vin: formData.vin,
      color: formData.color || undefined,
      vehicle_type: formData.vehicle_type,
      status: formData.status,
      mileage: parseInt(formData.mileage.toString()),
      daily_rate: parseFloat(formData.daily_rate.toString()),
      base_location_id: parseInt(formData.base_location_id),
    };

    console.log('DEBUG: Sending payload:', payload);

    try {
      await vehiclesAPI.create(payload);
      navigate('/admin');
    } catch (err: any) {
      console.error('DEBUG: Error response:', err.response?.data);

      // Handle validation errors from FastAPI
      if (err.response?.data?.detail) {
        if (Array.isArray(err.response.data.detail)) {
          // Pydantic validation errors
          const errorMessages = err.response.data.detail.map((e: any) =>
            `${e.loc.join('.')}: ${e.msg}`
          ).join(', ');
          setError(errorMessages);
        } else if (typeof err.response.data.detail === 'string') {
          setError(err.response.data.detail);
        } else {
          setError('Validation error: ' + JSON.stringify(err.response.data.detail));
        }
      } else {
        setError('Failed to create vehicle');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto py-8 px-4 max-w-2xl">
      <Card>
        <CardHeader>
          <CardTitle>Add New Vehicle</CardTitle>
          <CardDescription>Add a new vehicle to the fleet</CardDescription>
        </CardHeader>
        <CardContent>
          {error && (
            <Alert variant="destructive" className="mb-4">
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          {locations.length === 0 && (
            <Alert className="mb-4">
              <AlertDescription>
                No locations available. Please create a location first before adding vehicles.
              </AlertDescription>
            </Alert>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label htmlFor="make">Make *</Label>
                <Input
                  id="make"
                  name="make"
                  value={formData.make}
                  onChange={handleChange}
                  required
                  placeholder="Toyota"
                />
              </div>

              <div>
                <Label htmlFor="model">Model *</Label>
                <Input
                  id="model"
                  name="model"
                  value={formData.model}
                  onChange={handleChange}
                  required
                  placeholder="Camry"
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label htmlFor="year">Year *</Label>
                <Input
                  id="year"
                  name="year"
                  type="number"
                  value={formData.year}
                  onChange={handleChange}
                  required
                  min="1900"
                  max="2100"
                />
              </div>

              <div>
                <Label htmlFor="color">Color</Label>
                <Input
                  id="color"
                  name="color"
                  value={formData.color}
                  onChange={handleChange}
                  placeholder="Silver"
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label htmlFor="license_plate">License Plate *</Label>
                <Input
                  id="license_plate"
                  name="license_plate"
                  value={formData.license_plate}
                  onChange={handleChange}
                  required
                  placeholder="ABC-1234"
                />
              </div>

              <div>
                <Label htmlFor="vin">VIN *</Label>
                <Input
                  id="vin"
                  name="vin"
                  value={formData.vin}
                  onChange={handleChange}
                  required
                  placeholder="1HGBH41JXMN109186"
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label htmlFor="vehicle_type">Vehicle Type *</Label>
                <select
                  id="vehicle_type"
                  name="vehicle_type"
                  value={formData.vehicle_type}
                  onChange={handleChange}
                  required
                  className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                >
                  {vehicleTypes.map(type => (
                    <option key={type} value={type}>
                      {type.charAt(0).toUpperCase() + type.slice(1)}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <Label htmlFor="status">Status *</Label>
                <select
                  id="status"
                  name="status"
                  value={formData.status}
                  onChange={handleChange}
                  required
                  className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                >
                  {vehicleStatuses.map(status => (
                    <option key={status} value={status}>
                      {status.charAt(0).toUpperCase() + status.slice(1).replace('_', ' ')}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label htmlFor="mileage">Mileage *</Label>
                <Input
                  id="mileage"
                  name="mileage"
                  type="number"
                  value={formData.mileage}
                  onChange={handleChange}
                  required
                  min="0"
                  placeholder="12500"
                />
              </div>

              <div>
                <Label htmlFor="daily_rate">Daily Rate ($) *</Label>
                <Input
                  id="daily_rate"
                  name="daily_rate"
                  type="number"
                  step="0.01"
                  value={formData.daily_rate}
                  onChange={handleChange}
                  required
                  min="0"
                  placeholder="45.00"
                />
              </div>
            </div>

            <div>
              <Label htmlFor="base_location_id">Base Location *</Label>
              <select
                id="base_location_id"
                name="base_location_id"
                value={formData.base_location_id}
                onChange={handleChange}
                required
                className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
              >
                {locations.map(location => (
                  <option key={location.id} value={location.id}>
                    {location.name} - {location.city}, {location.state}
                  </option>
                ))}
              </select>
            </div>

            <div className="flex gap-4 pt-4">
              <Button type="submit" className="flex-1" disabled={loading || locations.length === 0}>
                {loading ? 'Creating...' : 'Create Vehicle'}
              </Button>
              <Button
                type="button"
                variant="outline"
                onClick={() => navigate('/admin')}
                disabled={loading}
              >
                Cancel
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );
};
