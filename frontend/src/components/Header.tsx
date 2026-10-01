import React from 'react';
import { Sparkles, LogOut, Loader, Globe } from 'lucide-react';
import { SubscriptionData } from '../types';
import { Language, LANGUAGES, translations } from '../i18n';

interface HeaderProps {
  subscription: SubscriptionData;
  language: Language;
  onLanguageChange: (lang: Language) => void;
  onLogout: () => void;
  onOpenLoaderShowcase?: () => void;
}

export const Header: React.FC<HeaderProps> = ({ subscription, language, onLanguageChange, onLogout, onOpenLoaderShowcase }) => {
  const t = translations[language] || translations.fr;

  return (
    <header style={{ backgroundColor: '#FFFFFF', color: '#0B1F3A', borderBottom: '1px solid #e2e8f0', boxShadow: '0 1px 3px rgba(0,0,0,0.05)' }}>
      <div style={{ maxWidth: '1280px', margin: '0 auto', padding: '0 24px', height: '70px', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <img src="/logo_white.jpg" alt="Luka Mosala Logo Web" style={{ height: '48px', objectFit: 'contain' }} />
          <span style={{ fontWeight: '900', fontSize: '20px', color: '#1B365D', letterSpacing: '0.5px' }}>Luka Mosala</span>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          {/* Language Selector */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', backgroundColor: '#f8fafc', border: '1px solid #cbd5e1', padding: '4px 8px', borderRadius: '8px' }}>
            <Globe style={{ width: '16px', height: '16px', color: '#185FA5' }} />
            <select
              value={language}
              onChange={(e) => onLanguageChange(e.target.value as Language)}
              style={{ background: 'transparent', border: 'none', fontWeight: '700', fontSize: '13px', color: '#0F172A', cursor: 'pointer', outline: 'none' }}
            >
              {LANGUAGES.map((lang) => (
                <option key={lang.code} value={lang.code}>
                  {lang.flag} {lang.label}
                </option>
              ))}
            </select>
          </div>

          {onOpenLoaderShowcase && (
            <button
              onClick={onOpenLoaderShowcase}
              style={{ display: 'flex', alignItems: 'center', gap: '6px', backgroundColor: '#f1f5f9', border: '1px solid #cbd5e1', color: '#0F172A', padding: '6px 14px', borderRadius: '20px', fontSize: '13px', fontWeight: '700', cursor: 'pointer', transition: 'all 0.2s' }}>
              <Loader style={{ width: '15px', height: '15px', color: '#d97706' }} />
              <span>{t.loadersAndCode}</span>
            </button>
          )}

          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', backgroundColor: '#fef3c7', border: '1px solid #fde68a', padding: '6px 14px', borderRadius: '20px' }}>
            <Sparkles style={{ width: '16px', height: '16px', color: '#d97706' }} />
            <span style={{ fontSize: '13px', fontWeight: '800', color: '#92400e' }}>{subscription.credits_remaining} {t.credits}</span>
          </div>

          <button onClick={onLogout} title={t.logout} style={{ backgroundColor: '#f8fafc', border: '1px solid #cbd5e1', color: '#64748b', padding: '8px 12px', borderRadius: '8px', fontSize: '12px', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '4px' }}>
            <LogOut style={{ width: '15px', height: '15px' }} />
          </button>
        </div>
      </div>
    </header>
  );
};
