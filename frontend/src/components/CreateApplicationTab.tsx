import React, { useState } from 'react';
import { ApiService } from '../services/api';

interface CreateApplicationTabProps {
  onSuccess: () => void;
}

export const CreateApplicationTab: React.FC<CreateApplicationTabProps> = ({ onSuccess }) => {
  const [jobText, setJobText] = useState('');
  const [sourceUrl, setSourceUrl] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);

  const handleGenerate = async () => {
    setIsGenerating(true);
    try {
      await ApiService.generateApplication(jobText, sourceUrl);
      setJobText('');
      setSourceUrl('');
      alert("Document / Candidature généré(e) avec succès par Groq Cloud API !");
      onSuccess();
    } catch (e: any) {
      alert(e?.response?.data?.error || "Erreur lors de la génération.");
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div style={{ maxWidth: '768px', margin: '0 auto', backgroundColor: '#ffffff', padding: '32px', borderRadius: '16px', border: '1px solid #cbd5e1' }}>
      <h2 style={{ fontSize: '22px', fontWeight: '900', color: '#0B1F3A', margin: '0 0 8px' }}>Générer un Dossier Sur Mesure</h2>
      <p style={{ fontSize: '13px', color: '#64748b', marginBottom: '20px' }}>
        Renseignez l'offre d'emploi pour générer le CV (1P), la LM (1P) et l'Email, ou laissez vide pour la <strong>rédaction du CV uniquement</strong>.
      </p>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
        <div>
          <label style={{ display: 'block', fontSize: '13px', fontWeight: '800', color: '#0B1F3A', marginBottom: '6px' }}>Lien URL de l'offre (Optionnel)</label>
          <input type="url" placeholder="https://acpe.cg/emplois/developpeur-fullstack" value={sourceUrl} onChange={e => setSourceUrl(e.target.value)} style={{ width: '100%', padding: '12px', border: '2px solid #cbd5e1', borderRadius: '10px' }} />
        </div>

        <div style={{ textAlign: 'center', fontWeight: '800', fontSize: '12px', color: '#94a3b8' }}>OU</div>

        <div>
          <label style={{ display: 'block', fontSize: '13px', fontWeight: '800', color: '#0B1F3A', marginBottom: '6px' }}>Texte brut de l'offre (Optionnel)</label>
          <textarea rows={6} placeholder="Collez ici l'offre d'emploi (laisser vide pour générer un CV seul)..." value={jobText} onChange={e => setJobText(e.target.value)} style={{ width: '100%', padding: '12px', border: '2px solid #cbd5e1', borderRadius: '10px' }}></textarea>
        </div>

        <button onClick={handleGenerate} disabled={isGenerating} style={{ width: '100%', backgroundColor: '#185FA5', color: '#ffffff', fontWeight: '900', fontSize: '16px', padding: '16px', borderRadius: '10px', border: 'none', cursor: 'pointer' }}>
          {isGenerating ? 'Génération par Groq Cloud AI en cours...' : (!jobText && !sourceUrl ? 'Générer le CV Uniquement (Sans Offre)' : 'Générer CV (1P), LM (1P) & Email')}
        </button>
      </div>
    </div>
  );
};
