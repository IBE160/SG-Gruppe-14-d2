import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { supabase } from '../supabaseClient';

function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isRegistering, setIsRegistering] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleAuth = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      if (isRegistering) {
        const { data, error } = await supabase.auth.signUp({
          email,
          password,
        });
        if (error) throw error;
        alert('Konto opprettet! Logger inn...');
      }

      const { data, error } = await supabase.auth.signInWithPassword({
        email,
        password,
      });

      if (error) throw error;
      navigate('/dashboard');
    } catch (error) {
      setError(error.message || 'Feil e-post eller passord');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <h1>Nye Hædda Barneskole</h1>
        <p>Prosjektledelsessimulator</p>

        <form onSubmit={handleAuth}>
          <label>E-post</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />

          <label>Passord</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            minLength={6}
          />

          {error && <p className="error">{error}</p>}

          <button type="submit" disabled={loading}>
            {loading ? 'Behandler...' : (isRegistering ? 'Registrer' : 'Logg Inn')}
          </button>
        </form>

        <p>
          {isRegistering ? 'Har du allerede konto?' : 'Har du ikke konto?'}
          <button onClick={() => setIsRegistering(!isRegistering)}>
            {isRegistering ? 'Logg Inn' : 'Registrer deg'}
          </button>
        </p>
      </div>
    </div>
  );
}

export default Login;
