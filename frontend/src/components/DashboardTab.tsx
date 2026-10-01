import React from 'react';
import { Sparkles, FileText } from 'lucide-react';
import { ApplicationPackage } from '../types';

interface DashboardTabProps {
  packages: ApplicationPackage[];
  onOpenCreate: () => void;
  onOpenPkgModal: (pkg: ApplicationPackage, type: 'CV' | 'LM' | 'EMAIL' | 'Paiement') => void;
}

export const DashboardTab: React.FC<DashboardTabProps> = ({
  packages,
  onOpenCreate,
  onOpenPkgModal
}) => {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h2 style={{ fontSize: '24px', fontWeight: '900', color: '#0B1F3A', margin: 0 }}>Tableau de Bord des Candidatures</h2>
          <p style={{ fontSize: '14px', fontWeight: '600', color: '#444441', marginTop: '4px' }}>Gérez vos dossiers de candidature sur mesure prêts à être envoyés.</p>
        </div>
        <button onClick={onOpenCreate} style={{ backgroundColor: '#185FA5', color: '#ffffff', fontWeight: '800', fontSize: '14px', padding: '12px 20px', borderRadius: '10px', border: 'none', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Sparkles style={{ width: '18px', height: '18px' }} />
          <span>Nouvelle Candidature</span>
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

              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '6px', borderTop: '1px solid #f1f5f9', paddingTop: '16px' }}>
                <button onClick={() => onOpenPkgModal(pkg, 'CV')} style={{ border: '1px solid #0B1F3A', backgroundColor: '#0B1F3A', color: '#ffffff', fontWeight: '800', fontSize: '11px', padding: '8px 4px', borderRadius: '6px', cursor: 'pointer' }}>
                  CV
                </button>
                <button onClick={() => onOpenPkgModal(pkg, 'LM')} style={{ border: '1px solid #0B1F3A', backgroundColor: '#0B1F3A', color: '#ffffff', fontWeight: '800', fontSize: '11px', padding: '8px 4px', borderRadius: '6px', cursor: 'pointer' }}>
                  LM
                </button>
                <button onClick={() => onOpenPkgModal(pkg, 'EMAIL')} style={{ border: '1px solid #185FA5', backgroundColor: '#185FA5', color: '#ffffff', fontWeight: '800', fontSize: '11px', padding: '8px 4px', borderRadius: '6px', cursor: 'pointer' }}>
                  EMAIL
                </button>
                <button onClick={() => onOpenPkgModal(pkg, 'Paiement')} style={{ border: '1px solid #0F6E56', backgroundColor: '#0F6E56', color: '#ffffff', fontWeight: '800', fontSize: '11px', padding: '8px 4px', borderRadius: '6px', cursor: 'pointer' }}>
                  Payer
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
