import React from 'react';
import { Briefcase, Sparkles, User, CreditCard } from 'lucide-react';

export type TabType = 'dashboard' | 'profile' | 'create' | 'plans';

interface NavigationProps {
  activeTab: TabType;
  setActiveTab: (tab: TabType) => void;
  onTabChange?: () => void;
}

export const Navigation: React.FC<NavigationProps> = ({ activeTab, setActiveTab, onTabChange }) => {
  const tabs = [
    { id: 'dashboard' as TabType, label: 'Mes Candidatures', icon: Briefcase },
    { id: 'create' as TabType, label: 'Générer un Dossier', icon: Sparkles },
    { id: 'profile' as TabType, label: 'Profil Structuré', icon: User },
    { id: 'plans' as TabType, label: 'Abonnements & Crédits', icon: CreditCard },
  ];

  return (
    <div style={{ backgroundColor: '#ffffff', borderBottom: '1px solid #e2e8f0' }}>
      <div style={{ maxWidth: '1280px', margin: '0 auto', padding: '0 24px', display: 'flex', gap: '24px' }}>
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => {
              setActiveTab(tab.id);
              if (onTabChange) onTabChange();
            }}
            style={{
              display: 'flex', alignItems: 'center', gap: '8px', padding: '16px 0', border: 'none',
              borderBottom: activeTab === tab.id ? '3px solid #185FA5' : '3px solid transparent',
              backgroundColor: 'transparent', color: activeTab === tab.id ? '#185FA5' : '#444441',
              fontWeight: activeTab === tab.id ? '900' : '700', fontSize: '14px', cursor: 'pointer'
            }}
          >
            <tab.icon style={{ width: '18px', height: '18px' }} />
            <span>{tab.label}</span>
          </button>
        ))}
      </div>
    </div>
  );
};
