import React, { useState, useEffect } from 'react';
import { vehiclesAPI, locationsAPI, ratePlansAPI } from '@/api/services';
import type { Vehicle, Location, RatePlan } from '@/types';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select } from '@/components/ui/select';

export const AdminDashboard: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'vehicles' | 'locations' | 'ratePlans'>('vehicles');
  const [vehicles, setVehicles] = useState<Vehicle[]>([]);
  const [locations, setLocations] = useState<Location[]>([]);
  const [ratePlans, setRatePlans] = useState<RatePlan[]>([]);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState<any>({});

  useEffect(() => {
    loadData();
  }, [activeTab]);

  const loadData = async () => {
    try {
      if (activeTab === 'vehicles') {
        const data = await vehiclesAPI.getAll();
        setVehicles(data);
      } else if (activeTab === 'locations') {
        const data = await locationsAPI.getAll();
        setLocations(data);
      } else if (activeTab === 'ratePlans') {
        const data = await ratePlansAPI.getAll();
        setRatePlans(data);
      }
    } catch (error) {
      console.error('Failed to load data:', error);
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm('Are you sure you want to delete this item?')) return;

    try {
      if (activeTab === 'vehicles') {
        await vehiclesAPI.delete(id);
      } else if (activeTab === 'locations') {
        await locationsAPI.delete(id);
      } else if (activeTab === 'ratePlans') {
        await ratePlansAPI.delete(id);
      }
      loadData();
    } catch (error: any) {
      alert(error.response?.data?.detail || 'Failed to delete');
    }
  };

  return (
    <div className="container mx-auto py-8 px-4">
      <h1 className="text-3xl font-bold mb-8">Admin Dashboard</h1>

      <div className="flex gap-4 mb-6">
        <Button
          variant={activeTab === 'vehicles' ? 'default' : 'outline'}
          onClick={() => setActiveTab('vehicles')}
        >
          Vehicles
        </Button>
        <Button
          variant={activeTab === 'locations' ? 'default' : 'outline'}
          onClick={() => setActiveTab('locations')}
        >
          Locations
        </Button>
        <Button
          variant={activeTab === 'ratePlans' ? 'default' : 'outline'}
          onClick={() => setActiveTab('ratePlans')}
        >
          Rate Plans
        </Button>
      </div>

      <Card>
        <CardHeader>
          <div className="flex justify-between items-center">
            <div>
              <CardTitle>
                {activeTab === 'vehicles' && 'Manage Vehicles'}
                {activeTab === 'locations' && 'Manage Locations'}
                {activeTab === 'ratePlans' && 'Manage Rate Plans'}
              </CardTitle>
              <CardDescription>
                {activeTab === 'vehicles' && 'Add, edit, or remove vehicles'}
                {activeTab === 'locations' && 'Add, edit, or remove locations'}
                {activeTab === 'ratePlans' && 'Add, edit, or remove rate plans'}
              </CardDescription>
            </div>
            <Button onClick={() => setShowForm(true)}>Add New</Button>
          </div>
        </CardHeader>
        <CardContent>
          {activeTab === 'vehicles' && (
            <div className="space-y-4">
              {vehicles.map((vehicle) => (
                <div key={vehicle.id} className="border rounded-lg p-4 flex justify-between items-center">
                  <div>
                    <h3 className="font-semibold">
                      {vehicle.year} {vehicle.make} {vehicle.model}
                    </h3>
                    <p className="text-sm text-gray-600">
                      {vehicle.license_plate} | {vehicle.vehicle_type} | ${vehicle.daily_rate}/day
                    </p>
                    <span className={`text-xs px-2 py-1 rounded ${
                      vehicle.status === 'available' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                    }`}>
                      {vehicle.status}
                    </span>
                  </div>
                  <Button variant="destructive" size="sm" onClick={() => handleDelete(vehicle.id)}>
                    Delete
                  </Button>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'locations' && (
            <div className="space-y-4">
              {locations.map((location) => (
                <div key={location.id} className="border rounded-lg p-4 flex justify-between items-center">
                  <div>
                    <h3 className="font-semibold">{location.name}</h3>
                    <p className="text-sm text-gray-600">
                      {location.address}, {location.city}, {location.state} {location.zip_code}
                    </p>
                    <p className="text-sm text-gray-600">{location.phone}</p>
                  </div>
                  <Button variant="destructive" size="sm" onClick={() => handleDelete(location.id)}>
                    Delete
                  </Button>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'ratePlans' && (
            <div className="space-y-4">
              {ratePlans.map((plan) => (
                <div key={plan.id} className="border rounded-lg p-4 flex justify-between items-center">
                  <div>
                    <h3 className="font-semibold">{plan.name}</h3>
                    <p className="text-sm text-gray-600">
                      {plan.discount_percentage}% discount | One-way fee: ${plan.one_way_fee}
                    </p>
                    <p className="text-sm text-gray-600">
                      Insurance: ${plan.insurance_daily_rate}/day | {plan.min_days}-{plan.max_days || '∞'} days
                    </p>
                  </div>
                  <Button variant="destructive" size="sm" onClick={() => handleDelete(plan.id)}>
                    Delete
                  </Button>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};
