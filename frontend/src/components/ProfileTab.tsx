import React from 'react';
import { Camera, Edit, Upload, Eye, Check, Plus, Trash2 } from 'lucide-react';
import { ProfileData, UserInfo, Experience, Certification, Education, Project } from '../types';

interface ProfileTabProps {
  profile: ProfileData;
  userInfo: UserInfo;
  setUserInfo: React.Dispatch<React.SetStateAction<UserInfo>>;
  experiences: Experience[];
  certifications: Certification[];
  educations: Education[];
  projects: Project[];
  onUploadPhoto: (file: File) => void;
  onSaveInfo: () => void;
  onOpenPhotoView: () => void;
  onOpenExpModal: (exp?: Experience) => void;
  onDeleteExp: (id: number) => void;
  onOpenCertModal: (cert?: Certification) => void;
  onDeleteCert: (id: number) => void;
  onOpenEduModal: (edu?: Education) => void;
  onDeleteEdu: (id: number) => void;
  onOpenProjModal: (proj?: Project) => void;
  onDeleteProj: (id: number) => void;
}

export const ProfileTab: React.FC<ProfileTabProps> = ({
  profile,
  userInfo,
  setUserInfo,
  experiences,
  certifications,
  educations,
  projects,
  onUploadPhoto,
  onSaveInfo,
  onOpenPhotoView,
  onOpenExpModal,
  onDeleteExp,
  onOpenCertModal,
  onDeleteCert,
  onOpenEduModal,
  onDeleteEdu,
  onOpenProjModal,
  onDeleteProj
}) => {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '32px' }}>
      {/* PHOTO DE PROFIL UPLOAD WITH 4 EXPLICIT BUTTONS */}
      <div style={{ backgroundColor: '#ffffff', padding: '24px', borderRadius: '16px', border: '1px solid #cbd5e1', display: 'flex', alignItems: 'center', gap: '24px' }}>
        <div style={{ width: '96px', height: '96px', borderRadius: '50%', overflow: 'hidden', backgroundColor: '#e2e8f0', display: 'flex', alignItems: 'center', justifyContent: 'center', border: '3px solid #185FA5' }}>
          {profile.cropped_photo ? (
            <img src={profile.cropped_photo} alt="Photo profil" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
          ) : (
            <Camera style={{ width: '36px', height: '36px', color: '#64748b' }} />
          )}
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
          <h3 style={{ fontSize: '18px', fontWeight: '900', margin: 0 }}>Photo de Profil Professionnelle</h3>
          <input type="file" accept="image/*" id="photo-input" style={{ display: 'none' }} onChange={e => { if (e.target.files?.[0]) onUploadPhoto(e.target.files[0]); }} />

          <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
            <label htmlFor="photo-input" style={{ backgroundColor: '#185FA5', color: '#ffffff', fontWeight: '800', fontSize: '12px', padding: '8px 14px', borderRadius: '8px', cursor: 'pointer', display: 'inline-flex', alignItems: 'center', gap: '4px' }}>
              <Edit style={{ width: '14px', height: '14px' }} /> Modifier
            </label>
            <label htmlFor="photo-input" style={{ backgroundColor: '#0B1F3A', color: '#ffffff', fontWeight: '800', fontSize: '12px', padding: '8px 14px', borderRadius: '8px', cursor: 'pointer', display: 'inline-flex', alignItems: 'center', gap: '4px' }}>
              <Upload style={{ width: '14px', height: '14px' }} /> Uploader
            </label>
            <label htmlFor="photo-input" style={{ backgroundColor: '#0F6E56', color: '#ffffff', fontWeight: '800', fontSize: '12px', padding: '8px 14px', borderRadius: '8px', cursor: 'pointer', display: 'inline-flex', alignItems: 'center', gap: '4px' }}>
              <Camera style={{ width: '14px', height: '14px' }} /> Caméra
            </label>
            <button onClick={onOpenPhotoView} style={{ backgroundColor: '#f1f5f9', border: '1px solid #cbd5e1', color: '#0B1F3A', fontWeight: '800', fontSize: '12px', padding: '8px 14px', borderRadius: '8px', cursor: 'pointer', display: 'inline-flex', alignItems: 'center', gap: '4px' }}>
              <Eye style={{ width: '14px', height: '14px' }} /> Voir
            </button>
          </div>
        </div>
      </div>

      {/* 1. INFO GENERALE */}
      <div style={{ backgroundColor: '#ffffff', padding: '24px', borderRadius: '16px', border: '1px solid #cbd5e1' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
          <h3 style={{ fontSize: '20px', fontWeight: '900', color: '#0B1F3A', margin: 0 }}>1. Informations Générales</h3>
          <button onClick={onSaveInfo} style={{ backgroundColor: '#0F6E56', color: '#ffffff', fontWeight: '800', padding: '10px 18px', borderRadius: '8px', border: 'none', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '6px' }}>
            <Check style={{ width: '16px', height: '16px' }} /> Enregistrer mes informations
          </button>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '16px' }}>
          <div>
            <label style={{ display: 'block', fontSize: '12px', fontWeight: '800', marginBottom: '4px' }}>Nom *</label>
            <input type="text" value={userInfo.last_name} onChange={e => setUserInfo({...userInfo, last_name: e.target.value})} style={{ width: '100%', padding: '10px', border: '1px solid #cbd5e1', borderRadius: '8px' }} />
          </div>
          <div>
            <label style={{ display: 'block', fontSize: '12px', fontWeight: '800', marginBottom: '4px' }}>Prénom *</label>
            <input type="text" value={userInfo.first_name} onChange={e => setUserInfo({...userInfo, first_name: e.target.value})} style={{ width: '100%', padding: '10px', border: '1px solid #cbd5e1', borderRadius: '8px' }} />
          </div>
          <div>
            <label style={{ display: 'block', fontSize: '12px', fontWeight: '800', marginBottom: '4px' }}>Genre *</label>
            <select value={userInfo.gender} onChange={e => setUserInfo({...userInfo, gender: e.target.value})} style={{ width: '100%', padding: '10px', border: '1px solid #cbd5e1', borderRadius: '8px' }}>
              <option value="MALE">Homme</option>
              <option value="FEMALE">Femme</option>
              <option value="OTHER">Autre</option>
            </select>
          </div>
          <div>
            <label style={{ display: 'block', fontSize: '12px', fontWeight: '800', marginBottom: '4px' }}>Date de naissance *</label>
            <input type="date" value={userInfo.birth_date || ''} onChange={e => setUserInfo({...userInfo, birth_date: e.target.value})} style={{ width: '100%', padding: '10px', border: '1px solid #cbd5e1', borderRadius: '8px' }} />
          </div>
          <div>
            <label style={{ display: 'block', fontSize: '12px', fontWeight: '800', marginBottom: '4px' }}>Numéro principal *</label>
            <input type="text" value={userInfo.primary_phone} onChange={e => setUserInfo({...userInfo, primary_phone: e.target.value})} style={{ width: '100%', padding: '10px', border: '1px solid #cbd5e1', borderRadius: '8px' }} />
          </div>
          <div>
            <label style={{ display: 'block', fontSize: '12px', fontWeight: '800', marginBottom: '4px' }}>Numéro secondaire</label>
            <input type="text" value={userInfo.secondary_phone} onChange={e => setUserInfo({...userInfo, secondary_phone: e.target.value})} style={{ width: '100%', padding: '10px', border: '1px solid #cbd5e1', borderRadius: '8px' }} />
          </div>
          <div>
            <label style={{ display: 'block', fontSize: '12px', fontWeight: '800', marginBottom: '4px' }}>Adresse</label>
            <input type="text" value={userInfo.address} onChange={e => setUserInfo({...userInfo, address: e.target.value})} style={{ width: '100%', padding: '10px', border: '1px solid #cbd5e1', borderRadius: '8px' }} />
          </div>
          <div>
            <label style={{ display: 'block', fontSize: '12px', fontWeight: '800', marginBottom: '4px' }}>Pays</label>
            <input type="text" value={userInfo.country} onChange={e => setUserInfo({...userInfo, country: e.target.value})} style={{ width: '100%', padding: '10px', border: '1px solid #cbd5e1', borderRadius: '8px' }} />
          </div>
          <div>
            <label style={{ display: 'block', fontSize: '12px', fontWeight: '800', marginBottom: '4px' }}>Arrondissement</label>
            <input type="text" value={userInfo.district} onChange={e => setUserInfo({...userInfo, district: e.target.value})} style={{ width: '100%', padding: '10px', border: '1px solid #cbd5e1', borderRadius: '8px' }} />
          </div>
          <div>
            <label style={{ display: 'block', fontSize: '12px', fontWeight: '800', marginBottom: '4px' }}>Quartier</label>
            <input type="text" value={userInfo.neighborhood} onChange={e => setUserInfo({...userInfo, neighborhood: e.target.value})} style={{ width: '100%', padding: '10px', border: '1px solid #cbd5e1', borderRadius: '8px' }} />
          </div>
        </div>

        <div style={{ marginTop: '16px' }}>
          <label style={{ display: 'block', fontSize: '12px', fontWeight: '800', marginBottom: '4px' }}>Résumé professionnel</label>
          <textarea rows={3} value={userInfo.professional_summary} onChange={e => setUserInfo({...userInfo, professional_summary: e.target.value})} style={{ width: '100%', padding: '10px', border: '1px solid #cbd5e1', borderRadius: '8px' }} />
        </div>
      </div>

      {/* 2. EXPERIENCES */}
      <div style={{ backgroundColor: '#ffffff', padding: '24px', borderRadius: '16px', border: '1px solid #cbd5e1' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
          <h3 style={{ fontSize: '20px', fontWeight: '900', color: '#0B1F3A', margin: 0 }}>2. Expériences Professionnelles</h3>
          <button onClick={() => onOpenExpModal()} style={{ backgroundColor: '#185FA5', color: '#ffffff', fontWeight: '800', padding: '10px 18px', borderRadius: '8px', border: 'none', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '6px' }}>
            <Plus style={{ width: '16px', height: '16px' }} /> Ajouter une expérience
          </button>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
          {experiences.map(exp => (
            <div key={exp.id} style={{ padding: '16px', border: '1px solid #e2e8f0', borderRadius: '10px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                <h4 style={{ margin: 0, fontWeight: '800', fontSize: '16px' }}>{exp.title} - <span style={{ color: '#185FA5' }}>{exp.company}</span></h4>
                <p style={{ margin: '4px 0 0', fontSize: '12px', color: '#64748b' }}>{exp.industry} | {exp.location} | {exp.start_date} à {exp.is_current ? 'Présent' : exp.end_date}</p>
              </div>
              <div style={{ display: 'flex', gap: '8px' }}>
                <button onClick={() => onOpenExpModal(exp)} style={{ backgroundColor: '#f1f5f9', border: 'none', padding: '8px', borderRadius: '6px', cursor: 'pointer' }}><Edit style={{ width: '16px', height: '16px' }} /></button>
                <button onClick={() => onDeleteExp(exp.id!)} style={{ backgroundColor: '#fef2f2', color: '#ef4444', border: 'none', padding: '8px', borderRadius: '6px', cursor: 'pointer' }}><Trash2 style={{ width: '16px', height: '16px' }} /></button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* 3. CERTIFICATIONS */}
      <div style={{ backgroundColor: '#ffffff', padding: '24px', borderRadius: '16px', border: '1px solid #cbd5e1' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
          <h3 style={{ fontSize: '20px', fontWeight: '900', color: '#0B1F3A', margin: 0 }}>3. Certifications et Attestations</h3>
          <button onClick={() => onOpenCertModal()} style={{ backgroundColor: '#185FA5', color: '#ffffff', fontWeight: '800', padding: '10px 18px', borderRadius: '8px', border: 'none', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '6px' }}>
            <Plus style={{ width: '16px', height: '16px' }} /> Ajouter un certificat
          </button>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
          {certifications.map(cert => (
            <div key={cert.id} style={{ padding: '16px', border: '1px solid #e2e8f0', borderRadius: '10px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                <h4 style={{ margin: 0, fontWeight: '800', fontSize: '16px' }}>{cert.title} ({cert.year})</h4>
                <p style={{ margin: '4px 0 0', fontSize: '12px', color: '#64748b' }}>{cert.institution} | {cert.location} {cert.pdf_url && <a href={cert.pdf_url} target="_blank" rel="noreferrer" style={{ color: '#0369a1', fontWeight: '800' }}>[Voir PDF Google Drive]</a>}</p>
              </div>
              <div style={{ display: 'flex', gap: '8px' }}>
                <button onClick={() => onOpenCertModal(cert)} style={{ backgroundColor: '#f1f5f9', border: 'none', padding: '8px', borderRadius: '6px', cursor: 'pointer' }}><Edit style={{ width: '16px', height: '16px' }} /></button>
                <button onClick={() => onDeleteCert(cert.id!)} style={{ backgroundColor: '#fef2f2', color: '#ef4444', border: 'none', padding: '8px', borderRadius: '6px', cursor: 'pointer' }}><Trash2 style={{ width: '16px', height: '16px' }} /></button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* 4. DIPLOMES */}
      <div style={{ backgroundColor: '#ffffff', padding: '24px', borderRadius: '16px', border: '1px solid #cbd5e1' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
          <h3 style={{ fontSize: '20px', fontWeight: '900', color: '#0B1F3A', margin: 0 }}>4. Diplômes</h3>
          <button onClick={() => onOpenEduModal()} style={{ backgroundColor: '#185FA5', color: '#ffffff', fontWeight: '800', padding: '10px 18px', borderRadius: '8px', border: 'none', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '6px' }}>
            <Plus style={{ width: '16px', height: '16px' }} /> Ajouter un diplôme
          </button>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
          {educations.map(edu => (
            <div key={edu.id} style={{ padding: '16px', border: '1px solid #e2e8f0', borderRadius: '10px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                <h4 style={{ margin: 0, fontWeight: '800', fontSize: '16px' }}>{edu.title} - {edu.degree_level} ({edu.year})</h4>
                <p style={{ margin: '4px 0 0', fontSize: '12px', color: '#64748b' }}>{edu.institution} {edu.pdf_url && <a href={edu.pdf_url} target="_blank" rel="noreferrer" style={{ color: '#0369a1', fontWeight: '800' }}>[Voir PDF Google Drive]</a>}</p>
              </div>
              <div style={{ display: 'flex', gap: '8px' }}>
                <button onClick={() => onOpenEduModal(edu)} style={{ backgroundColor: '#f1f5f9', border: 'none', padding: '8px', borderRadius: '6px', cursor: 'pointer' }}><Edit style={{ width: '16px', height: '16px' }} /></button>
                <button onClick={() => onDeleteEdu(edu.id!)} style={{ backgroundColor: '#fef2f2', color: '#ef4444', border: 'none', padding: '8px', borderRadius: '6px', cursor: 'pointer' }}><Trash2 style={{ width: '16px', height: '16px' }} /></button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* 5. PROJETS */}
      <div style={{ backgroundColor: '#ffffff', padding: '24px', borderRadius: '16px', border: '1px solid #cbd5e1' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
          <h3 style={{ fontSize: '20px', fontWeight: '900', color: '#0B1F3A', margin: 0 }}>5. Projets</h3>
          <button onClick={() => onOpenProjModal()} style={{ backgroundColor: '#185FA5', color: '#ffffff', fontWeight: '800', padding: '10px 18px', borderRadius: '8px', border: 'none', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '6px' }}>
            <Plus style={{ width: '16px', height: '16px' }} /> Ajouter un projet
          </button>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
          {projects.map(proj => (
            <div key={proj.id} style={{ padding: '16px', border: '1px solid #e2e8f0', borderRadius: '10px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                <h4 style={{ margin: 0, fontWeight: '800', fontSize: '16px' }}>{proj.name} ({proj.industry})</h4>
                <p style={{ margin: '4px 0 0', fontSize: '12px', color: '#64748b' }}>{proj.description}</p>
              </div>
              <div style={{ display: 'flex', gap: '8px' }}>
                <button onClick={() => onOpenProjModal(proj)} style={{ backgroundColor: '#f1f5f9', border: 'none', padding: '8px', borderRadius: '6px', cursor: 'pointer' }}><Edit style={{ width: '16px', height: '16px' }} /></button>
                <button onClick={() => onDeleteProj(proj.id!)} style={{ backgroundColor: '#fef2f2', color: '#ef4444', border: 'none', padding: '8px', borderRadius: '6px', cursor: 'pointer' }}><Trash2 style={{ width: '16px', height: '16px' }} /></button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
