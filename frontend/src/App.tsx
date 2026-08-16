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
      <div className="min-h-screen bg-slate-900 flex items-center justify-center p-4">
        <div className="bg-white p-8 rounded-2xl shadow-2xl max-w-md w-full border border-slate-200">
          <div className="flex items-center space-x-3 mb-6">
            <Sparkles className="w-8 h-8 text-blue-700" />
            <h1 className="text-2xl font-black text-slate-900">AI JobApply SaaS</h1>
          </div>
          <p className="text-sm font-medium text-slate-700 mb-6">Connectez-vous pour générer vos candidatures sur mesure en 1-clic.</p>
          <form onSubmit={handleLogin} className="space-y-4">
            <div>
              <label className="block text-sm font-bold text-slate-900 mb-1">Nom d'utilisateur</label>
              <input
                type="text"
                value={username}
                onChange={e => setUsername(e.target.value)}
                className="w-full p-3 border-2 border-slate-300 rounded-xl text-slate-900 font-bold focus:border-blue-700 focus:outline-none"
              />
            </div>
            <div>
              <label className="block text-sm font-bold text-slate-900 mb-1">Mot de passe</label>
              <input
                type="password"
                value={password}
                onChange={e => setPassword(e.target.value)}
                className="w-full p-3 border-2 border-slate-300 rounded-xl text-slate-900 font-bold focus:border-blue-700 focus:outline-none"
              />
            </div>
            <button type="submit" className="w-full bg-blue-700 hover:bg-blue-800 text-white font-extrabold text-base p-3.5 rounded-xl shadow-lg transition">
              Se connecter / S'inscrire
            </button>
          </form>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-100 flex flex-col font-sans">
      <header className="bg-slate-900 text-white shadow-lg sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <Sparkles className="w-7 h-7 text-sky-400" />
            <span className="font-extrabold text-xl tracking-tight text-white">AI JobApply <span className="text-sky-400">SaaS</span></span>
          </div>

          <nav className="flex space-x-2 sm:space-x-4">
            <button
              onClick={() => setActiveTab('dashboard')}
              className={`px-4 py-2 rounded-xl text-sm font-extrabold transition ${activeTab === 'dashboard' ? 'bg-blue-700 text-white shadow-md' : 'text-slate-200 hover:bg-slate-800'}`}
            >
              Tableau de bord
            </button>
            <button
              onClick={() => setActiveTab('create')}
              className={`px-4 py-2 rounded-xl text-sm font-extrabold transition ${activeTab === 'create' ? 'bg-blue-700 text-white shadow-md' : 'text-slate-200 hover:bg-slate-800'}`}
            >
              Nouvelle Candidature
            </button>
            <button
              onClick={() => setActiveTab('profile')}
              className={`px-4 py-2 rounded-xl text-sm font-extrabold transition ${activeTab === 'profile' ? 'bg-blue-700 text-white shadow-md' : 'text-slate-200 hover:bg-slate-800'}`}
            >
              Mon Profil
            </button>
            <button
              onClick={() => setActiveTab('plans')}
              className={`px-4 py-2 rounded-xl text-sm font-extrabold transition ${activeTab === 'plans' ? 'bg-blue-700 text-white shadow-md' : 'text-slate-200 hover:bg-slate-800'}`}
            >
              Abonnements ({subscription.credits_remaining})
            </button>
          </nav>
        </div>
      </header>

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 py-8">
        {activeTab === 'dashboard' && (
          <div className="space-y-6">
            <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-300 flex flex-col md:flex-row items-center justify-between gap-4">
              <div>
                <h2 className="text-2xl font-black text-slate-900">Bienvenue, Christ Dany OBIEY 👋</h2>
                <p className="text-slate-700 font-medium mt-1">Générez des dossiers de candidature sur mesure (CV 1-Page & LM 1-Page) en quelques secondes.</p>
              </div>
              <div className="flex items-center space-x-3 bg-blue-50 border-2 border-blue-200 px-5 py-3 rounded-2xl">
                <ShieldCheck className="w-7 h-7 text-blue-700" />
                <div>
                  <p className="text-xs text-blue-800 font-extrabold uppercase">Solde Actuel</p>
                  <p className="text-xl font-black text-blue-900">{subscription.credits_remaining} Crédit(s)</p>
                </div>
              </div>
            </div>

            <h3 className="text-xl font-extrabold text-slate-900 mt-8">Historique des candidatures générées</h3>

            {packages.length === 0 ? (
              <div className="bg-white p-12 text-center rounded-2xl border-2 border-dashed border-slate-300">
                <Briefcase className="w-12 h-12 text-slate-500 mx-auto mb-3" />
                <p className="text-slate-700 font-extrabold text-lg">Aucune candidature générée pour le moment.</p>
                <button
                  onClick={() => setActiveTab('create')}
                  className="mt-4 inline-flex items-center space-x-2 bg-blue-700 hover:bg-blue-800 text-white px-6 py-3 rounded-xl font-extrabold shadow-md transition"
                >
                  <Sparkles className="w-5 h-5 text-sky-300" />
                  <span>Créer ma première candidature</span>
                </button>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {packages.map(pkg => (
                  <div key={pkg.id} className="bg-white p-5 rounded-2xl border border-slate-300 shadow-sm space-y-3">
                    <div className="flex items-start justify-between">
                      <div>
                        <span className="text-xs font-black bg-blue-100 text-blue-900 px-3 py-1 rounded-full uppercase">
                          {pkg.job_offer.site_category}
                        </span>
                        <h4 className="font-extrabold text-slate-900 text-lg mt-2">{pkg.job_offer.title}</h4>
                        <p className="text-sm font-bold text-slate-600">{pkg.job_offer.company}</p>
                      </div>
                    </div>
                    <div className="border-t border-slate-200 pt-3 flex flex-wrap gap-2">
                      <a href={pkg.cv_pdf} target="_blank" rel="noreferrer" className="text-xs bg-slate-800 hover:bg-slate-900 text-white font-extrabold px-3 py-2 rounded-xl flex items-center space-x-1">
                        <FileText className="w-4 h-4 text-sky-400" />
                        <span>CV (1 Page)</span>
                      </a>
                      <a href={pkg.cover_letter_pdf} target="_blank" rel="noreferrer" className="text-xs bg-slate-800 hover:bg-slate-900 text-white font-extrabold px-3 py-2 rounded-xl flex items-center space-x-1">
                        <FileText className="w-4 h-4 text-sky-400" />
                        <span>LM (1 Page)</span>
                      </a>
                      <a href={pkg.zip_package} download className="text-xs bg-blue-700 hover:bg-blue-800 text-white font-extrabold px-3 py-2 rounded-xl flex items-center space-x-1 ml-auto">
                        <Download className="w-4 h-4" />
                        <span>Télécharger ZIP</span>
                      </a>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {activeTab === 'create' && (
          <div className="max-w-3xl mx-auto bg-white p-8 rounded-2xl border border-slate-300 shadow-md space-y-6">
            <div>
              <h2 className="text-2xl font-black text-slate-900">Générer un dossier de candidature sur mesure</h2>
              <p className="text-sm font-medium text-slate-700 mt-1">Collez l'URL de l'offre d'emploi ou son texte brut. L'IA adaptera automatiquement votre profil README.</p>
            </div>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-extrabold text-slate-900 mb-1">Lien de l'offre d'emploi (URL)</label>
                <input
                  type="url"
                  placeholder="https://www.acpe.cg/details-offre-emplois/4200"
                  value={sourceUrl}
                  onChange={e => setSourceUrl(e.target.value)}
                  className="w-full p-3 border-2 border-slate-300 rounded-xl font-bold text-slate-900 focus:border-blue-700 outline-none text-sm"
                />
              </div>

              <div className="relative flex py-1 items-center">
                <div className="flex-grow border-t border-slate-300"></div>
                <span className="flex-shrink mx-4 text-xs font-black text-slate-500 uppercase">OU</span>
                <div className="flex-grow border-t border-slate-300"></div>
              </div>

              <div>
                <label className="block text-sm font-extrabold text-slate-900 mb-1">Texte brut de l'offre d'emploi</label>
                <textarea
                  rows={6}
                  placeholder="Collez ici l'intitulé du poste, le nom de l'entreprise, les missions et compétences requises..."
                  value={jobText}
                  onChange={e => setJobText(e.target.value)}
                  className="w-full p-3 border-2 border-slate-300 rounded-xl font-bold text-slate-900 focus:border-blue-700 outline-none text-sm"
                ></textarea>
              </div>

              <button
                onClick={handleGenerateApplication}
                disabled={isGenerating}
                className="w-full bg-blue-700 hover:bg-blue-800 text-white font-black p-4 rounded-xl shadow-lg transition flex items-center justify-center space-x-2 text-base"
              >
                {isGenerating ? (
                  <>
                    <RefreshCw className="w-5 h-5 animate-spin" />
                    <span>Génération de votre dossier en cours (IA & PDF Engine)...</span>
                  </>
                ) : (
                  <>
                    <Sparkles className="w-5 h-5 text-sky-300" />
                    <span>Générer CV (1 Page), LM (1 Page) & Email TXT</span>
                  </>
                )}
              </button>
            </div>
          </div>
        )}

        {activeTab === 'profile' && (
          <div className="max-w-4xl mx-auto bg-white p-8 rounded-2xl border border-slate-300 shadow-md space-y-6">
            <div>
              <h2 className="text-2xl font-black text-slate-900">Gestion de Profil & README de Référence</h2>
              <p className="text-sm font-medium text-slate-700 mt-1">Vos données de référence utilisées par le moteur IA pour rédiger vos candidatures.</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-extrabold text-slate-900 mb-1">Titre Principal</label>
                <input
                  type="text"
                  value={profile.title}
                  onChange={e => setProfile({...profile, title: e.target.value})}
                  className="w-full p-3 border-2 border-slate-300 rounded-xl font-bold text-slate-900 text-sm"
                />
              </div>
              <div>
                <label className="block text-sm font-extrabold text-slate-900 mb-1">Téléphone</label>
                <input
                  type="text"
                  value={profile.phone}
                  onChange={e => setProfile({...profile, phone: e.target.value})}
                  className="w-full p-3 border-2 border-slate-300 rounded-xl font-bold text-slate-900 text-sm"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-extrabold text-slate-900 mb-1">Profil README / Markdown</label>
              <textarea
                rows={10}
                value={profile.readme_content}
                onChange={e => setProfile({...profile, readme_content: e.target.value})}
                className="w-full p-3 border-2 border-slate-300 rounded-xl font-mono text-slate-900 font-bold text-sm"
              ></textarea>
            </div>
          </div>
        )}

        {activeTab === 'plans' && (
          <div className="max-w-5xl mx-auto space-y-8">
            <div className="text-center">
              <h2 className="text-3xl font-black text-slate-900">Formules d'Abonnement & Crédits</h2>
              <p className="text-slate-700 font-medium mt-2">Choisissez votre formule et payez instantanément via Mobile Money (Airtel, MTN, PayDunya).</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className={`bg-white p-6 rounded-2xl border-2 ${selectedPlan === 1 ? 'border-blue-700 ring-2 ring-blue-700' : 'border-slate-300'} shadow-sm flex flex-col justify-between`}>
                <div>
                  <span className="text-xs font-black bg-slate-200 text-slate-900 px-3 py-1 rounded-full uppercase">Découverte</span>
                  <h3 className="text-2xl font-extrabold text-slate-900 mt-4">Gratuit</h3>
                  <p className="text-3xl font-black text-blue-900 mt-2">0 FCFA</p>
                  <ul className="mt-6 space-y-3 text-sm font-bold text-slate-700">
                    <li className="flex items-center space-x-2"><CheckCircle className="w-5 h-5 text-green-600" /><span>1 Candidature offerte</span></li>
                    <li className="flex items-center space-x-2"><CheckCircle className="w-5 h-5 text-green-600" /><span>CV & LM 1-Page stricts</span></li>
                  </ul>
                </div>
                <button onClick={() => setSelectedPlan(1)} className="mt-8 w-full border-2 border-blue-700 text-blue-700 font-extrabold p-3 rounded-xl hover:bg-blue-50 transition">
                  Sélectionner
                </button>
              </div>

              <div className={`bg-white p-6 rounded-2xl border-2 ${selectedPlan === 2 ? 'border-blue-700 ring-2 ring-blue-700' : 'border-slate-300'} shadow-sm flex flex-col justify-between relative`}>
                <span className="absolute -top-3 right-6 bg-blue-700 text-white text-xs font-black px-3 py-1 rounded-full uppercase">Recommandé</span>
                <div>
                  <span className="text-xs font-black bg-blue-100 text-blue-900 px-3 py-1 rounded-full uppercase">Pack 5</span>
                  <h3 className="text-2xl font-extrabold text-slate-900 mt-4">Pack 5 Candidatures</h3>
                  <p className="text-3xl font-black text-blue-900 mt-2">2 000 FCFA</p>
                  <ul className="mt-6 space-y-3 text-sm font-bold text-slate-700">
                    <li className="flex items-center space-x-2"><CheckCircle className="w-5 h-5 text-green-600" /><span>5 Candidatures complètes</span></li>
                    <li className="flex items-center space-x-2"><CheckCircle className="w-5 h-5 text-green-600" /><span>Archive PDF de l'offre</span></li>
                  </ul>
                </div>
                <button onClick={() => setSelectedPlan(2)} className="mt-8 w-full bg-blue-700 text-white font-extrabold p-3.5 rounded-xl hover:bg-blue-800 transition">
                  Sélectionner
                </button>
              </div>

              <div className={`bg-white p-6 rounded-2xl border-2 ${selectedPlan === 3 ? 'border-blue-700 ring-2 ring-blue-700' : 'border-slate-300'} shadow-sm flex flex-col justify-between`}>
                <div>
                  <span className="text-xs font-black bg-purple-100 text-purple-900 px-3 py-1 rounded-full uppercase">Illimité</span>
                  <h3 className="text-2xl font-extrabold text-slate-900 mt-4">Illimité Mensuel</h3>
                  <p className="text-3xl font-black text-blue-900 mt-2">5 000 FCFA <span className="text-xs font-bold text-slate-600">/ mois</span></p>
                  <ul className="mt-6 space-y-3 text-sm font-bold text-slate-700">
                    <li className="flex items-center space-x-2"><CheckCircle className="w-5 h-5 text-green-600" /><span>Candidatures illimitées</span></li>
                    <li className="flex items-center space-x-2"><CheckCircle className="w-5 h-5 text-green-600" /><span>Support prioritaire</span></li>
                  </ul>
                </div>
                <button onClick={() => setSelectedPlan(3)} className="mt-8 w-full border-2 border-blue-700 text-blue-700 font-extrabold p-3 rounded-xl hover:bg-blue-50 transition">
                  Sélectionner
                </button>
              </div>
            </div>

            <div className="bg-white p-8 rounded-2xl border border-slate-300 shadow-md max-w-xl mx-auto space-y-6">
              <h3 className="text-xl font-black text-slate-900">Procéder au paiement Fintech Mobile Money</h3>

              <div className="space-y-3">
                <label className="block text-sm font-extrabold text-slate-900">Sélectionner le mode de paiement</label>
                <div className="grid grid-cols-3 gap-3">
                  <button
                    onClick={() => setPaymentMethod('AIRTEL_MONEY')}
                    className={`p-3 border-2 rounded-xl font-extrabold text-xs flex flex-col items-center space-y-1 ${paymentMethod === 'AIRTEL_MONEY' ? 'border-red-600 bg-red-50 text-red-800' : 'border-slate-300 text-slate-900'}`}
                  >
                    <span>Airtel Money</span>
                  </button>
                  <button
                    onClick={() => setPaymentMethod('MTN_MOMO')}
                    className={`p-3 border-2 rounded-xl font-extrabold text-xs flex flex-col items-center space-y-1 ${paymentMethod === 'MTN_MOMO' ? 'border-yellow-600 bg-yellow-50 text-yellow-900' : 'border-slate-300 text-slate-900'}`}
                  >
                    <span>MTN MoMo</span>
                  </button>
                  <button
                    onClick={() => setPaymentMethod('PAYDUNYA')}
                    className={`p-3 border-2 rounded-xl font-extrabold text-xs flex flex-col items-center space-y-1 ${paymentMethod === 'PAYDUNYA' ? 'border-blue-700 bg-blue-50 text-blue-900' : 'border-slate-300 text-slate-900'}`}
                  >
                    <span>PayDunya / Carte</span>
                  </button>
                </div>
              </div>

              <div>
                <label className="block text-sm font-extrabold text-slate-900 mb-1">Numéro Mobile Money (+242...)</label>
                <input
                  type="text"
                  value={phoneNumber}
                  onChange={e => setPhoneNumber(e.target.value)}
                  className="w-full p-3 border-2 border-slate-300 rounded-xl font-black text-slate-900 text-sm"
                />
              </div>

              <button
                onClick={handlePayment}
                className="w-full bg-green-700 hover:bg-green-800 text-white font-black p-4 rounded-xl shadow-lg transition flex items-center justify-center space-x-2 text-base"
              >
                <Lock className="w-5 h-5 text-white" />
                <span>Payer et recharger mes crédits</span>
              </button>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
