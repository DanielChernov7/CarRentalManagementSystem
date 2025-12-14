import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { Layout } from './components/Layout';
import { ProtectedRoute } from './components/ProtectedRoute';
import { Home } from './pages/Home';
import { Login } from './pages/Login';
import { Register } from './pages/Register';
import { BrowseVehicles } from './pages/BrowseVehicles';
import { NewReservation } from './pages/NewReservation';
import { Dashboard } from './pages/Dashboard';
import { AdminDashboard } from './pages/AdminDashboard';
import { ClerkDashboard } from './pages/ClerkDashboard';
import { AddVehicle } from './pages/AddVehicle';
import { AddLocation } from './pages/AddLocation';
import { AddRatePlan } from './pages/AddRatePlan';

function App() {
  return (
    <Router>
      <AuthProvider>
        <Layout>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />

            <Route
              path="/browse"
              element={
                <ProtectedRoute allowedRoles={['customer']}>
                  <BrowseVehicles />
                </ProtectedRoute>
              }
            />

            <Route
              path="/reservation/new"
              element={
                <ProtectedRoute allowedRoles={['customer']}>
                  <NewReservation />
                </ProtectedRoute>
              }
            />

            <Route
              path="/dashboard"
              element={
                <ProtectedRoute allowedRoles={['customer']}>
                  <Dashboard />
                </ProtectedRoute>
              }
            />

            <Route
              path="/admin"
              element={
                <ProtectedRoute allowedRoles={['admin']}>
                  <AdminDashboard />
                </ProtectedRoute>
              }
            />

            <Route
              path="/admin/vehicles/add"
              element={
                <ProtectedRoute allowedRoles={['admin']}>
                  <AddVehicle />
                </ProtectedRoute>
              }
            />

            <Route
              path="/admin/locations/add"
              element={
                <ProtectedRoute allowedRoles={['admin']}>
                  <AddLocation />
                </ProtectedRoute>
              }
            />

            <Route
              path="/admin/rate-plans/add"
              element={
                <ProtectedRoute allowedRoles={['admin']}>
                  <AddRatePlan />
                </ProtectedRoute>
              }
            />

            <Route
              path="/clerk"
              element={
                <ProtectedRoute allowedRoles={['clerk']}>
                  <ClerkDashboard />
                </ProtectedRoute>
              }
            />

            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </Layout>
      </AuthProvider>
    </Router>
  );
}

export default App;
