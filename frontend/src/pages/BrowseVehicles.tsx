import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { vehiclesAPI, locationsAPI } from '@/api/services';
import type { Vehicle, Location } from '@/types';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select } from '@/components/ui/select';
import { Car } from 'lucide-react';

export const BrowseVehicles: React.FC = () => {
  const [vehicles, setVehicles] = useState<Vehicle[]>([]);
  const [locations, setLocations] = useState<Location[]>([]);
  const [loading, setLoading] = useState(true);
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [locationId, setLocationId] = useState('');
  const [vehicleType, setVehicleType] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    loadLocations();
    loadVehicles();
  }, []);

  const loadLocations = async () => {
    try {
      const data = await locationsAPI.getAll();
      setLocations(data);
    } catch (error) {
      console.error('Failed to load locations:', error);
    }
  };

  const loadVehicles = async () => {
    try {
      setLoading(true);
      const data = await vehiclesAPI.getAll({ status: 'available' });
      setVehicles(data);
    } catch (error) {
      console.error('Failed to load vehicles:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async () => {
    if (!startDate || !endDate) {
      alert('Please select start and end dates');
      return;
    }

    try {
      setLoading(true);
      const data = await vehiclesAPI.getAvailable({
        start_date: startDate,
        end_date: endDate,
        location_id: locationId ? parseInt(locationId) : undefined,
        vehicle_type: vehicleType || undefined,
      });
      setVehicles(data);
    } catch (error) {
      console.error('Failed to search vehicles:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleRentNow = (vehicle: Vehicle) => {
    navigate('/reservation/new', {
      state: { vehicle, startDate, endDate, locationId },
    });
  };

  return (
    <div className="container mx-auto py-8 px-4">
      <h1 className="text-3xl font-bold mb-8">Browse Vehicles</h1>

      <Card className="mb-8">
        <CardHeader>
          <CardTitle>Search Available Vehicles</CardTitle>
          <CardDescription>Find the perfect vehicle for your trip</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="space-y-2">
              <Label htmlFor="startDate">Start Date</Label>
              <Input
                id="startDate"
                type="date"
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
                min={new Date().toISOString().split('T')[0]}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="endDate">End Date</Label>
              <Input
                id="endDate"
                type="date"
                value={endDate}
                onChange={(e) => setEndDate(e.target.value)}
                min={startDate || new Date().toISOString().split('T')[0]}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="location">Location</Label>
              <Select
                id="location"
                value={locationId}
                onChange={(e) => setLocationId(e.target.value)}
              >
                <option value="">All Locations</option>
                {locations.map((loc) => (
                  <option key={loc.id} value={loc.id}>
                    {loc.name}
                  </option>
                ))}
              </Select>
            </div>

            <div className="space-y-2">
              <Label htmlFor="vehicleType">Vehicle Type</Label>
              <Select
                id="vehicleType"
                value={vehicleType}
                onChange={(e) => setVehicleType(e.target.value)}
              >
                <option value="">All Types</option>
                <option value="sedan">Sedan</option>
                <option value="suv">SUV</option>
                <option value="truck">Truck</option>
                <option value="van">Van</option>
                <option value="luxury">Luxury</option>
                <option value="economy">Economy</option>
              </Select>
            </div>
          </div>
        </CardContent>
        <CardFooter>
          <Button onClick={handleSearch} className="w-full">
            Search Vehicles
          </Button>
        </CardFooter>
      </Card>

      {loading ? (
        <div className="text-center py-12">Loading vehicles...</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {vehicles.map((vehicle) => (
            <Card key={vehicle.id}>
              <CardHeader>
                <div className="flex items-center gap-2">
                  <Car className="h-6 w-6" />
                  <CardTitle>
                    {vehicle.year} {vehicle.make} {vehicle.model}
                  </CardTitle>
                </div>
                <CardDescription className="capitalize">{vehicle.vehicle_type}</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-2 text-sm">
                  <p>
                    <span className="font-semibold">Color:</span> {vehicle.color || 'N/A'}
                  </p>
                  <p>
                    <span className="font-semibold">License:</span> {vehicle.license_plate}
                  </p>
                  <p>
                    <span className="font-semibold">Mileage:</span> {vehicle.mileage.toLocaleString()} miles
                  </p>
                  <p className="text-lg font-bold text-primary">
                    ${vehicle.daily_rate.toFixed(2)}/day
                  </p>
                </div>
              </CardContent>
              <CardFooter>
                <Button onClick={() => handleRentNow(vehicle)} className="w-full">
                  Rent Now
                </Button>
              </CardFooter>
            </Card>
          ))}
        </div>
      )}

      {!loading && vehicles.length === 0 && (
        <div className="text-center py-12 text-gray-500">
          No vehicles found. Try adjusting your search criteria.
        </div>
      )}
    </div>
  );
};
