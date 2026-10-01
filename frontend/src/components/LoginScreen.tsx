import React, { useState } from 'react';
import { Briefcase, AlertCircle } from 'lucide-react';
import { ApiService, setAuthToken } from '../services/api';

interface LoginScreenProps {
  onLoginSuccess: (token: string) => void;
}

export const LoginScreen: React.FC<LoginScreenProps> = ({ onLoginSuccess }) => {
  const [username, setUsername] = useState('admin');
  const [password, setPassword] = useState('admin1234');
  const [authError, setAuthError] = useState<string | null>(null);
  const [authLoading, setAuthLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setAuthError(null);
    setAuthLoading(true);
    try {
      const accessToken = await ApiService.login(username, password);
      setAuthToken(accessToken);
      localStorage.setItem('token', accessToken);
      onLoginSuccess(accessToken);
    } catch (err: any) {
      setAuthError("Identifiants incorrects ou serveur indisponible.");
    } finally {
      setAuthLoading(false);
    }
  };

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#0A192F', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '20px', fontFamily: 'sans-serif' }}>
      <div style={{ width: '100%', maxWidth: '440px', backgroundColor: '#ffffff', borderRadius: '16px', padding: '32px', boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.3)' }}>
        <div style={{ textAlign: 'center', marginBottom: '24px' }}>
          <div style={{ display: 'inline-flex', alignItems: 'center', justifyContent: 'center', width: '56px', height: '56px', backgroundColor: '#185FA5', borderRadius: '14px', marginBottom: '12px' }}>
            <Briefcase style={{ width: '30px', height: '30px', color: '#ffffff' }} />
          </div>
          <h1 style={{ fontSize: '24px', fontWeight: '900', color: '#0B1F3A', margin: 0 }}>Luka Mosala SaaS</h1>
          <p style={{ fontSize: '13px', color: '#444441', fontWeight: '600', marginTop: '6px' }}>
            Générateur automatique de dossiers de candidature sur mesure (CV 1P & LM 1P).
          </p>
        </div>

        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          {authError && (
            <div style={{ backgroundColor: '#fef2f2', border: '1px solid #fca5a5', padding: '12px', borderRadius: '10px', display: 'flex', alignItems: 'center', gap: '8px', color: '#991b1b', fontSize: '13px', fontWeight: '600' }}>
              <AlertCircle style={{ width: '18px', height: '18px', flexShrink: 0 }} />
              <span>{authError}</span>
            </div>
          )}

          <div>
            <label style={{ display: 'block', fontSize: '13px', fontWeight: '800', color: '#0B1F3A', marginBottom: '6px' }}>Nom d'utilisateur</label>
            <input type="text" value={username} onChange={e => setUsername(e.target.value)} style={{ width: '100%', padding: '12px', border: '2px solid #cbd5e1', borderRadius: '10px', fontSize: '14px', fontWeight: '700', color: '#0B1F3A', boxSizing: 'border-box' }} required />
          </div>

          <div>
            <label style={{ display: 'block', fontSize: '13px', fontWeight: '800', color: '#0B1F3A', marginBottom: '6px' }}>Mot de passe</label>
            <input type="password" value={password} onChange={e => setPassword(e.target.value)} style={{ width: '100%', padding: '12px', border: '2px solid #cbd5e1', borderRadius: '10px', fontSize: '14px', fontWeight: '700', color: '#0B1F3A', boxSizing: 'border-box' }} required />
          </div>

          <button type="submit" disabled={authLoading} style={{ width: '100%', backgroundColor: '#185FA5', color: '#ffffff', fontWeight: '900', fontSize: '15px', padding: '14px', borderRadius: '10px', border: 'none', cursor: 'pointer', marginTop: '8px' }}>
            {authLoading ? 'Connexion...' : 'Se connecter / S\'inscrire'}
          </button>
        </form>

        <div style={{ marginTop: '20px', padding: '12px', backgroundColor: '#f1f5f9', borderRadius: '10px', fontSize: '12px', color: '#334155', fontWeight: '600', textAlign: 'center' }}>
          💡 Compte de test par défaut : <strong>admin</strong> / <strong>admin1234</strong>
        </div>
      </div>
    </div>
  );
};
