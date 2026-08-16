import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  Briefcase, FileText, User, CreditCard, Upload, Download,
  Sparkles, CheckCircle, ShieldCheck, Phone, Mail, MapPin,
  Eye, RefreshCw, Scissors, ChevronRight, Lock
} from 'lucide-react';

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

  const [username, setUsername] = useState('obieydany');
  const [password, setPassword] = useState('Password123!');

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
      console.error(e);
    }
  };

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await axios.post('/api/auth/login/', { username, password });
      setToken(res.data.access);
      localStorage.setItem('token', res.data.access);
    } catch (e) {
      try {
        const regRes = await axios.post('/api/auth/register/', {
          username,
          password,
          email: 'obieydany@gmail.com',
          first_name: 'Christ Dany',
          last_name: 'Obiey'
        });
        setToken(regRes.data.access);
        localStorage.setItem('token', regRes.data.access);
      } catch (err) {
        alert("Erreur de connexion");
      }
    }
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
      alert("Dossier de candidature généré avec succès (CV et Lettre 1-Page stricts)!");
      setIsGenerating(false);
      fetchData();
      setActiveTab('dashboard');
    } catch (err: any) {
      setIsGenerating(false);
      if (err.response?.status === 402) {
        alert("Crédits insuffisants. Veuillez souscrire à une formule d'abonnement.");
        setActiveTab('plans');
      } else {
        alert("Erreur lors de la génération.");
      }
    }
  };

  const handlePayment = async () => {
    try {
      const res = await axios.post('/api/subscriptions/pay/', {
        plan_id: selectedPlan,
        payment_method: paymentMethod,
        phone_number: phoneNumber
      });
      alert(`Paiement réussi ! ${res.data.credits_remaining} crédits disponibles.`);
      fetchData();
      setActiveTab('create');
    } catch (e) {
      alert("Erreur de paiement.");
    }
  };

  if (!token) {
    return (
      <div style={{ minHeight: '100vh', backgroundColor: '#0B1F3A', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '16px', fontFamily: 'system-ui, sans-serif' }}>
        <div style={{ backgroundColor: '#ffffff', padding: '32px', borderRadius: '16px', boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.3)', maxWidth: '420px', width: '100%', border: '1px solid #cbd5e1' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '20px' }}>
            <Sparkles style={{ width: '32px', height: '32px', color: '#185FA5' }} />
            <h1 style={{ fontSize: '24px', fontWeight: '900', color: '#0B1F3A', margin: 0 }}>Luka Mosala SaaS</h1>
          </div>
          <p style={{ fontSize: '14px', fontWeight: '600', color: '#444441', marginBottom: '24px' }}>Connectez-vous pour générer vos candidatures sur mesure en 1-clic.</p>
          <form onSubmit={handleLogin} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            <div>
              <label style={{ display: 'block', fontSize: '14px', fontWeight: '700', color: '#0B1F3A', marginBottom: '6px' }}>Nom d'utilisateur</label>
              <input
                type="text"
                value={username}
                onChange={e => setUsername(e.target.value)}
                style={{ width: '100%', padding: '12px', border: '2px solid #cbd5e1', borderRadius: '10px', fontSize: '15px', fontWeight: '600', color: '#0B1F3A', boxSizing: 'border-box' }}
              />
            </div>
            <div>
              <label style={{ display: 'block', fontSize: '14px', fontWeight: '700', color: '#0B1F3A', marginBottom: '6px' }}>Mot de passe</label>
              <input
                type="password"
                value={password}
                onChange={e => setPassword(e.target.value)}
                style={{ width: '100%', padding: '12px', border: '2px solid #cbd5e1', borderRadius: '10px', fontSize: '15px', fontWeight: '600', color: '#0B1F3A', boxSizing: 'border-box' }}
              />
            </div>
            <button
              type="submit"
              style={{ width: '100%', backgroundColor: '#185FA5', color: '#ffffff', fontWeight: '800', fontSize: '16px', padding: '14px', borderRadius: '10px', border: 'none', cursor: 'pointer', boxShadow: '0 4px 12px rgba(24, 95, 165, 0.4)', marginTop: '8px' }}
            >
              Se connecter / S'inscrire
            </button>
          </form>
        </div>
      </div>
    );
  }

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#F1EFE8', display: 'flex', flexDirection: 'column', fontFamily: 'system-ui, sans-serif' }}>
      <header style={{ backgroundColor: '#0B1F3A', color: '#ffffff', boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)', position: 'sticky', top: 0, zIndex: 50 }}>
        <div style={{ maxWidth: '1280px', margin: '0 auto', padding: '0 16px', height: '64px', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <Sparkles style={{ width: '28px', height: '28px', color: '#38bdf8' }} />
            <span style={{ fontWeight: '900', fontSize: '20px', letterSpacing: '-0.5px', color: '#ffffff' }}>Luka Mosala <span style={{ color: '#38bdf8' }}>SaaS</span></span>
          </div>

          <nav style={{ display: 'flex', gap: '8px' }}>
            <button
              onClick={() => setActiveTab('dashboard')}
              style={{ padding: '8px 16px', borderRadius: '10px', fontSize: '14px', fontWeight: '700', cursor: 'pointer', border: 'none', backgroundColor: activeTab === 'dashboard' ? '#185FA5' : 'transparent', color: '#ffffff' }}
            >
              Tableau de bord
            </button>
            <button
              onClick={() => setActiveTab('create')}
              style={{ padding: '8px 16px', borderRadius: '10px', fontSize: '14px', fontWeight: '700', cursor: 'pointer', border: 'none', backgroundColor: activeTab === 'create' ? '#185FA5' : 'transparent', color: '#ffffff' }}
            >
              Nouvelle Candidature
            </button>
            <button
              onClick={() => setActiveTab('profile')}
              style={{ padding: '8px 16px', borderRadius: '10px', fontSize: '14px', fontWeight: '700', cursor: 'pointer', border: 'none', backgroundColor: activeTab === 'profile' ? '#185FA5' : 'transparent', color: '#ffffff' }}
            >
              Mon Profil
            </button>
            <button
              onClick={() => setActiveTab('plans')}
              style={{ padding: '8px 16px', borderRadius: '10px', fontSize: '14px', fontWeight: '700', cursor: 'pointer', border: 'none', backgroundColor: activeTab === 'plans' ? '#185FA5' : 'transparent', color: '#ffffff' }}
            >
              Abonnements ({subscription.credits_remaining})
            </button>
          </nav>
        </div>
      </header>

      <main style={{ flex: 1, maxWidth: '1280px', width: '100%', margin: '0 auto', padding: '32px 16px', boxSizing: 'border-box' }}>
        {activeTab === 'dashboard' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
            <div style={{ backgroundColor: '#ffffff', padding: '24px', borderRadius: '16px', border: '1px solid #cbd5e1', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '16px' }}>
              <div>
                <h2 style={{ fontSize: '24px', fontWeight: '900', color: '#0B1F3A', margin: 0 }}>Bienvenue, Christ Dany OBIEY 👋</h2>
                <p style={{ color: '#444441', fontWeight: '600', marginTop: '6px', fontSize: '15px' }}>Générez des dossiers de candidature sur mesure (CV 1-Page & LM 1-Page) en quelques secondes.</p>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '12px', backgroundColor: '#e0f2fe', border: '2px solid #bae6fd', padding: '12px 20px', borderRadius: '12px' }}>
                <ShieldCheck style={{ width: '28px', height: '28px', color: '#0284c7' }} />
                <div>
                  <p style={{ fontSize: '11px', color: '#0369a1', fontWeight: '800', textTransform: 'uppercase', margin: 0 }}>Solde Actuel</p>
                  <p style={{ fontSize: '18px', fontWeight: '900', color: '#0c4a6e', margin: 0 }}>{subscription.credits_remaining} Crédit(s)</p>
                </div>
              </div>
            </div>

            <h3 style={{ fontSize: '20px', fontWeight: '800', color: '#0B1F3A', marginTop: '16px', marginBottom: '8px' }}>Historique des candidatures générées</h3>

            {packages.length === 0 ? (
              <div style={{ backgroundColor: '#ffffff', padding: '48px', textAlign: 'center', borderRadius: '16px', border: '2px dashed #cbd5e1' }}>
                <Briefcase style={{ width: '48px', height: '48px', color: '#94a3b8', margin: '0 auto 12px' }} />
                <p style={{ color: '#444441', fontWeight: '700', fontSize: '16px' }}>Aucune candidature générée pour le moment.</p>
                <button
                  onClick={() => setActiveTab('create')}
                  style={{ marginTop: '16px', display: 'inline-flex', alignItems: 'center', gap: '8px', backgroundColor: '#185FA5', color: '#ffffff', padding: '12px 24px', borderRadius: '10px', fontWeight: '800', border: 'none', cursor: 'pointer' }}
                >
                  <Sparkles style={{ width: '18px', height: '18px' }} />
                  <span>Créer ma première candidature</span>
                </button>
              </div>
            ) : (
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))', gap: '16px' }}>
                {packages.map(pkg => (
                  <div key={pkg.id} style={{ backgroundColor: '#ffffff', padding: '20px', borderRadius: '16px', border: '1px solid #cbd5e1', display: 'flex', flexDirection: 'column', gap: '12px' }}>
                    <div>
                      <span style={{ fontSize: '11px', fontWeight: '800', backgroundColor: '#e0f2fe', color: '#0369a1', padding: '4px 10px', borderRadius: '12px', textTransform: 'uppercase' }}>
                        {pkg.job_offer.site_category}
                      </span>
                      <h4 style={{ fontWeight: '800', color: '#0B1F3A', fontSize: '18px', marginTop: '8px', marginBottom: '4px' }}>{pkg.job_offer.title}</h4>
                      <p style={{ fontSize: '14px', fontWeight: '600', color: '#444441', margin: 0 }}>{pkg.job_offer.company}</p>
                    </div>
                    <div style={{ borderTop: '1px solid #e2e8f0', paddingTop: '12px', display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
                      <a href={pkg.cv_pdf} target="_blank" rel="noreferrer" style={{ fontSize: '12px', backgroundColor: '#0B1F3A', color: '#ffffff', fontWeight: '800', padding: '8px 12px', borderRadius: '8px', textDecoration: 'none', display: 'inline-flex', alignItems: 'center', gap: '6px' }}>
                        <FileText style={{ width: '14px', height: '14px', color: '#38bdf8' }} />
                        <span>CV (1 Page)</span>
                      </a>
                      <a href={pkg.cover_letter_pdf} target="_blank" rel="noreferrer" style={{ fontSize: '12px', backgroundColor: '#0B1F3A', color: '#ffffff', fontWeight: '800', padding: '8px 12px', borderRadius: '8px', textDecoration: 'none', display: 'inline-flex', alignItems: 'center', gap: '6px' }}>
                        <FileText style={{ width: '14px', height: '14px', color: '#38bdf8' }} />
                        <span>LM (1 Page)</span>
                      </a>
                      <a href={pkg.zip_package} download style={{ fontSize: '12px', backgroundColor: '#0F6E56', color: '#ffffff', fontWeight: '800', padding: '8px 12px', borderRadius: '8px', textDecoration: 'none', display: 'inline-flex', alignItems: 'center', gap: '6px', marginLeft: 'auto' }}>
                        <Download style={{ width: '14px', height: '14px' }} />
                        <span>ZIP</span>
                      </a>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {activeTab === 'create' && (
          <div style={{ maxWidth: '768px', margin: '0 auto', backgroundColor: '#ffffff', padding: '32px', borderRadius: '16px', border: '1px solid #cbd5e1', display: 'flex', flexDirection: 'column', gap: '20px' }}>
            <div>
              <h2 style={{ fontSize: '24px', fontWeight: '900', color: '#0B1F3A', margin: 0 }}>Générer un dossier de candidature sur mesure</h2>
              <p style={{ fontSize: '14px', fontWeight: '600', color: '#444441', marginTop: '6px' }}>Collez l'URL de l'offre d'emploi ou son texte brut. L'IA adaptera automatiquement votre profil README.</p>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
              <div>
                <label style={{ display: 'block', fontSize: '14px', fontWeight: '800', color: '#0B1F3A', marginBottom: '6px' }}>Lien de l'offre d'emploi (URL)</label>
                <input
                  type="url"
                  placeholder="https://www.acpe.cg/details-offre-emplois/4200"
                  value={sourceUrl}
                  onChange={e => setSourceUrl(e.target.value)}
                  style={{ width: '100%', padding: '12px', border: '2px solid #cbd5e1', borderRadius: '10px', fontSize: '14px', fontWeight: '600', color: '#0B1F3A', boxSizing: 'border-box' }}
                />
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '14px', fontWeight: '800', color: '#0B1F3A', marginBottom: '6px' }}>Texte brut de l'offre d'emploi</label>
                <textarea
                  rows={6}
                  placeholder="Collez ici l'intitulé du poste, le nom de l'entreprise, les missions et compétences requises..."
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
                    <RefreshCw style={{ width: '20px', height: '20px' }} />
                    <span>Génération de votre dossier en cours...</span>
                  </>
                ) : (
                  <>
                    <Sparkles style={{ width: '20px', height: '20px', color: '#38bdf8' }} />
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
