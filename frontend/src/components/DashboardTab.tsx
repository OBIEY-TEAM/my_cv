import React, { useState } from 'react';
import { FilePlus, FileText, Edit3, Save, FileEdit, Eye, Download } from 'lucide-react';
import { ApplicationPackage } from '../types';
import { ApiService } from '../services/api';
import { ReusableModal } from './ReusableModal';

interface DashboardTabProps {
  packages: ApplicationPackage[];
  onOpenCreate: () => void;
  onOpenPkgModal: (pkg: ApplicationPackage, type: 'CV' | 'LM' | 'EMAIL' | 'Paiement') => void;
  onRefresh?: () => void;
}

const DEFAULT_DEMO_PACKAGE: ApplicationPackage = {
  id: 1,
  job_offer: {
    title: 'Ingénieur Logiciel Fullstack',
    company: 'Tech Congo',
    site_category: 'ACPE',
    abbreviation: 'DEV-FULLSTACK'
  },
  cv_text: 'Ingénieur Logiciel et Consultant IT expérimenté en Python, React, Flutter et Architecture Cloud.',
  lm_text: "A l'attention du Recruteur\nTech Congo\n\nOBJET : Candidature au poste d'Ingénieur Logiciel Fullstack\n\nMadame, Monsieur,\n\nC'est avec un grand intérêt que je vous présente ma candidature...",
  email_text: "Objet : Candidature au poste d'Ingénieur Logiciel Fullstack\n\nMadame, Monsieur,\n\nVeuillez trouver ci-joint mon dossier de candidature.\n\nCordialement,",
  cv_pdf: 'https://example.com/cv.pdf',
  cover_letter_pdf: 'https://example.com/lm.pdf',
  email_txt: 'https://example.com/email.txt',
  zip_package: 'https://example.com/package.zip',
  created_at: new Date().toISOString(),
  payment_status: 'approuved',
  processing_status: 'finalized'
};

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
  const [showPreviewModal, setShowPreviewModal] = useState(false);

  const displayPackages = packages.length > 0 ? packages : [DEFAULT_DEMO_PACKAGE];

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

  const getCurrentDocUrl = () => {
    if (!editingPkg) return '#';
    return activeTab === 'LM' ? editingPkg.cover_letter_pdf : editingPkg.cv_pdf;
  };

  const getCurrentTextPreview = () => {
    if (activeTab === 'CV') return cvText;
    if (activeTab === 'LM') return lmText;
    return emailText;
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

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(360px, 1fr))', gap: '20px' }}>
        {displayPackages.map((pkg) => (
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

      {/* WORD-STYLE APPLICATION EDITOR REUSABLE MODAL */}
      {editingPkg && (
        <ReusableModal
          isOpen={!!editingPkg}
          onClose={() => setEditingPkg(null)}
          title={`Éditeur Word - ${editingPkg.job_offer.title}`}
          subtitle="Modifiez le contenu puis enregistrez pour régénérer le PDF sur mesure."
          headerBg="#185FA5"
          headerIcon={<FileEdit style={{ width: '22px', height: '22px' }} />}
          maxWidth="850px"
          footerButtons={
            <>
              <button
                type="button"
                onClick={() => setEditingPkg(null)}
                style={{ padding: '10px 18px', borderRadius: '8px', border: '1px solid #cbd5e1', backgroundColor: '#fff', fontWeight: '800', cursor: 'pointer' }}
              >
                Annuler
              </button>
              <button
                type="button"
                onClick={() => setShowPreviewModal(true)}
                style={{ padding: '10px 18px', borderRadius: '8px', border: '1px solid #0B1F3A', backgroundColor: '#0B1F3A', color: '#fff', fontWeight: '800', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '6px' }}
              >
                <Eye style={{ width: '16px', height: '16px' }} />
                <span>Aperçu PDF</span>
              </button>
              <button
                type="button"
                onClick={handleSaveEdit}
                disabled={isSaving}
                style={{ padding: '10px 20px', borderRadius: '8px', border: 'none', backgroundColor: '#0F6E56', color: '#fff', fontWeight: '900', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '6px' }}
              >
                <Save style={{ width: '16px', height: '16px' }} />
                <span>{isSaving ? 'Régénération...' : 'Enregistrer & Régénérer le PDF'}</span>
              </button>
            </>
          }
        >
          {/* TAB SELECTOR FOR CV, LM, EMAIL */}
          <div style={{ display: 'flex', borderBottom: '1px solid #cbd5e1', backgroundColor: '#f8fafc', marginBottom: '16px', borderRadius: '8px', overflow: 'hidden' }}>
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
          <div style={{ flex: 1 }}>
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
        </ReusableModal>
      )}

      {/* REUSABLE PDF PREVIEW MODAL */}
      {showPreviewModal && editingPkg && (
        <ReusableModal
          isOpen={showPreviewModal}
          onClose={() => setShowPreviewModal(false)}
          title={`Aperçu PDF - ${activeTab} (${editingPkg.job_offer.title})`}
          subtitle="Prévisualisation en direct du document rédigé par Luka Mossala"
          headerBg="#0B1F3A"
          headerIcon={<Eye style={{ width: '22px', height: '22px' }} />}
          maxWidth="800px"
          footerButtons={
            <>
              <button
                type="button"
                onClick={() => window.open(getCurrentDocUrl(), '_blank')}
                style={{ padding: '10px 18px', borderRadius: '8px', border: '1px solid #0B1F3A', backgroundColor: '#0B1F3A', color: '#fff', fontWeight: '800', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '6px' }}
              >
                <Download style={{ width: '16px', height: '16px' }} />
                <span>Télécharger le PDF</span>
              </button>
              <button
                type="button"
                onClick={() => setShowPreviewModal(false)}
                style={{ padding: '10px 18px', borderRadius: '8px', border: 'none', backgroundColor: '#185FA5', color: '#fff', fontWeight: '800', cursor: 'pointer' }}
              >
                Fermer l'Aperçu
              </button>
            </>
          }
        >
          <div style={{ backgroundColor: '#f1f5f9', padding: '20px', borderRadius: '12px', border: '1px solid #cbd5e1', minHeight: '300px' }}>
            <div style={{ backgroundColor: '#ffffff', padding: '24px', borderRadius: '8px', boxShadow: '0 4px 6px -1px rgba(0,0,0,0.1)', fontFamily: 'serif', whiteSpace: 'pre-wrap', lineHeight: '1.7', color: '#1e293b' }}>
              <h3 style={{ margin: '0 0 16px', fontFamily: 'sans-serif', color: '#0B1F3A', borderBottom: '2px solid #0B1F3A', paddingBottom: '8px' }}>
                DOCUMENT : {activeTab} - {editingPkg.job_offer.title}
              </h3>
              {getCurrentTextPreview()}
            </div>
          </div>
        </ReusableModal>
      )}
    </div>
  );
};
