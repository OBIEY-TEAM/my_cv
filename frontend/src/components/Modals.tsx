import React from 'react';
import { Eye, Download, CreditCard, X } from 'lucide-react';
import { ApplicationPackage, Experience, Certification, Education, Project } from '../types';

interface PhotoModalProps {
  photoUrl: string | null;
  onClose: () => void;
}

export const PhotoModal: React.FC<PhotoModalProps> = ({ photoUrl, onClose }) => {
  return (
    <div style={{ position: 'fixed', inset: 0, backgroundColor: 'rgba(0,0,0,0.8)', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '20px', zIndex: 100 }}>
      <div style={{ backgroundColor: '#ffffff', padding: '24px', borderRadius: '16px', maxWidth: '400px', width: '100%', textAlign: 'center', display: 'flex', flexDirection: 'column', gap: '16px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <h3 style={{ margin: 0, fontWeight: '900' }}>Aperçu Photo Profil</h3>
          <button onClick={onClose} style={{ border: 'none', backgroundColor: 'transparent', cursor: 'pointer' }}><X style={{ width: '20px', height: '20px' }} /></button>
        </div>
        {photoUrl ? (
          <img src={photoUrl} alt="Photo" style={{ width: '100%', borderRadius: '12px', objectFit: 'cover' }} />
        ) : (
          <p>Aucune photo téléchargée</p>
        )}
      </div>
    </div>
  );
};

interface PackageModalProps {
  activeModal: { pkg: ApplicationPackage; type: 'CV' | 'LM' | 'EMAIL' | 'Paiement' };
  onClose: () => void;
  onNavigateToPlans: () => void;
}

export const PackageModal: React.FC<PackageModalProps> = ({ activeModal, onClose, onNavigateToPlans }) => {
  const { pkg, type } = activeModal;
  const docUrl = type === 'CV' ? pkg.cv_pdf : pkg.cover_letter_pdf;

  return (
    <div style={{ position: 'fixed', inset: 0, backgroundColor: 'rgba(0,0,0,0.5)', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '20px', zIndex: 100 }}>
      <div style={{ backgroundColor: '#ffffff', padding: '24px', borderRadius: '16px', maxWidth: '480px', width: '100%', display: 'flex', flexDirection: 'column', gap: '16px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <h3 style={{ margin: 0, fontWeight: '900', color: '#0B1F3A' }}>{type} - {pkg.job_offer.title}</h3>
          <button onClick={onClose} style={{ border: 'none', backgroundColor: 'transparent', cursor: 'pointer' }}><X style={{ width: '20px', height: '20px' }} /></button>
        </div>

        <div style={{ display: 'flex', gap: '12px', alignItems: 'center', backgroundColor: '#f8fafc', padding: '12px', borderRadius: '8px' }}>
          <span style={{ fontSize: '12px', fontWeight: '800' }}>Status Paiement:</span>
          <span style={{ fontSize: '11px', fontWeight: '900', padding: '2px 8px', borderRadius: '4px', backgroundColor: pkg.payment_status === 'approuved' ? '#dcfce7' : '#fef3c7', color: pkg.payment_status === 'approuved' ? '#166534' : '#92400e' }}>
            {pkg.payment_status}
          </span>
          <span style={{ fontSize: '12px', fontWeight: '800', marginLeft: 'auto' }}>Status Traitement:</span>
          <span style={{ fontSize: '11px', fontWeight: '900', padding: '2px 8px', borderRadius: '4px', backgroundColor: pkg.processing_status === 'finalized' ? '#e0f2fe' : '#fef3c7', color: pkg.processing_status === 'finalized' ? '#075985' : '#92400e' }}>
            {pkg.processing_status}
          </span>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', marginTop: '8px' }}>
          <button onClick={() => window.open(docUrl, '_blank')} style={{ width: '100%', backgroundColor: '#0B1F3A', color: '#ffffff', fontWeight: '800', padding: '12px', borderRadius: '8px', border: 'none', cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px' }}>
            <Eye style={{ width: '16px', height: '16px' }} /> Voir le document
          </button>
          <button onClick={() => window.open(docUrl, '_blank')} style={{ width: '100%', border: '2px solid #0B1F3A', backgroundColor: 'transparent', color: '#0B1F3A', fontWeight: '800', padding: '12px', borderRadius: '8px', cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px' }}>
            <Download style={{ width: '16px', height: '16px' }} /> Télécharger le document
          </button>
          <button onClick={() => { onClose(); onNavigateToPlans(); }} style={{ width: '100%', backgroundColor: '#0F6E56', color: '#ffffff', fontWeight: '800', padding: '12px', borderRadius: '8px', border: 'none', cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px' }}>
            <CreditCard style={{ width: '16px', height: '16px' }} /> Payer / Recharger Crédits
          </button>
        </div>
      </div>
    </div>
  );
};

interface ExpModalProps {
  expForm: Experience;
  setExpForm: React.Dispatch<React.SetStateAction<Experience>>;
  onClose: () => void;
  onSave: () => void;
}

export const ExperienceModal: React.FC<ExpModalProps> = ({ expForm, setExpForm, onClose, onSave }) => {
  return (
    <div style={{ position: 'fixed', inset: 0, backgroundColor: 'rgba(0,0,0,0.5)', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '20px', zIndex: 100 }}>
      <div style={{ backgroundColor: '#ffffff', padding: '24px', borderRadius: '16px', maxWidth: '500px', width: '100%', display: 'flex', flexDirection: 'column', gap: '12px' }}>
        <h3 style={{ margin: 0, fontWeight: '900' }}>Expérience Professionnelle</h3>
        <input type="text" placeholder="Poste occupé *" value={expForm.title} onChange={e => setExpForm({...expForm, title: e.target.value})} style={{ padding: '10px', border: '1px solid #cbd5e1', borderRadius: '8px' }} />
        <input type="text" placeholder="Structure *" value={expForm.company} onChange={e => setExpForm({...expForm, company: e.target.value})} style={{ padding: '10px', border: '1px solid #cbd5e1', borderRadius: '8px' }} />
        <input type="text" placeholder="Secteur d'activité *" value={expForm.industry} onChange={e => setExpForm({...expForm, industry: e.target.value})} style={{ padding: '10px', border: '1px solid #cbd5e1', borderRadius: '8px' }} />
        <input type="text" placeholder="Lieu" value={expForm.location} onChange={e => setExpForm({...expForm, location: e.target.value})} style={{ padding: '10px', border: '1px solid #cbd5e1', borderRadius: '8px' }} />
        <input type="date" value={expForm.start_date} onChange={e => setExpForm({...expForm, start_date: e.target.value})} style={{ padding: '10px', border: '1px solid #cbd5e1', borderRadius: '8px' }} />
        <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
          <input type="checkbox" checked={expForm.is_current} onChange={e => setExpForm({...expForm, is_current: e.target.checked})} />
          <label style={{ fontSize: '12px', fontWeight: '800' }}>Jusqu'à présent</label>
        </div>
        {!expForm.is_current && <input type="date" value={expForm.end_date || ''} onChange={e => setExpForm({...expForm, end_date: e.target.value})} style={{ padding: '10px', border: '1px solid #cbd5e1', borderRadius: '8px' }} />}
        <input type="text" placeholder="Compétences acquises" value={expForm.skills_acquired} onChange={e => setExpForm({...expForm, skills_acquired: e.target.value})} style={{ padding: '10px', border: '1px solid #cbd5e1', borderRadius: '8px' }} />
        <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '8px', marginTop: '12px' }}>
          <button onClick={onClose} style={{ padding: '8px 16px', borderRadius: '8px', border: '1px solid #cbd5e1' }}>Annuler</button>
          <button onClick={onSave} style={{ padding: '8px 16px', borderRadius: '8px', backgroundColor: '#185FA5', color: '#fff', border: 'none' }}>Enregistrer</button>
        </div>
      </div>
    </div>
  );
};

interface CertModalProps {
  certForm: Certification;
  setCertForm: React.Dispatch<React.SetStateAction<Certification>>;
  setCertFile: (file: File | null) => void;
  onClose: () => void;
  onSave: () => void;
}

export const CertificationModal: React.FC<CertModalProps> = ({ certForm, setCertForm, setCertFile, onClose, onSave }) => {
  return (
    <div style={{ position: 'fixed', inset: 0, backgroundColor: 'rgba(0,0,0,0.5)', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '20px', zIndex: 100 }}>
      <div style={{ backgroundColor: '#ffffff', padding: '24px', borderRadius: '16px', maxWidth: '500px', width: '100%', display: 'flex', flexDirection: 'column', gap: '12px' }}>
        <h3 style={{ margin: 0, fontWeight: '900' }}>Certificat & Attestation</h3>
        <input type="text" placeholder="Libellé du certificat *" value={certForm.title} onChange={e => setCertForm({...certForm, title: e.target.value})} style={{ padding: '10px', border: '1px solid #cbd5e1', borderRadius: '8px' }} />
        <input type="number" placeholder="Année *" value={certForm.year} onChange={e => setCertForm({...certForm, year: parseInt(e.target.value) || 2025})} style={{ padding: '10px', border: '1px solid #cbd5e1', borderRadius: '8px' }} />
        <input type="text" placeholder="Institution *" value={certForm.institution} onChange={e => setCertForm({...certForm, institution: e.target.value})} style={{ padding: '10px', border: '1px solid #cbd5e1', borderRadius: '8px' }} />
        <input type="text" placeholder="Lieu" value={certForm.location} onChange={e => setCertForm({...certForm, location: e.target.value})} style={{ padding: '10px', border: '1px solid #cbd5e1', borderRadius: '8px' }} />
        <textarea placeholder="Description" value={certForm.description} onChange={e => setCertForm({...certForm, description: e.target.value})} style={{ padding: '10px', border: '1px solid #cbd5e1', borderRadius: '8px' }}></textarea>
        <div>
          <label style={{ display: 'block', fontSize: '12px', fontWeight: '800', marginBottom: '4px' }}>Certificat PDF (Optionnel - Google Drive)</label>
          <input type="file" accept="application/pdf" onChange={e => setCertFile(e.target.files ? e.target.files[0] : null)} />
        </div>
        <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '8px', marginTop: '12px' }}>
          <button onClick={onClose} style={{ padding: '8px 16px', borderRadius: '8px', border: '1px solid #cbd5e1' }}>Annuler</button>
          <button onClick={onSave} style={{ padding: '8px 16px', borderRadius: '8px', backgroundColor: '#185FA5', color: '#fff', border: 'none' }}>Enregistrer</button>
        </div>
      </div>
    </div>
  );
};

interface EduModalProps {
  eduForm: Education;
  setEduForm: React.Dispatch<React.SetStateAction<Education>>;
  setEduFile: (file: File | null) => void;
  onClose: () => void;
  onSave: () => void;
}

export const EducationModal: React.FC<EduModalProps> = ({ eduForm, setEduForm, setEduFile, onClose, onSave }) => {
  return (
    <div style={{ position: 'fixed', inset: 0, backgroundColor: 'rgba(0,0,0,0.5)', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '20px', zIndex: 100 }}>
      <div style={{ backgroundColor: '#ffffff', padding: '24px', borderRadius: '16px', maxWidth: '500px', width: '100%', display: 'flex', flexDirection: 'column', gap: '12px' }}>
        <h3 style={{ margin: 0, fontWeight: '900' }}>Diplôme</h3>
        <input type="text" placeholder="Libellé du diplôme *" value={eduForm.title} onChange={e => setEduForm({...eduForm, title: e.target.value})} style={{ padding: '10px', border: '1px solid #cbd5e1', borderRadius: '8px' }} />
        <input type="number" placeholder="Année *" value={eduForm.year} onChange={e => setEduForm({...eduForm, year: parseInt(e.target.value) || 2024})} style={{ padding: '10px', border: '1px solid #cbd5e1', borderRadius: '8px' }} />
        <input type="text" placeholder="Institution *" value={eduForm.institution} onChange={e => setEduForm({...eduForm, institution: e.target.value})} style={{ padding: '10px', border: '1px solid #cbd5e1', borderRadius: '8px' }} />
        <input type="text" placeholder="Niveau d'étude (Bac, Licence, Master) *" value={eduForm.degree_level} onChange={e => setEduForm({...eduForm, degree_level: e.target.value})} style={{ padding: '10px', border: '1px solid #cbd5e1', borderRadius: '8px' }} />
        <input type="text" placeholder="Spécialité" value={eduForm.field_of_study} onChange={e => setEduForm({...eduForm, field_of_study: e.target.value})} style={{ padding: '10px', border: '1px solid #cbd5e1', borderRadius: '8px' }} />
        <input type="text" placeholder="Compétences acquises" value={eduForm.skills_acquired} onChange={e => setEduForm({...eduForm, skills_acquired: e.target.value})} style={{ padding: '10px', border: '1px solid #cbd5e1', borderRadius: '8px' }} />
        <div>
          <label style={{ display: 'block', fontSize: '12px', fontWeight: '800', marginBottom: '4px' }}>Diplôme PDF (Optionnel - Google Drive)</label>
          <input type="file" accept="application/pdf" onChange={e => setEduFile(e.target.files ? e.target.files[0] : null)} />
        </div>
        <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '8px', marginTop: '12px' }}>
          <button onClick={onClose} style={{ padding: '8px 16px', borderRadius: '8px', border: '1px solid #cbd5e1' }}>Annuler</button>
          <button onClick={onSave} style={{ padding: '8px 16px', borderRadius: '8px', backgroundColor: '#185FA5', color: '#fff', border: 'none' }}>Enregistrer</button>
        </div>
      </div>
    </div>
  );
};

interface ProjModalProps {
  projForm: Project;
  setProjForm: React.Dispatch<React.SetStateAction<Project>>;
  onClose: () => void;
  onSave: () => void;
}

export const ProjectModal: React.FC<ProjModalProps> = ({ projForm, setProjForm, onClose, onSave }) => {
  return (
    <div style={{ position: 'fixed', inset: 0, backgroundColor: 'rgba(0,0,0,0.5)', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '20px', zIndex: 100 }}>
      <div style={{ backgroundColor: '#ffffff', padding: '24px', borderRadius: '16px', maxWidth: '500px', width: '100%', display: 'flex', flexDirection: 'column', gap: '12px' }}>
        <h3 style={{ margin: 0, fontWeight: '900' }}>Projet</h3>
        <input type="text" placeholder="Nom du projet *" value={projForm.name} onChange={e => setProjForm({...projForm, name: e.target.value})} style={{ padding: '10px', border: '1px solid #cbd5e1', borderRadius: '8px' }} />
        <input type="text" placeholder="Secteur d'activité *" value={projForm.industry} onChange={e => setProjForm({...projForm, industry: e.target.value})} style={{ padding: '10px', border: '1px solid #cbd5e1', borderRadius: '8px' }} />
        <input type="text" placeholder="Bénéficiaire" value={projForm.beneficiary} onChange={e => setProjForm({...projForm, beneficiary: e.target.value})} style={{ padding: '10px', border: '1px solid #cbd5e1', borderRadius: '8px' }} />
        <input type="url" placeholder="Lien d'hébergement" value={projForm.link_url} onChange={e => setProjForm({...projForm, link_url: e.target.value})} style={{ padding: '10px', border: '1px solid #cbd5e1', borderRadius: '8px' }} />
        <textarea placeholder="Description" value={projForm.description} onChange={e => setProjForm({...projForm, description: e.target.value})} style={{ padding: '10px', border: '1px solid #cbd5e1', borderRadius: '8px' }}></textarea>
        <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '8px', marginTop: '12px' }}>
          <button onClick={onClose} style={{ padding: '8px 16px', borderRadius: '8px', border: '1px solid #cbd5e1' }}>Annuler</button>
          <button onClick={onSave} style={{ padding: '8px 16px', borderRadius: '8px', backgroundColor: '#185FA5', color: '#fff', border: 'none' }}>Enregistrer</button>
        </div>
      </div>
    </div>
  );
};
