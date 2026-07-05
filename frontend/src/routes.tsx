import { Routes, Route, Navigate } from 'react-router-dom';
import AppLayout from './layouts/AppLayout';
import DashboardPage from './pages/DashboardPage';
import SensorsPage from './pages/SensorsPage';
import HistoryPage from './pages/HistoryPage';
import ActivitiesPage from './pages/ActivitiesPage';
import MetricsPage from './pages/MetricsPage';
import ConsumptionPage from './pages/ConsumptionPage';
import NotFoundPage from './pages/NotFoundPage';
import SalonDetailsPage from './pages/SalonDetailsPage';
import SalonHistoryPage from './pages/SalonHistoryPage';
import SalonesPage from './pages/SalonesPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import ProtectedRoute from './components/ui/ProtectedRoute';

const AppRoutes = () => (
  <Routes>
    <Route path="/login" element={<LoginPage />} />
    <Route path="/register" element={<RegisterPage />} />

    <Route
      path="/"
      element={
        <ProtectedRoute>
          <AppLayout />
        </ProtectedRoute>
      }
    >
      <Route index element={<DashboardPage />} />
      <Route path="sensores" element={<SensorsPage />} />
      <Route path="historial" element={<HistoryPage />} />
      <Route path="actividades" element={<ActivitiesPage />} />
      <Route path="reportes" element={<MetricsPage />} />
      <Route path="consumo" element={<ConsumptionPage />} />
      {/* Configuration route removed */}
      <Route path="salones/:id" element={<SalonDetailsPage />} />
      <Route path="salones/:id/historial" element={<SalonHistoryPage />} />
      <Route path="salones" element={<SalonesPage />} />
      <Route path="*" element={<NotFoundPage />} />
    </Route>

    <Route path="*" element={<Navigate to="/login" replace />} />
  </Routes>
);

export default AppRoutes;
