import React from 'react';
import { Briefcase, Sparkles, LogOut } from 'lucide-react';
import { SubscriptionData } from '../types';

interface HeaderProps {
  subscription: SubscriptionData;
  onLogout: () => void;
}

export const Header: React.FC<HeaderProps> = ({ subscription, onLogout }) => {
  return (
    <header style={{ backgroundColor: '#0B1F3A', color: '#ffffff', borderBottom: '1px solid #1e293b' }}>
      <div style={{ maxWidth: '1280px', margin: '0 auto', padding: '0 24px', height: '64px', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div style={{ backgroundColor: '#185FA5', padding: '8px', borderRadius: '10px' }}>
            <Briefcase style={{ width: '20px', height: '20px', color: '#ffffff' }} />
          </div>
          <span style={{ fontWeight: '900', fontSize: '18px', color: '#ffffff' }}>Luka Mosala SaaS</span>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', backgroundColor: 'rgba(255, 255, 255, 0.1)', padding: '6px 14px', borderRadius: '20px' }}>
            <Sparkles style={{ width: '16px', height: '16px', color: '#f59e0b' }} />
            <span style={{ fontSize: '13px', fontWeight: '800', color: '#ffffff' }}>{subscription.credits_remaining} Crédit(s)</span>
          </div>
          <button onClick={onLogout} style={{ backgroundColor: 'transparent', border: '1px solid rgba(255, 255, 255, 0.2)', color: '#ffffff', padding: '6px 12px', borderRadius: '8px', fontSize: '12px', cursor: 'pointer' }}>
            <LogOut style={{ width: '14px', height: '14px' }} />
          </button>
        </div>
      </div>
    </header>
  );
};
