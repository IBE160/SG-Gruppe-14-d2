import { useEffect, useState } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { supabase } from './supabaseClient';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import './App.css'; // Assuming this is needed, based on existing file.

function App() {
  const [session, setSession] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    supabase.auth.getSession().then(({ data: { session } }) => {
      setSession(session);
      setLoading(false);
    });

    const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
      setSession(session);
    });

    return () => subscription.unsubscribe();
  }, []);

  if (loading) return <div>Laster...</div>;

  return (
    <Routes>
      <Route path="/" element={session ? <Navigate to="/dashboard" /> : <Login />} />
      <Route
        path="/dashboard"
        element={session ? <Dashboard session={session} /> : <Navigate to="/" />}
      />
      <Route
        path="/chat/:wbsCode/:supplierId"
        element={session ? <Chat session={session} /> : <Navigate to="/" />}
      />
    </Routes>
  );
}

export default App;

