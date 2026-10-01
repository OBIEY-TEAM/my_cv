import React, { useState } from 'react';
import { FilePlus, FileText, Edit3, Save, X, FileEdit } from 'lucide-react';
import { ApplicationPackage } from '../types';
import { ApiService } from '../services/api';

interface DashboardTabProps {
  packages: ApplicationPackage[];
  onOpenCreate: () => void;
  onOpenPkgModal: (pkg: ApplicationPackage, type: 'CV' | 'LM' | 'EMAIL' | 'Paiement') => void;
  onRefresh?: () => void;
}

export const DashboardTab: React.FC<DashboardTabProps> = ({
  packages,
  onOpenCreate,
  onOpenPkgModal,
  onRefresh
}) => {
  const [editingPkg, setEditingPkg] = useState<ApplicationPackage | null>(null);
  const [cvText, setCvText] = useState('');
  const [lmText, setLmText] = useState('');
  const [emailText, setEmailText] = useState('');
  const [activeTab, setActiveTab] = useState<'CV' | 'LM' | 'EMAIL'>('CV');
  const [isSaving, setIsSaving] = useState(false);

  const handleOpenEdit = (pkg: ApplicationPackage) => {
    setEditingPkg(pkg);
    setCvText(pkg.cv_text || `Ingénieur Logiciel et Consultant IT pour le poste de ${pkg.job_offer.title}.`);
    setLmText(pkg.lm_text || `A l'attention du Recruteur\n${pkg.job_offer.company}\n\nOBJET : Candidature au poste de ${pkg.job_offer.title}\n\nMadame, Monsieur,\n\nC'est avec un grand intérêt que je pose ma candidature...`);
    setEmailText(pkg.email_text || pkg.email_body || `Objet : Candidature au poste de ${pkg.job_offer.title}\n\nMadame, Monsieur,\n\nVeuillez trouver ci-joint mon dossier de candidature.\n\nCordialement,`);
    setActiveTab('CV');
  };

  const handleSaveEdit = async () => {
    if (!editingPkg) return;
    setIsSaving(true);
    try {
      await ApiService.updatePackageContent(editingPkg.id, {
        cv_text: cvText,
        lm_text: lmText,
        email_text: emailText
      });
      alert("Contenu modifié et PDF régénéré avec succès par Luka Mossala !");
      setEditingPkg(null);
      if (onRefresh) onRefresh();
    } catch (e: any) {
      alert("Erreur lors de la modification et régénération du PDF.");
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h2 style={{ fontSize: '24px', fontWeight: '900', color: '#0B1F3A', margin: 0 }}>Tableau de Bord des Candidatures</h2>
          <p style={{ fontSize: '14px', fontWeight: '600', color: '#444441', marginTop: '4px' }}>Gérez vos dossiers de candidature sur mesure (Générés par Luka Mossala).</p>
        </div>
        <button onClick={onOpenCreate} style={{ backgroundColor: '#185FA5', color: '#ffffff', fontWeight: '800', fontSize: '14px', padding: '12px 20px', borderRadius: '10px', border: 'none', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <FilePlus style={{ width: '18px', height: '18px' }} />
          <span>Générer par Luka Mossala</span>
        </button>
      </div>

      {packages.length === 0 ? (
        <div style={{ backgroundColor: '#ffffff', padding: '48px', borderRadius: '16px', border: '1px solid #cbd5e1', textAlign: 'center' }}>
          <FileText style={{ width: '48px', height: '48px', color: '#94a3b8', margin: '0 auto 16px' }} />
          <h3 style={{ fontSize: '18px', fontWeight: '800', color: '#0B1F3A' }}>Aucune candidature générée pour le moment</h3>
        </div>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(360px, 1fr))', gap: '20px' }}>
          {packages.map((pkg) => (
            <div key={pkg.id} style={{ backgroundColor: '#ffffff', borderRadius: '16px', border: '1px solid #cbd5e1', padding: '20px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                <div>
                  <span style={{ fontSize: '11px', fontWeight: '900', backgroundColor: '#e0f2fe', color: '#0369a1', padding: '4px 10px', borderRadius: '6px', textTransform: 'uppercase' }}>
                    {pkg.job_offer.site_category || 'ACPE'}
                  </span>
                  <h3 style={{ fontSize: '18px', fontWeight: '800', color: '#0B1F3A', margin: '8px 0 2px' }}>{pkg.job_offer.title}</h3>
                  <p style={{ fontSize: '13px', fontWeight: '700', color: '#444441', margin: 0 }}>{pkg.job_offer.company}</p>
                </div>
                <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end', gap: '4px' }}>
                  <span style={{ fontSize: '10px', fontWeight: '800', padding: '2px 8px', borderRadius: '4px', backgroundColor: pkg.payment_status === 'approuved' ? '#dcfce7' : '#fef3c7', color: pkg.payment_status === 'approuved' ? '#166534' : '#92400e' }}>
                    Paiement: {pkg.payment_status}
                  </span>
                  <span style={{ fontSize: '10px', fontWeight: '800', padding: '2px 8px', borderRadius: '4px', backgroundColor: pkg.processing_status === 'finalized' ? '#e0f2fe' : '#fef3c7', color: pkg.processing_status === 'finalized' ? '#075985' : '#92400e' }}>
                    Traitement: {pkg.processing_status}
                  </span>
                </div>
              </div>

              {/* ACTION BUTTONS WITH MODIFIER BUTTON */}
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(5, 1fr)', gap: '6px', borderTop: '1px solid #f1f5f9', paddingTop: '16px' }}>
                <button onClick={() => onOpenPkgModal(pkg, 'CV')} style={{ border: '1px solid #0B1F3A', backgroundColor: '#0B1F3A', color: '#ffffff', fontWeight: '800', fontSize: '11px', padding: '8px 2px', borderRadius: '6px', cursor: 'pointer' }}>
                  CV
                </button>
                <button onClick={() => onOpenPkgModal(pkg, 'LM')} style={{ border: '1px solid #0B1F3A', backgroundColor: '#0B1F3A', color: '#ffffff', fontWeight: '800', fontSize: '11px', padding: '8px 2px', borderRadius: '6px', cursor: 'pointer' }}>
                  LM
                </button>
                <button onClick={() => onOpenPkgModal(pkg, 'EMAIL')} style={{ border: '1px solid #185FA5', backgroundColor: '#185FA5', color: '#ffffff', fontWeight: '800', fontSize: '11px', padding: '8px 2px', borderRadius: '6px', cursor: 'pointer' }}>
                  EMAIL
                </button>
                <button onClick={() => handleOpenEdit(pkg)} style={{ border: '1px solid #d97706', backgroundColor: '#d97706', color: '#ffffff', fontWeight: '800', fontSize: '11px', padding: '8px 2px', borderRadius: '6px', cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '2px' }}>
                  <Edit3 style={{ width: '12px', height: '12px' }} /> Modifier
                </button>
                <button onClick={() => onOpenPkgModal(pkg, 'Paiement')} style={{ border: '1px solid #0F6E56', backgroundColor: '#0F6E56', color: '#ffffff', fontWeight: '800', fontSize: '11px', padding: '8px 2px', borderRadius: '6px', cursor: 'pointer' }}>
                  Payer
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* WORD-STYLE APPLICATION EDITOR MODAL */}
      {editingPkg && (
        <div style={{ position: 'fixed', inset: 0, backgroundColor: 'rgba(0,0,0,0.6)', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '20px', zIndex: 110 }}>
          <div style={{ backgroundColor: '#ffffff', borderRadius: '16px', maxWidth: '800px', width: '100%', maxHeight: '90vh', display: 'flex', flexDirection: 'column', border: '1px solid #cbd5e1', overflow: 'hidden' }}>

            {/* WORD RIBBON HEADER */}
            <div style={{ backgroundColor: '#185FA5', padding: '16px 24px', color: '#ffffff', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                <FileEdit style={{ width: '22px', height: '22px' }} />
                <div>
                  <h3 style={{ margin: 0, fontSize: '18px', fontWeight: '900' }}>Éditeur Word - {editingPkg.job_offer.title}</h3>
                  <p style={{ margin: 0, fontSize: '12px', opacity: 0.9 }}>Modifiez le contenu puis enregistrez pour régénérer le PDF sur mesure.</p>
                </div>
              </div>
              <button onClick={() => setEditingPkg(null)} style={{ background: 'none', border: 'none', color: '#fff', cursor: 'pointer' }}><X style={{ width: '22px', height: '22px' }} /></button>
            </div>

            {/* TAB SELECTOR FOR CV, LM, EMAIL */}
            <div style={{ display: 'flex', borderBottom: '1px solid #cbd5e1', backgroundColor: '#f8fafc' }}>
              <button onClick={() => setActiveTab('CV')} style={{ flex: 1, padding: '12px', border: 'none', borderBottom: activeTab === 'CV' ? '3px solid #185FA5' : 'none', fontWeight: '800', backgroundColor: activeTab === 'CV' ? '#fff' : 'transparent', color: activeTab === 'CV' ? '#185FA5' : '#64748b', cursor: 'pointer' }}>
                1. Contenu du CV
              </button>
              <button onClick={() => setActiveTab('LM')} style={{ flex: 1, padding: '12px', border: 'none', borderBottom: activeTab === 'LM' ? '3px solid #185FA5' : 'none', fontWeight: '800', backgroundColor: activeTab === 'LM' ? '#fff' : 'transparent', color: activeTab === 'LM' ? '#185FA5' : '#64748b', cursor: 'pointer' }}>
                2. Lettre de Motivation (LM)
              </button>
              <button onClick={() => setActiveTab('EMAIL')} style={{ flex: 1, padding: '12px', border: 'none', borderBottom: activeTab === 'EMAIL' ? '3px solid #185FA5' : 'none', fontWeight: '800', backgroundColor: activeTab === 'EMAIL' ? '#fff' : 'transparent', color: activeTab === 'EMAIL' ? '#185FA5' : '#64748b', cursor: 'pointer' }}>
                3. Email de Candidature
              </button>
            </div>

            {/* WORD SIMULATED EDITOR AREA */}
            <div style={{ padding: '24px', overflowY: 'auto', flex: 1 }}>
              {activeTab === 'CV' && (
                <div>
                  <label style={{ display: 'block', fontWeight: '800', fontSize: '13px', marginBottom: '8px', color: '#0B1F3A' }}>Contenu / Résumé du CV (Editable comme Word) :</label>
                  <textarea
                    rows={12}
                    value={cvText}
                    onChange={e => setCvText(e.target.value)}
                    style={{ width: '100%', padding: '16px', border: '2px solid #cbd5e1', borderRadius: '10px', fontFamily: 'sans-serif', fontSize: '14px', lineHeight: '1.6', boxSizing: 'border-box' }}
                  />
                </div>
              )}

              {activeTab === 'LM' && (
                <div>
                  <label style={{ display: 'block', fontWeight: '800', fontSize: '13px', marginBottom: '8px', color: '#0B1F3A' }}>Corps de la Lettre de Motivation (Editable comme Word) :</label>
                  <textarea
                    rows={14}
                    value={lmText}
                    onChange={e => setLmText(e.target.value)}
                    style={{ width: '100%', padding: '16px', border: '2px solid #cbd5e1', borderRadius: '10px', fontFamily: 'sans-serif', fontSize: '14px', lineHeight: '1.6', boxSizing: 'border-box' }}
                  />
                </div>
              )}

              {activeTab === 'EMAIL' && (
                <div>
                  <label style={{ display: 'block', fontWeight: '800', fontSize: '13px', marginBottom: '8px', color: '#0B1F3A' }}>Texte de l'Email de Candidature :</label>
                  <textarea
                    rows={10}
                    value={emailText}
                    onChange={e => setEmailText(e.target.value)}
                    style={{ width: '100%', padding: '16px', border: '2px solid #cbd5e1', borderRadius: '10px', fontFamily: 'sans-serif', fontSize: '14px', lineHeight: '1.6', boxSizing: 'border-box' }}
                  />
                </div>
              )}
            </div>

            {/* MODAL FOOTER */}
            <div style={{ padding: '16px 24px', borderTop: '1px solid #cbd5e1', backgroundColor: '#f8fafc', display: 'flex', justifyContent: 'flex-end', gap: '12px' }}>
              <button onClick={() => setEditingPkg(null)} style={{ padding: '12px 20px', borderRadius: '8px', border: '1px solid #cbd5e1', backgroundColor: '#fff', fontWeight: '800', cursor: 'pointer' }}>
                Annuler
              </button>
              <button onClick={handleSaveEdit} disabled={isSaving} style={{ padding: '12px 24px', borderRadius: '8px', border: 'none', backgroundColor: '#0F6E56', color: '#fff', fontWeight: '900', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '8px' }}>
                <Save style={{ width: '18px', height: '18px' }} />
                <span>{isSaving ? 'Régénération...' : 'Enregistrer & Régénérer le PDF'}</span>
              </button>
            </div>

          </div>
        </div>
      )}
    </div>
  );
};
