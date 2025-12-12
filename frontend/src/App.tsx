import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { AuthProvider, useAuthContext } from '@/features/auth/hooks/useAuthContext';

import LoginPage from '@/pages/LoginPage';
import RegisterPage from '@/pages/RegisterPage';
import ResearchPage from '@/pages/ResearchPage';
import "@/index.css"

// Create a client
const queryClient = new QueryClient();

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
    <QueryClientProvider client={queryClient}>
      <Router>
        <AuthProvider>
          <AppRoutes />
        </AuthProvider>
      </Router>
    </QueryClientProvider>
  );
}

export default App;
