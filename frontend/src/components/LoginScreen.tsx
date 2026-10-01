import React, { useState } from 'react';
import { Briefcase, AlertCircle } from 'lucide-react';
import { ApiService, setAuthToken } from '../services/api';

interface LoginScreenProps {
  onLoginSuccess: (token: string) => void;
}

export const LoginScreen: React.FC<LoginScreenProps> = ({ onLoginSuccess }) => {
  const [mode, setMode] = useState<'login' | 'register'>('login');
  const [username, setUsername] = useState('admin');
  const [phone, setPhone] = useState('066130118');
  const [password, setPassword] = useState('admin1234');
  const [confirmPassword, setConfirmPassword] = useState('admin1234');
  const [authError, setAuthError] = useState<string | null>(null);
  const [authLoading, setAuthLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setAuthError(null);
    setAuthLoading(true);

    try {
      if (mode === 'register') {
        if (password !== confirmPassword) {
          setAuthError("Les mots de passe ne correspondent pas.");
          setAuthLoading(false);
          return;
        }
        const token = await ApiService.registerByPhone(phone, password, confirmPassword);
        setAuthToken(token);
        localStorage.setItem('token', token);
        onLoginSuccess(token);
      } else {
        const accessToken = await ApiService.login(username, password);
        setAuthToken(accessToken);
        localStorage.setItem('token', accessToken);
        onLoginSuccess(accessToken);
      }
    } catch (err: any) {
      const msg = err?.response?.data?.password_confirm || err?.response?.data?.username || "Erreur lors de l'authentification ou création de compte.";
      setAuthError(typeof msg === 'string' ? msg : "Identifiants incorrects ou création de compte échouée.");
    } finally {
      setAuthLoading(false);
    }
  };

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#0A192F', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '20px', fontFamily: 'sans-serif' }}>
      <div style={{ width: '100%', maxWidth: '440px', backgroundColor: '#ffffff', borderRadius: '16px', padding: '32px', boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.3)' }}>
        <div style={{ textAlign: 'center', marginBottom: '20px' }}>
          <div style={{ display: 'inline-flex', alignItems: 'center', justifyContent: 'center', width: '56px', height: '56px', backgroundColor: '#185FA5', borderRadius: '14px', marginBottom: '12px' }}>
            <Briefcase style={{ width: '30px', height: '30px', color: '#ffffff' }} />
          </div>
          <h1 style={{ fontSize: '24px', fontWeight: '900', color: '#0B1F3A', margin: 0 }}>Luka Mosala SaaS</h1>
          <p style={{ fontSize: '13px', color: '#444441', fontWeight: '600', marginTop: '6px' }}>
            Générateur de dossiers de candidature sur mesure (Généré par Luka Mossala).
          </p>
        </div>

        {/* TOGGLE BETWEEN LOGIN & REGISTER */}
        <div style={{ display: 'flex', border: '1px solid #cbd5e1', borderRadius: '10px', overflow: 'hidden', marginBottom: '20px' }}>
          <button
            type="button"
            onClick={() => { setMode('login'); setAuthError(null); }}
            style={{ flex: 1, padding: '10px', backgroundColor: mode === 'login' ? '#185FA5' : '#ffffff', color: mode === 'login' ? '#ffffff' : '#0B1F3A', fontWeight: '800', border: 'none', cursor: 'pointer' }}
          >
            Se Connecter
          </button>
          <button
            type="button"
            onClick={() => { setMode('register'); setAuthError(null); }}
            style={{ flex: 1, padding: '10px', backgroundColor: mode === 'register' ? '#185FA5' : '#ffffff', color: mode === 'register' ? '#ffffff' : '#0B1F3A', fontWeight: '800', border: 'none', cursor: 'pointer' }}
          >
            Créer un compte
          </button>
        </div>

        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          {authError && (
            <div style={{ backgroundColor: '#fef2f2', border: '1px solid #fca5a5', padding: '12px', borderRadius: '10px', display: 'flex', alignItems: 'center', gap: '8px', color: '#991b1b', fontSize: '13px', fontWeight: '600' }}>
              <AlertCircle style={{ width: '18px', height: '18px', flexShrink: 0 }} />
              <span>{authError}</span>
            </div>
          )}

          {mode === 'login' ? (
            <div>
              <label style={{ display: 'block', fontSize: '13px', fontWeight: '800', color: '#0B1F3A', marginBottom: '6px' }}>Nom d'utilisateur ou Téléphone</label>
              <input type="text" value={username} onChange={e => setUsername(e.target.value)} style={{ width: '100%', padding: '12px', border: '2px solid #cbd5e1', borderRadius: '10px', fontSize: '14px', fontWeight: '700', color: '#0B1F3A', boxSizing: 'border-box' }} required />
            </div>
          ) : (
            <div>
              <label style={{ display: 'block', fontSize: '13px', fontWeight: '800', color: '#0B1F3A', marginBottom: '6px' }}>Numéro de Téléphone</label>
              <input type="text" placeholder="06XXXXXXX" value={phone} onChange={e => setPhone(e.target.value)} style={{ width: '100%', padding: '12px', border: '2px solid #cbd5e1', borderRadius: '10px', fontSize: '14px', fontWeight: '700', color: '#0B1F3A', boxSizing: 'border-box' }} required />
            </div>
          )}

          <div>
            <label style={{ display: 'block', fontSize: '13px', fontWeight: '800', color: '#0B1F3A', marginBottom: '6px' }}>Mot de passe</label>
            <input type="password" value={password} onChange={e => setPassword(e.target.value)} style={{ width: '100%', padding: '12px', border: '2px solid #cbd5e1', borderRadius: '10px', fontSize: '14px', fontWeight: '700', color: '#0B1F3A', boxSizing: 'border-box' }} required />
          </div>

          {mode === 'register' && (
            <div>
              <label style={{ display: 'block', fontSize: '13px', fontWeight: '800', color: '#0B1F3A', marginBottom: '6px' }}>Confirmer le mot de passe</label>
              <input type="password" value={confirmPassword} onChange={e => setConfirmPassword(e.target.value)} style={{ width: '100%', padding: '12px', border: '2px solid #cbd5e1', borderRadius: '10px', fontSize: '14px', fontWeight: '700', color: '#0B1F3A', boxSizing: 'border-box' }} required />
            </div>
          )}

          <button type="submit" disabled={authLoading} style={{ width: '100%', backgroundColor: '#185FA5', color: '#ffffff', fontWeight: '900', fontSize: '15px', padding: '14px', borderRadius: '10px', border: 'none', cursor: 'pointer', marginTop: '8px' }}>
            {authLoading ? 'Traitement...' : (mode === 'register' ? 'Créer mon compte automatiquement' : 'Se connecter')}
          </button>
        </form>

        <div style={{ marginTop: '20px', padding: '12px', backgroundColor: '#f1f5f9', borderRadius: '10px', fontSize: '12px', color: '#334155', fontWeight: '600', textAlign: 'center' }}>
          💡 Compte de test par défaut : <strong>admin</strong> / <strong>admin1234</strong>
        </div>
      </div>
    </div>
  );
};
