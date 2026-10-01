import React, { useState, useEffect } from 'react';
import { ApiService, setAuthToken } from './services/api';
import {
  ProfileData, UserInfo, Experience, Certification, Education,
  Project, ApplicationPackage, SubscriptionPlan, SubscriptionData
} from './types';
import { Header } from './components/Header';
import { Navigation, TabType } from './components/Navigation';
import { LoginScreen } from './components/LoginScreen';
import { DashboardTab } from './components/DashboardTab';
import { CreateApplicationTab } from './components/CreateApplicationTab';
import { ProfileTab } from './components/ProfileTab';
import { PaymentsTab } from './components/PaymentsTab';
import {
  PhotoModal, PackageModal, ExperienceModal,
  CertificationModal, EducationModal, ProjectModal
} from './components/Modals';

export default function App() {
  const [activeTab, setActiveTab] = useState<TabType>('dashboard');
  const [token, setToken] = useState<string | null>(localStorage.getItem('token'));

  const [profile, setProfile] = useState<ProfileData>({
    title: 'Consultant IT & Expert Fullstack',
    phone: '+242 06 613 01 18',
    cities: 'Brazzaville & Pointe-Noire, Congo',
    readme_content: '',
    cropped_photo: null,
    original_photo: null
  });

  const [userInfo, setUserInfo] = useState<UserInfo>({
    first_name: 'Christ Dany',
    last_name: 'Obiey',
    gender: 'MALE',
    birth_date: '1995-05-10',
    primary_phone: '+242 06 613 01 18',
    secondary_phone: '',
    professional_summary: 'Consultant IT & Expert Fullstack.',
    address: 'Avenue de l\'Indépendance',
    country: 'Congo',
    district: 'Poto-Poto',
    neighborhood: 'Centre'
  });

  const [experiences, setExperiences] = useState<Experience[]>([]);
  const [certifications, setCertifications] = useState<Certification[]>([]);
  const [educations, setEducations] = useState<Education[]>([]);
  const [projects, setProjects] = useState<Project[]>([]);
  const [availablePlans, setAvailablePlans] = useState<SubscriptionPlan[]>([]);
  const [packages, setPackages] = useState<ApplicationPackage[]>([]);
  const [subscription, setSubscription] = useState<SubscriptionData>({ credits_remaining: 1, plan: null });

  const [selectedPlan, setSelectedPlan] = useState<number>(1);

  // Modals state
  const [activePkgModal, setActivePkgModal] = useState<{ pkg: ApplicationPackage; type: 'CV' | 'LM' | 'EMAIL' | 'Paiement' } | null>(null);
  const [showPhotoView, setShowPhotoView] = useState(false);

  const [showExpModal, setShowExpModal] = useState(false);
  const [expForm, setExpForm] = useState<Experience>({
    title: '', company: '', industry: 'Informatique', location: '',
    start_date: '2024-01-01', end_date: null, is_current: false, skills_acquired: ''
  });

  const [showCertModal, setShowCertModal] = useState(false);
  const [certForm, setCertForm] = useState<Certification>({
    title: '', year: 2025, institution: '', location: '',
    start_date: null, end_date: null, description: '', pdf_url: ''
  });
  const [certFile, setCertFile] = useState<File | null>(null);

  const [showEduModal, setShowEduModal] = useState(false);
  const [eduForm, setEduForm] = useState<Education>({
    title: '', year: 2024, institution: '', degree_level: 'Licence',
    field_of_study: '', location: '', start_date: null, end_date: null, description: '', skills_acquired: '', pdf_url: ''
  });
  const [eduFile, setEduFile] = useState<File | null>(null);

  const [showProjModal, setShowProjModal] = useState(false);
  const [projForm, setProjForm] = useState<Project>({
    name: '', industry: 'Informatique', beneficiary: '', link_url: '', description: ''
  });

  useEffect(() => {
    if (token) {
      setAuthToken(token);
      fetchData();
    }
  }, [token, activeTab]);

  const fetchData = async () => {
    try {
      const data = await ApiService.fetchAllProfileData();
      setProfile(data.profile);
      if (data.userInfo) setUserInfo(data.userInfo);
      setSubscription(data.subscription);
      setPackages(data.packages);
      setExperiences(data.experiences);
      setCertifications(data.certifications);
      setEducations(data.educations);
      setProjects(data.projects);
      if (data.plans && data.plans.length > 0) {
        setAvailablePlans(data.plans);
        setSelectedPlan(data.plans[0].id);
      }
    } catch (e) {
      console.error("Error fetching data:", e);
    }
  };

  const handleLogout = () => {
    setToken(null);
    setAuthToken(null);
    localStorage.removeItem('token');
  };

  const handlePhotoUpload = async (file: File) => {
    try {
      const updatedProfile = await ApiService.uploadPhoto(file);
      setProfile(updatedProfile);
      alert("Photo de profil mise à jour !");
    } catch (e) {
      alert("Erreur lors du téléchargement de la photo.");
    }
  };

  const handleSaveInfo = async () => {
    try {
      await ApiService.updateUserInfo(userInfo);
      alert("Informations enregistrées avec succès !");
    } catch (e) {
      alert("Erreur lors de l'enregistrement des informations.");
    }
  };

  const handleSaveExperience = async () => {
    try {
      await ApiService.saveExperience(expForm);
      setShowExpModal(false);
      await fetchData();
    } catch (e) {
      alert("Erreur lors de la sauvegarde de l'expérience.");
    }
  };

  const handleDeleteExperience = async (id: number) => {
    if (confirm("Supprimer cette expérience ?")) {
      await ApiService.deleteExperience(id);
      await fetchData();
    }
  };

  const handleSaveCertification = async () => {
    try {
      await ApiService.saveCertification(certForm, certFile);
      setShowCertModal(false);
      setCertFile(null);
      await fetchData();
    } catch (e) {
      alert("Erreur lors de la sauvegarde du certificat.");
    }
  };

  const handleDeleteCertification = async (id: number) => {
    if (confirm("Supprimer ce certificat ?")) {
      await ApiService.deleteCertification(id);
      await fetchData();
    }
  };

  const handleSaveEducation = async () => {
    try {
      await ApiService.saveEducation(eduForm, eduFile);
      setShowEduModal(false);
      setEduFile(null);
      await fetchData();
    } catch (e) {
      alert("Erreur lors de la sauvegarde du diplôme.");
    }
  };

  const handleDeleteEducation = async (id: number) => {
    if (confirm("Supprimer ce diplôme ?")) {
      await ApiService.deleteEducation(id);
      await fetchData();
    }
  };

  const handleSaveProject = async () => {
    try {
      await ApiService.saveProject(projForm);
      setShowProjModal(false);
      await fetchData();
    } catch (e) {
      alert("Erreur lors de la sauvegarde du projet.");
    }
  };

  const handleDeleteProject = async (id: number) => {
    if (confirm("Supprimer ce projet ?")) {
      await ApiService.deleteProject(id);
      await fetchData();
    }
  };

  if (!token) {
    return <LoginScreen onLoginSuccess={(newToken) => { setToken(newToken); fetchData(); }} />;
  }

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#f8fafc', color: '#0B1F3A', fontFamily: 'sans-serif' }}>
      <Header subscription={subscription} onLogout={handleLogout} />
      <Navigation activeTab={activeTab} setActiveTab={setActiveTab} onTabChange={fetchData} />

      <main style={{ maxWidth: '1280px', margin: '0 auto', padding: '32px 24px' }}>
        {activeTab === 'dashboard' && (
          <DashboardTab
            packages={packages}
            onOpenCreate={() => setActiveTab('create')}
            onOpenPkgModal={(pkg, type) => setActivePkgModal({ pkg, type })}
          />
        )}

        {activeTab === 'create' && (
          <CreateApplicationTab
            onSuccess={() => {
              fetchData();
              setActiveTab('dashboard');
            }}
          />
        )}

        {activeTab === 'profile' && (
          <ProfileTab
            profile={profile}
            userInfo={userInfo}
            setUserInfo={setUserInfo}
            experiences={experiences}
            certifications={certifications}
            educations={educations}
            projects={projects}
            onUploadPhoto={handlePhotoUpload}
            onSaveInfo={handleSaveInfo}
            onOpenPhotoView={() => setShowPhotoView(true)}
            onOpenExpModal={(exp) => {
              if (exp) setExpForm(exp);
              else setExpForm({ title: '', company: '', industry: 'Informatique', location: '', start_date: '2024-01-01', end_date: null, is_current: false, skills_acquired: '' });
              setShowExpModal(true);
            }}
            onDeleteExp={handleDeleteExperience}
            onOpenCertModal={(cert) => {
              if (cert) setCertForm(cert);
              else setCertForm({ title: '', year: 2025, institution: '', location: '', start_date: null, end_date: null, description: '', pdf_url: '' });
              setShowCertModal(true);
            }}
            onDeleteCert={handleDeleteCertification}
            onOpenEduModal={(edu) => {
              if (edu) setEduForm(edu);
              else setEduForm({ title: '', year: 2024, institution: '', degree_level: 'Licence', field_of_study: '', location: '', start_date: null, end_date: null, description: '', skills_acquired: '', pdf_url: '' });
              setShowEduModal(true);
            }}
            onDeleteEdu={handleDeleteEducation}
            onOpenProjModal={(proj) => {
              if (proj) setProjForm(proj);
              else setProjForm({ name: '', industry: 'Informatique', beneficiary: '', link_url: '', description: '' });
              setShowProjModal(true);
            }}
            onDeleteProj={handleDeleteProject}
          />
        )}

        {activeTab === 'plans' && (
          <PaymentsTab
            availablePlans={availablePlans}
            selectedPlan={selectedPlan}
            setSelectedPlan={setSelectedPlan}
            onSuccess={fetchData}
          />
        )}
      </main>

      {/* MODALS */}
      {showPhotoView && (
        <PhotoModal photoUrl={profile.cropped_photo} onClose={() => setShowPhotoView(false)} />
      )}

      {activePkgModal && (
        <PackageModal
          activeModal={activePkgModal}
          onClose={() => setActivePkgModal(null)}
          onNavigateToPlans={() => setActiveTab('plans')}
        />
      )}

      {showExpModal && (
        <ExperienceModal
          expForm={expForm}
          setExpForm={setExpForm}
          onClose={() => setShowExpModal(false)}
          onSave={handleSaveExperience}
        />
      )}

      {showCertModal && (
        <CertificationModal
          certForm={certForm}
          setCertForm={setCertForm}
          setCertFile={setCertFile}
          onClose={() => setShowCertModal(false)}
          onSave={handleSaveCertification}
        />
      )}

      {showEduModal && (
        <EducationModal
          eduForm={eduForm}
          setEduForm={setEduForm}
          setEduFile={setEduFile}
          onClose={() => setShowEduModal(false)}
          onSave={handleSaveEducation}
        />
      )}

      {showProjModal && (
        <ProjectModal
          projForm={projForm}
          setProjForm={setProjForm}
          onClose={() => setShowProjModal(false)}
          onSave={handleSaveProject}
        />
      )}
    </div>
  );
}
