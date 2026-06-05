import { Routes, Route, Navigate } from 'react-router-dom';
import AppLayout from './layouts/AppLayout';
import DashboardPage from './pages/DashboardPage';
import SensorsPage from './pages/SensorsPage';
import HistoryPage from './pages/HistoryPage';
import ActivitiesPage from './pages/ActivitiesPage';
import MetricsPage from './pages/MetricsPage';
import ConsumptionPage from './pages/ConsumptionPage';
import SettingsPage from './pages/SettingsPage';
import NotFoundPage from './pages/NotFoundPage';
import SalonDetailsPage from './pages/SalonDetailsPage';
import SalonesPage from './pages/SalonesPage';

const AppRoutes = () => (
  <Routes>
    <Route path="/" element={<AppLayout />}>
      <Route index element={<DashboardPage />} />
      <Route path="sensores" element={<SensorsPage />} />
      <Route path="historial" element={<HistoryPage />} />
      <Route path="actividades" element={<ActivitiesPage />} />
      <Route path="reportes" element={<MetricsPage />} />
      <Route path="consumo" element={<ConsumptionPage />} />
      <Route path="configuracion" element={<SettingsPage />} />
      <Route path="salones/:id" element={<SalonDetailsPage />} />
      <Route path="salones" element={<SalonesPage />} />
      <Route path="*" element={<NotFoundPage />} />
    </Route>
    <Route path="*" element={<Navigate to="/" replace />} />
  </Routes>
);

export default AppRoutes;
