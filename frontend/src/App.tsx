import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuthContext } from '@/features/auth/hooks/useAuthContext';
import { Toaster } from '@/components/ui/sonner';

import LoginPage from '@/pages/LoginPage';
import RegisterPage from '@/pages/RegisterPage';
import ResearchPage from '@/pages/ResearchPage';
import "@/index.css"

const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated } = useAuthContext();
  if (!isAuthenticated) { // Ideally wait for initial check
    // For this demo, isAuthenticated defaults to !!token from localStorage immediately
    return <Navigate to="/login" />;
  }
  return <>{children}</>;
};

function AppRoutes() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route path="/research" element={
        <ProtectedRoute>
          <ResearchPage />
        </ProtectedRoute>
      } />
      <Route path="/" element={<Navigate to="/research" />} />
    </Routes>
  );
}

function App() {
  return (
    <Router>
      <AuthProvider>
        <AppRoutes />
        <Toaster richColors position="top-right" />
      </AuthProvider>
    </Router>
  );
}

export default App;

