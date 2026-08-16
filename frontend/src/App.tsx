import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  Briefcase, FileText, User, CreditCard, Upload, Download,
  Sparkles, CheckCircle, ShieldCheck, Phone, Mail, MapPin,
  Eye, RefreshCw, Scissors, ChevronRight, Lock, LogOut, AlertCircle
} from 'lucide-react';

const API_BASE_URL = import.meta.env.VITE_API_URL || (
  window.location.hostname.includes('onrender.com')
    ? 'https://luka-mosala-backend.onrender.com'
    : ''
);

axios.defaults.baseURL = API_BASE_URL;

interface ProfileData {
  title: string;
  phone: string;
  cities: string;
  readme_content: string;
  cropped_photo: string | null;
}

interface ApplicationPackage {
  id: number;
  job_offer: {
    title: string;
    company: string;
    site_category: string;
    abbreviation: string;
  };
  cv_pdf: string;
  cover_letter_pdf: string;
  email_txt: string;
  zip_package: string;
  created_at: string;
}

interface SubscriptionData {
  credits_remaining: number;
  plan: {
    name: string;
  } | null;
}

export default function App() {
  const [activeTab, setActiveTab] = useState<'dashboard' | 'profile' | 'create' | 'plans'>('dashboard');
  const [token, setToken] = useState<string | null>(localStorage.getItem('token'));

  // Default credentials as requested by user
  const [username, setUsername] = useState('admin');
  const [password, setPassword] = useState('admin1234');
  const [authError, setAuthError] = useState<string | null>(null);
  const [authLoading, setAuthLoading] = useState(false);

  const [profile, setProfile] = useState<ProfileData>({
    title: 'Consultant IT & Expert Fullstack',
    phone: '+242 06 613 01 18',
    cities: 'Brazzaville & Pointe-Noire, Congo',
    readme_content: '# CV | CHRIST DANY OBIEY\nConsultant IT & Transformation Digitale',
    cropped_photo: null
  });

  const [jobText, setJobText] = useState('');
  const [sourceUrl, setSourceUrl] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [packages, setPackages] = useState<ApplicationPackage[]>([]);
  const [subscription, setSubscription] = useState<SubscriptionData>({ credits_remaining: 1, plan: null });

  const [selectedPlan, setSelectedPlan] = useState<number>(2);
  const [paymentMethod, setPaymentMethod] = useState<'AIRTEL_MONEY' | 'MTN_MOMO' | 'PAYDUNYA'>('AIRTEL_MONEY');
  const [phoneNumber, setPhoneNumber] = useState('+242066130118');
  const [paymentSuccessMsg, setPaymentSuccessMsg] = useState<string | null>(null);

  useEffect(() => {
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      fetchData();
    }
  }, [token]);

  const fetchData = async () => {
    try {
      const [profRes, subRes, pkgsRes] = await Promise.all([
        axios.get('/api/profile/'),
        axios.get('/api/subscriptions/me/'),
        axios.get('/api/jobs/packages/')
      ]);
      setProfile(profRes.data);
      setSubscription(subRes.data);
      setPackages(pkgsRes.data);
    } catch (e) {
      console.error("Error fetching user data:", e);
    }
  };

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setAuthError(null);
    setAuthLoading(true);
    try {
      const res = await axios.post('/api/auth/login/', { username, password });
      const accessToken = res.data.access;
      setToken(accessToken);
      localStorage.setItem('token', accessToken);
      axios.defaults.headers.common['Authorization'] = `Bearer ${accessToken}`;
      await fetchData();
    } catch (e: any) {
      // If login failed, attempt to register automatically for seamless UX
      try {
        const regRes = await axios.post('/api/auth/register/', {
          username,
          password,
          email: `${username}@lukamosala.cg`,
          first_name: username === 'admin' ? 'Admin' : 'Utilisateur',
          last_name: 'Luka Mosala'
        });
        const accessToken = regRes.data.access;
        setToken(accessToken);
        localStorage.setItem('token', accessToken);
        axios.defaults.headers.common['Authorization'] = `Bearer ${accessToken}`;
        await fetchData();
      } catch (err: any) {
        const errorMsg = e?.response?.data?.detail || e?.response?.data?.error || "Identifiants incorrects ou serveur indisponible.";
        setAuthError(errorMsg);
      }
    } finally {
      setAuthLoading(false);
    }
  };

  const handleLogout = () => {
    setToken(null);
    localStorage.removeItem('token');
    delete axios.defaults.headers.common['Authorization'];
  };

  const handleGenerateApplication = async () => {
    if (!jobText && !sourceUrl) {
      alert("Veuillez coller le texte de l'offre ou entrer l'URL.");
      return;
    }
    setIsGenerating(true);
    try {
      await axios.post('/api/jobs/offers/', {
        source_type: sourceUrl ? 'URL' : 'TEXT',
        source_url: sourceUrl,
        raw_text: jobText
      });
      setJobText('');
      setSourceUrl('');
      await fetchData();
      setActiveTab('dashboard');
      alert("Candidature sur mesure générée avec succès !");
    } catch (e: any) {
      alert(e?.response?.data?.error || "Erreur lors de la génération de la candidature. Vérifiez vos crédits.");
    } finally {
      setIsGenerating(false);
    }
  };

  const handlePayment = async () => {
    setPaymentSuccessMsg(null);
    try {
      const res = await axios.post('/api/subscriptions/pay/', {
        plan_id: selectedPlan,
        payment_method: paymentMethod,
        phone_number: phoneNumber
      });
      setPaymentSuccessMsg(`Paiement réussi via ${paymentMethod} ! Vos crédits ont été rechargés.`);
      await fetchData();
    } catch (e: any) {
      alert("Échec de la transaction Fintech Mobile Money.");
    }
  };

  if (!token) {
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

          <form onSubmit={handleLogin} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            {authError && (
              <div style={{ backgroundColor: '#fef2f2', border: '1px solid #fca5a5', padding: '12px', borderRadius: '10px', display: 'flex', alignItems: 'center', gap: '8px', color: '#991b1b', fontSize: '13px', fontWeight: '600' }}>
                <AlertCircle style={{ width: '18px', height: '18px', flexShrink: 0 }} />
                <span>{authError}</span>
              </div>
            )}

            <div>
              <label style={{ display: 'block', fontSize: '13px', fontWeight: '800', color: '#0B1F3A', marginBottom: '6px' }}>
                Nom d'utilisateur
              </label>
              <input
                type="text"
                value={username}
                onChange={e => setUsername(e.target.value)}
                style={{ width: '100%', padding: '12px', border: '2px solid #cbd5e1', borderRadius: '10px', fontSize: '14px', fontWeight: '700', color: '#0B1F3A', boxSizing: 'border-box' }}
                required
              />
            </div>

            <div>
              <label style={{ display: 'block', fontSize: '13px', fontWeight: '800', color: '#0B1F3A', marginBottom: '6px' }}>
                Mot de passe
              </label>
              <input
                type="password"
                value={password}
                onChange={e => setPassword(e.target.value)}
                style={{ width: '100%', padding: '12px', border: '2px solid #cbd5e1', borderRadius: '10px', fontSize: '14px', fontWeight: '700', color: '#0B1F3A', boxSizing: 'border-box' }}
                required
              />
            </div>

            <button
              type="submit"
              disabled={authLoading}
              style={{ width: '100%', backgroundColor: '#185FA5', color: '#ffffff', fontWeight: '900', fontSize: '15px', padding: '14px', borderRadius: '10px', border: 'none', cursor: 'pointer', marginTop: '8px', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px' }}
            >
              {authLoading ? 'Connexion en cours...' : 'Se connecter / S\'inscrire'}
            </button>
          </form>

          <div style={{ marginTop: '20px', padding: '12px', backgroundColor: '#f1f5f9', borderRadius: '10px', fontSize: '12px', color: '#334155', fontWeight: '600', textAlign: 'center' }}>
            💡 Compte de test par défaut :<br />
            <strong>Identifiant:</strong> admin &nbsp;|&nbsp; <strong>Mot de passe:</strong> admin1234
          </div>
        </div>
      </div>
    );
  }

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#f8fafc', color: '#0B1F3A', fontFamily: 'sans-serif' }}>
      {/* Top Navbar */}
      <header style={{ backgroundColor: '#0B1F3A', color: '#ffffff', borderBottom: '1px solid #1e293b' }}>
        <div style={{ maxWidth: '1280px', margin: '0 auto', padding: '0 24px', height: '64px', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <div style={{ backgroundColor: '#185FA5', padding: '8px', borderRadius: '10px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <Briefcase style={{ width: '20px', height: '20px', color: '#ffffff' }} />
            </div>
            <div>
              <span style={{ fontWeight: '900', fontSize: '18px', color: '#ffffff', letterSpacing: '-0.5px' }}>Luka Mosala</span>
              <span style={{ fontSize: '10px', fontWeight: '800', backgroundColor: '#185FA5', color: '#ffffff', padding: '2px 6px', borderRadius: '4px', marginLeft: '8px', textTransform: 'uppercase' }}>SaaS Pro</span>
            </div>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', backgroundColor: 'rgba(255, 255, 255, 0.1)', padding: '6px 14px', borderRadius: '20px', border: '1px solid rgba(255, 255, 255, 0.15)' }}>
              <Sparkles style={{ width: '16px', height: '16px', color: '#f59e0b' }} />
              <span style={{ fontSize: '13px', fontWeight: '800', color: '#ffffff' }}>{subscription.credits_remaining} Crédit(s)</span>
            </div>
            <button
              onClick={handleLogout}
              style={{ backgroundColor: 'transparent', border: '1px solid rgba(255, 255, 255, 0.2)', color: '#ffffff', padding: '6px 12px', borderRadius: '8px', fontSize: '12px', fontWeight: '700', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '6px' }}
            >
              <LogOut style={{ width: '14px', height: '14px' }} />
              <span>Déconnexion</span>
            </button>
          </div>
        </div>
      </header>

      {/* Main Navigation Tabs */}
      <div style={{ backgroundColor: '#ffffff', borderBottom: '1px solid #e2e8f0' }}>
        <div style={{ maxWidth: '1280px', margin: '0 auto', padding: '0 24px', display: 'flex', gap: '24px' }}>
          {[
            { id: 'dashboard', label: 'Mes Candidatures', icon: Briefcase },
            { id: 'create', label: 'Générer un Dossier', icon: Sparkles },
            { id: 'profile', label: 'Profil & README', icon: User },
            { id: 'plans', label: 'Abonnements & Crédits', icon: CreditCard },
          ].map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px',
                  padding: '16px 0',
                  border: 'none',
                  borderBottom: isActive ? '3px solid #185FA5' : '3px solid transparent',
                  backgroundColor: 'transparent',
                  color: isActive ? '#185FA5' : '#444441',
                  fontWeight: isActive ? '900' : '700',
                  fontSize: '14px',
                  cursor: 'pointer',
                  transition: 'all 0.2s'
                }}
              >
                <Icon style={{ width: '18px', height: '18px', color: isActive ? '#185FA5' : '#444441' }} />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Content Container */}
      <main style={{ maxWidth: '1280px', margin: '0 auto', padding: '32px 24px' }}>
        {activeTab === 'dashboard' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                <h2 style={{ fontSize: '24px', fontWeight: '900', color: '#0B1F3A', margin: 0 }}>Tableau de Bord des Candidatures</h2>
                <p style={{ fontSize: '14px', fontWeight: '600', color: '#444441', marginTop: '4px' }}>Gérez vos dossiers de candidature sur mesure prêts à être envoyés.</p>
              </div>
              <button
                onClick={() => setActiveTab('create')}
                style={{ backgroundColor: '#185FA5', color: '#ffffff', fontWeight: '800', fontSize: '14px', padding: '12px 20px', borderRadius: '10px', border: 'none', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '8px' }}
              >
                <Sparkles style={{ width: '18px', height: '18px' }} />
                <span>Nouvelle Candidature</span>
              </button>
            </div>

            {packages.length === 0 ? (
              <div style={{ backgroundColor: '#ffffff', padding: '48px', borderRadius: '16px', border: '1px solid #cbd5e1', textAlign: 'center' }}>
                <FileText style={{ width: '48px', height: '48px', color: '#94a3b8', margin: '0 auto 16px' }} />
                <h3 style={{ fontSize: '18px', fontWeight: '800', color: '#0B1F3A' }}>Aucune candidature générée pour le moment</h3>
                <p style={{ color: '#444441', fontSize: '14px', marginTop: '8px' }}>Importez une offre d'emploi pour créer votre premier dossier sur mesure.</p>
              </div>
            ) : (
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(360px, 1fr))', gap: '20px' }}>
                {packages.map((pkg) => (
                  <div key={pkg.id} style={{ backgroundColor: '#ffffff', borderRadius: '16px', border: '1px solid #cbd5e1', padding: '20px', display: 'flex', flexDirection: 'column', gap: '16px', boxShadow: '0 4px 6px -1px rgba(0,0,0,0.05)' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                      <div>
                        <span style={{ fontSize: '11px', fontWeight: '900', backgroundColor: '#e0f2fe', color: '#0369a1', padding: '4px 10px', borderRadius: '6px', textTransform: 'uppercase' }}>
                          {pkg.job_offer.site_category || 'ACPE'}
                        </span>
                        <h3 style={{ fontSize: '18px', fontWeight: '800', color: '#0B1F3A', marginTop: '8px', margin: '8px 0 2px' }}>{pkg.job_offer.title}</h3>
                        <p style={{ fontSize: '13px', fontWeight: '700', color: '#444441', margin: 0 }}>{pkg.job_offer.company || 'Organisme Recruteur'}</p>
                      </div>
                    </div>

                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px', borderTop: '1px solid #f1f5f9', paddingTop: '16px' }}>
                      <a href={pkg.cv_pdf} target="_blank" rel="noreferrer" style={{ textDecoration: 'none' }}>
                        <button style={{ width: '100%', border: '1px solid #0B1F3A', backgroundColor: '#0B1F3A', color: '#ffffff', fontWeight: '800', fontSize: '12px', padding: '10px', borderRadius: '8px', cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '6px' }}>
                          <Download style={{ width: '14px', height: '14px' }} />
                          <span>CV (1 Page)</span>
                        </button>
                      </a>
                      <a href={pkg.cover_letter_pdf} target="_blank" rel="noreferrer" style={{ textDecoration: 'none' }}>
                        <button style={{ width: '100%', border: '1px solid #0B1F3A', backgroundColor: '#0B1F3A', color: '#ffffff', fontWeight: '800', fontSize: '12px', padding: '10px', borderRadius: '8px', cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '6px' }}>
                          <Download style={{ width: '14px', height: '14px' }} />
                          <span>LM (1 Page)</span>
                        </button>
                      </a>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {activeTab === 'create' && (
          <div style={{ maxWidth: '768px', margin: '0 auto', backgroundColor: '#ffffff', padding: '32px', borderRadius: '16px', border: '1px solid #cbd5e1', boxShadow: '0 4px 6px -1px rgba(0,0,0,0.05)' }}>
            <h2 style={{ fontSize: '22px', fontWeight: '900', color: '#0B1F3A', margin: '0 0 8px' }}>Générer un Dossier Sur Mesure</h2>
            <p style={{ fontSize: '14px', fontWeight: '600', color: '#444441', marginBottom: '24px' }}>Entrez le texte brut ou l'URL de l'offre d'emploi. L'agent IA créera instantanément un CV (1P) et une Lettre de Motivation (1P) ciblés.</p>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
              <div>
                <label style={{ display: 'block', fontSize: '13px', fontWeight: '800', color: '#0B1F3A', marginBottom: '6px' }}>Option A : Lien URL de l'offre</label>
                <input
                  type="url"
                  placeholder="https://acpe.cg/emplois/developpeur-fullstack"
                  value={sourceUrl}
                  onChange={e => setSourceUrl(e.target.value)}
                  style={{ width: '100%', padding: '12px', border: '2px solid #cbd5e1', borderRadius: '10px', fontSize: '14px', fontWeight: '600', color: '#0B1F3A', boxSizing: 'border-box' }}
                />
              </div>

              <div style={{ textAlign: 'center', fontWeight: '800', fontSize: '12px', color: '#94a3b8' }}>OU</div>

              <div>
                <label style={{ display: 'block', fontSize: '13px', fontWeight: '800', color: '#0B1F3A', marginBottom: '6px' }}>Option B : Texte brut de l'offre</label>
                <textarea
                  rows={6}
                  placeholder="Collez ici l'intitulé du poste, la description et les exigences de l'offre d'emploi..."
                  value={jobText}
                  onChange={e => setJobText(e.target.value)}
                  style={{ width: '100%', padding: '12px', border: '2px solid #cbd5e1', borderRadius: '10px', fontSize: '14px', fontWeight: '600', color: '#0B1F3A', boxSizing: 'border-box' }}
                ></textarea>
              </div>

              <button
                onClick={handleGenerateApplication}
                disabled={isGenerating}
                style={{ width: '100%', backgroundColor: '#185FA5', color: '#ffffff', fontWeight: '900', fontSize: '16px', padding: '16px', borderRadius: '10px', border: 'none', cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px' }}
              >
                {isGenerating ? (
                  <>
                    <RefreshCw style={{ width: '20px', height: '20px', animation: 'spin 1s linear infinite' }} />
                    <span>Génération de votre dossier en cours...</span>
                  </>
                ) : (
                  <>
                    <Sparkles style={{ width: '20px', height: '20px' }} />
                    <span>Générer CV (1 Page), LM (1 Page) & Email TXT</span>
                  </>
                )}
              </button>
            </div>
          </div>
        )}

        {activeTab === 'profile' && (
          <div style={{ maxWidth: '896px', margin: '0 auto', backgroundColor: '#ffffff', padding: '32px', borderRadius: '16px', border: '1px solid #cbd5e1', display: 'flex', flexDirection: 'column', gap: '20px' }}>
            <div>
              <h2 style={{ fontSize: '24px', fontWeight: '900', color: '#0B1F3A', margin: 0 }}>Gestion de Profil & README de Référence</h2>
              <p style={{ fontSize: '14px', fontWeight: '600', color: '#444441', marginTop: '6px' }}>Vos données de référence utilisées par le moteur IA pour rédiger vos candidatures.</p>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
              <div>
                <label style={{ display: 'block', fontSize: '14px', fontWeight: '800', color: '#0B1F3A', marginBottom: '6px' }}>Titre Principal</label>
                <input
                  type="text"
                  value={profile.title}
                  onChange={e => setProfile({...profile, title: e.target.value})}
                  style={{ width: '100%', padding: '12px', border: '2px solid #cbd5e1', borderRadius: '10px', fontSize: '14px', fontWeight: '600', color: '#0B1F3A', boxSizing: 'border-box' }}
                />
              </div>
              <div>
                <label style={{ display: 'block', fontSize: '14px', fontWeight: '800', color: '#0B1F3A', marginBottom: '6px' }}>Téléphone</label>
                <input
                  type="text"
                  value={profile.phone}
                  onChange={e => setProfile({...profile, phone: e.target.value})}
                  style={{ width: '100%', padding: '12px', border: '2px solid #cbd5e1', borderRadius: '10px', fontSize: '14px', fontWeight: '600', color: '#0B1F3A', boxSizing: 'border-box' }}
                />
              </div>
            </div>

            <div>
              <label style={{ display: 'block', fontSize: '14px', fontWeight: '800', color: '#0B1F3A', marginBottom: '6px' }}>Profil README / Markdown</label>
              <textarea
                rows={10}
                value={profile.readme_content}
                onChange={e => setProfile({...profile, readme_content: e.target.value})}
                style={{ width: '100%', padding: '12px', border: '2px solid #cbd5e1', borderRadius: '10px', fontFamily: 'monospace', fontSize: '14px', fontWeight: '600', color: '#0B1F3A', boxSizing: 'border-box' }}
              ></textarea>
            </div>
          </div>
        )}

        {activeTab === 'plans' && (
          <div style={{ maxWidth: '1024px', margin: '0 auto', display: 'flex', flexDirection: 'column', gap: '32px' }}>
            <div style={{ textAlign: 'center' }}>
              <h2 style={{ fontSize: '28px', fontWeight: '900', color: '#0B1F3A', margin: 0 }}>Formules d'Abonnement & Crédits</h2>
              <p style={{ color: '#444441', fontWeight: '600', marginTop: '8px' }}>Choisissez votre formule et payez instantanément via Mobile Money (Airtel, MTN, PayDunya).</p>
            </div>

            {paymentSuccessMsg && (
              <div style={{ backgroundColor: '#ecfdf5', border: '1px solid #6ee7b7', padding: '16px', borderRadius: '12px', color: '#065f46', fontWeight: '800', fontSize: '14px', textAlign: 'center' }}>
                {paymentSuccessMsg}
              </div>
            )}

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '20px' }}>
              <div style={{ backgroundColor: '#ffffff', padding: '24px', borderRadius: '16px', border: selectedPlan === 1 ? '3px solid #185FA5' : '1px solid #cbd5e1', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
                <div>
                  <span style={{ fontSize: '11px', fontWeight: '900', backgroundColor: '#f1f5f9', color: '#0B1F3A', padding: '4px 12px', borderRadius: '12px', textTransform: 'uppercase' }}>Découverte</span>
                  <h3 style={{ fontSize: '22px', fontWeight: '800', color: '#0B1F3A', marginTop: '16px' }}>Gratuit</h3>
                  <p style={{ fontSize: '28px', fontWeight: '900', color: '#185FA5', marginTop: '8px' }}>0 FCFA</p>
                </div>
                <button onClick={() => setSelectedPlan(1)} style={{ marginTop: '24px', width: '100%', border: '2px solid #185FA5', backgroundColor: 'transparent', color: '#185FA5', fontWeight: '800', padding: '12px', borderRadius: '10px', cursor: 'pointer' }}>
                  Sélectionner
                </button>
              </div>

              <div style={{ backgroundColor: '#ffffff', padding: '24px', borderRadius: '16px', border: selectedPlan === 2 ? '3px solid #185FA5' : '1px solid #cbd5e1', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
                <div>
                  <span style={{ fontSize: '11px', fontWeight: '900', backgroundColor: '#e0f2fe', color: '#0369a1', padding: '4px 12px', borderRadius: '12px', textTransform: 'uppercase' }}>Pack 5</span>
                  <h3 style={{ fontSize: '22px', fontWeight: '800', color: '#0B1F3A', marginTop: '16px' }}>Pack 5 Candidatures</h3>
                  <p style={{ fontSize: '28px', fontWeight: '900', color: '#185FA5', marginTop: '8px' }}>2 000 FCFA</p>
                </div>
                <button onClick={() => setSelectedPlan(2)} style={{ marginTop: '24px', width: '100%', backgroundColor: '#185FA5', color: '#ffffff', fontWeight: '800', padding: '12px', borderRadius: '10px', border: 'none', cursor: 'pointer' }}>
                  Sélectionner
                </button>
              </div>

              <div style={{ backgroundColor: '#ffffff', padding: '24px', borderRadius: '16px', border: selectedPlan === 3 ? '3px solid #185FA5' : '1px solid #cbd5e1', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
                <div>
                  <span style={{ fontSize: '11px', fontWeight: '900', backgroundColor: '#f3e8ff', color: '#7e22ce', padding: '4px 12px', borderRadius: '12px', textTransform: 'uppercase' }}>Illimité</span>
                  <h3 style={{ fontSize: '22px', fontWeight: '800', color: '#0B1F3A', marginTop: '16px' }}>Illimité Mensuel</h3>
                  <p style={{ fontSize: '28px', fontWeight: '900', color: '#185FA5', marginTop: '8px' }}>5 000 FCFA</p>
                </div>
                <button onClick={() => setSelectedPlan(3)} style={{ marginTop: '24px', width: '100%', border: '2px solid #185FA5', backgroundColor: 'transparent', color: '#185FA5', fontWeight: '800', padding: '12px', borderRadius: '10px', cursor: 'pointer' }}>
                  Sélectionner
                </button>
              </div>
            </div>

            <div style={{ backgroundColor: '#ffffff', padding: '32px', borderRadius: '16px', border: '1px solid #cbd5e1', maxWidth: '512px', margin: '0 auto', width: '100%', boxSizing: 'border-box', display: 'flex', flexDirection: 'column', gap: '20px' }}>
              <h3 style={{ fontSize: '20px', fontWeight: '900', color: '#0B1F3A', margin: 0 }}>Procéder au paiement Fintech Mobile Money</h3>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                <label style={{ fontSize: '14px', fontWeight: '800', color: '#0B1F3A' }}>Mode de paiement</label>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '8px' }}>
                  <button
                    onClick={() => setPaymentMethod('AIRTEL_MONEY')}
                    style={{ padding: '12px', borderRadius: '10px', border: '2px solid #ef4444', backgroundColor: paymentMethod === 'AIRTEL_MONEY' ? '#fef2f2' : '#ffffff', color: '#b91c1c', fontWeight: '800', fontSize: '12px', cursor: 'pointer' }}
                  >
                    Airtel Money
                  </button>
                  <button
                    onClick={() => setPaymentMethod('MTN_MOMO')}
                    style={{ padding: '12px', borderRadius: '10px', border: '2px solid #eab308', backgroundColor: paymentMethod === 'MTN_MOMO' ? '#fefce8' : '#ffffff', color: '#a16207', fontWeight: '800', fontSize: '12px', cursor: 'pointer' }}
                  >
                    MTN MoMo
                  </button>
                  <button
                    onClick={() => setPaymentMethod('PAYDUNYA')}
                    style={{ padding: '12px', borderRadius: '10px', border: '2px solid #185FA5', backgroundColor: paymentMethod === 'PAYDUNYA' ? '#e0f2fe' : '#ffffff', color: '#185FA5', fontWeight: '800', fontSize: '12px', cursor: 'pointer' }}
                  >
                    PayDunya
                  </button>
                </div>
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '14px', fontWeight: '800', color: '#0B1F3A', marginBottom: '6px' }}>Numéro Mobile Money (+242...)</label>
                <input
                  type="text"
                  value={phoneNumber}
                  onChange={e => setPhoneNumber(e.target.value)}
                  style={{ width: '100%', padding: '12px', border: '2px solid #cbd5e1', borderRadius: '10px', fontSize: '14px', fontWeight: '800', color: '#0B1F3A', boxSizing: 'border-box' }}
                />
              </div>

              <button
                onClick={handlePayment}
                style={{ width: '100%', backgroundColor: '#0F6E56', color: '#ffffff', fontWeight: '900', fontSize: '16px', padding: '16px', borderRadius: '10px', border: 'none', cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px' }}
              >
                <Lock style={{ width: '18px', height: '18px' }} />
                <span>Payer et recharger mes crédits</span>
              </button>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
