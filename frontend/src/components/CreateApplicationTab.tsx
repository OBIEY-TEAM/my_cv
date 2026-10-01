import React, { useState } from 'react';
import { FilePlus } from 'lucide-react';
import { ApiService } from '../services/api';
import { Language, translations } from '../i18n';

interface CreateApplicationTabProps {
  language?: Language;
  onSuccess: () => void;
}

export const CreateApplicationTab: React.FC<CreateApplicationTabProps> = ({ language = 'fr', onSuccess }) => {
  const t = translations[language] || translations.fr;
  const [jobText, setJobText] = useState('');
  const [sourceUrl, setSourceUrl] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);

  const handleGenerate = async () => {
    setIsGenerating(true);
    try {
      await ApiService.generateApplication(jobText, sourceUrl, language);
      setJobText('');
      setSourceUrl('');
      alert("Document / Candidature généré(e) avec succès par Luka Mossala !");
      onSuccess();
    } catch (e: any) {
      alert(e?.response?.data?.error || "Erreur lors de la génération.");
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div style={{ maxWidth: '768px', margin: '0 auto', backgroundColor: '#ffffff', padding: '32px', borderRadius: '16px', border: '1px solid #cbd5e1' }}>
      <h2 style={{ fontSize: '22px', fontWeight: '900', color: '#0B1F3A', margin: '0 0 8px' }}>{t.generateTitle}</h2>
      <p style={{ fontSize: '13px', color: '#64748b', marginBottom: '20px' }}>
        {t.generateSubtitle}
      </p>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
        <div>
          <label style={{ display: 'block', fontSize: '13px', fontWeight: '800', color: '#0B1F3A', marginBottom: '6px' }}>{t.urlLabel}</label>
          <input type="url" placeholder="https://acpe.cg/emplois/developpeur-fullstack" value={sourceUrl} onChange={e => setSourceUrl(e.target.value)} style={{ width: '100%', padding: '12px', border: '2px solid #cbd5e1', borderRadius: '10px' }} />
        </div>

        <div style={{ textAlign: 'center', fontWeight: '800', fontSize: '12px', color: '#94a3b8' }}>{t.or}</div>

        <div>
          <label style={{ display: 'block', fontSize: '13px', fontWeight: '800', color: '#0B1F3A', marginBottom: '6px' }}>{t.textLabel}</label>
          <textarea rows={6} placeholder="..." value={jobText} onChange={e => setJobText(e.target.value)} style={{ width: '100%', padding: '12px', border: '2px solid #cbd5e1', borderRadius: '10px' }}></textarea>
        </div>

        <button onClick={handleGenerate} disabled={isGenerating} style={{ width: '100%', backgroundColor: '#185FA5', color: '#ffffff', fontWeight: '900', fontSize: '16px', padding: '16px', borderRadius: '10px', border: 'none', cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '10px' }}>
          <FilePlus style={{ width: '20px', height: '20px' }} />
          <span>{isGenerating ? t.btnGenerating : t.btnGenerate}</span>
        </button>
      </div>
    </div>
  );
};
