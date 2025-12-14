import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ratePlansAPI } from '@/api/services';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Alert, AlertDescription } from '@/components/ui/alert';

export const AddRatePlan: React.FC = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    discount_percentage: 0,
    one_way_fee: 0,
    insurance_daily_rate: 0,
    min_days: 1,
    max_days: '',
    is_active: true,
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value, type } = e.target;
    if (type === 'checkbox') {
      const checked = (e.target as HTMLInputElement).checked;
      setFormData(prev => ({ ...prev, [name]: checked }));
    } else {
      setFormData(prev => ({ ...prev, [name]: value }));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      await ratePlansAPI.create({
        name: formData.name,
        description: formData.description || undefined,
        discount_percentage: parseFloat(formData.discount_percentage.toString()),
        one_way_fee: parseFloat(formData.one_way_fee.toString()),
        insurance_daily_rate: parseFloat(formData.insurance_daily_rate.toString()),
        min_days: parseInt(formData.min_days.toString()),
        max_days: formData.max_days ? parseInt(formData.max_days) : undefined,
        is_active: formData.is_active,
      });
      navigate('/admin');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to create rate plan');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto py-8 px-4 max-w-2xl">
      <Card>
        <CardHeader>
          <CardTitle>Add New Rate Plan</CardTitle>
          <CardDescription>Create a new pricing plan for rentals</CardDescription>
        </CardHeader>
        <CardContent>
          {error && (
            <Alert variant="destructive" className="mb-4">
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <Label htmlFor="name">Plan Name *</Label>
              <Input
                id="name"
                name="name"
                value={formData.name}
                onChange={handleChange}
                required
                placeholder="Weekend Special"
              />
            </div>

            <div>
              <Label htmlFor="description">Description</Label>
              <textarea
                id="description"
                name="description"
                value={formData.description}
                onChange={handleChange}
                className="flex min-h-[80px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                placeholder="10% discount for weekend rentals"
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label htmlFor="discount_percentage">Discount (%) *</Label>
                <Input
                  id="discount_percentage"
                  name="discount_percentage"
                  type="number"
                  step="0.01"
                  value={formData.discount_percentage}
                  onChange={handleChange}
                  required
                  min="0"
                  max="100"
                  placeholder="10.00"
                />
              </div>

              <div>
                <Label htmlFor="one_way_fee">One-Way Fee ($) *</Label>
                <Input
                  id="one_way_fee"
                  name="one_way_fee"
                  type="number"
                  step="0.01"
                  value={formData.one_way_fee}
                  onChange={handleChange}
                  required
                  min="0"
                  placeholder="50.00"
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label htmlFor="insurance_daily_rate">Insurance/Day ($) *</Label>
                <Input
                  id="insurance_daily_rate"
                  name="insurance_daily_rate"
                  type="number"
                  step="0.01"
                  value={formData.insurance_daily_rate}
                  onChange={handleChange}
                  required
                  min="0"
                  placeholder="15.00"
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label htmlFor="min_days">Minimum Days *</Label>
                <Input
                  id="min_days"
                  name="min_days"
                  type="number"
                  value={formData.min_days}
                  onChange={handleChange}
                  required
                  min="1"
                  placeholder="1"
                />
              </div>

              <div>
                <Label htmlFor="max_days">Maximum Days (optional)</Label>
                <Input
                  id="max_days"
                  name="max_days"
                  type="number"
                  value={formData.max_days}
                  onChange={handleChange}
                  min="1"
                  placeholder="Leave empty for unlimited"
                />
              </div>
            </div>

            <div className="flex items-center space-x-2">
              <input
                type="checkbox"
                id="is_active"
                name="is_active"
                checked={formData.is_active}
                onChange={handleChange}
                className="h-4 w-4 rounded border-gray-300"
              />
              <Label htmlFor="is_active" className="cursor-pointer">
                Active (available for customers)
              </Label>
            </div>

            <div className="flex gap-4 pt-4">
              <Button type="submit" className="flex-1" disabled={loading}>
                {loading ? 'Creating...' : 'Create Rate Plan'}
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
