import React, { useState } from 'react';
import { X, Maximize2, Minimize2 } from 'lucide-react';

export interface ReusableModalProps {
  isOpen?: boolean;
  onClose: () => void;
  title: string;
  subtitle?: string;
  headerBg?: string;
  headerIcon?: React.ReactNode;
  children: React.ReactNode;
  footerButtons?: React.ReactNode;
  maxWidth?: string;
  initialFullScreen?: boolean;
}

export const ReusableModal: React.FC<ReusableModalProps> = ({
  isOpen = true,
  onClose,
  title,
  subtitle,
  headerBg = '#185FA5',
  headerIcon,
  children,
  footerButtons,
  maxWidth = '750px',
  initialFullScreen = false,
}) => {
  const [isFullScreen, setIsFullScreen] = useState(initialFullScreen);

  if (!isOpen) return null;

  return (
    <div
      style={{
        position: 'fixed',
        inset: 0,
        backgroundColor: 'rgba(0,0,0,0.65)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: isFullScreen ? '0' : '20px',
        zIndex: 110,
        transition: 'all 0.2s ease-in-out',
      }}
    >
      <div
        style={{
          backgroundColor: '#ffffff',
          borderRadius: isFullScreen ? '0px' : '16px',
          maxWidth: isFullScreen ? '100vw' : maxWidth,
          width: '100%',
          height: isFullScreen ? '100vh' : 'auto',
          maxHeight: isFullScreen ? '100vh' : '90vh',
          display: 'flex',
          flexDirection: 'column',
          border: '1px solid #cbd5e1',
          overflow: 'hidden',
          boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.3)',
          transition: 'all 0.2s ease-in-out',
        }}
      >
        {/* MODAL HEADER */}
        <div
          style={{
            backgroundColor: headerBg,
            padding: '16px 20px',
            color: '#ffffff',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            gap: '12px',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', overflow: 'hidden' }}>
            {headerIcon}
            <div>
              <h3 style={{ margin: 0, fontSize: '18px', fontWeight: '900', color: '#ffffff' }}>{title}</h3>
              {subtitle && <p style={{ margin: 0, fontSize: '12px', opacity: 0.9, color: '#f1f5f9' }}>{subtitle}</p>}
            </div>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <button
              type="button"
              onClick={() => setIsFullScreen(!isFullScreen)}
              title={isFullScreen ? 'Réduire la fenêtre' : 'Agrandir toute la fenêtre (Plein Écran)'}
              style={{
                background: 'rgba(255,255,255,0.15)',
                border: '1px solid rgba(255,255,255,0.3)',
                borderRadius: '6px',
                color: '#fff',
                cursor: 'pointer',
                padding: '6px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
              }}
            >
              {isFullScreen ? <Minimize2 style={{ width: '18px', height: '18px' }} /> : <Maximize2 style={{ width: '18px', height: '18px' }} />}
            </button>
            <button
              type="button"
              onClick={onClose}
              title="Fermer"
              style={{
                background: 'transparent',
                border: 'none',
                color: '#fff',
                cursor: 'pointer',
                padding: '6px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
              }}
            >
              <X style={{ width: '22px', height: '22px' }} />
            </button>
          </div>
        </div>

        {/* MODAL BODY */}
        <div style={{ padding: '20px', overflowY: 'auto', flex: 1, backgroundColor: '#ffffff' }}>
          {children}
        </div>

        {/* MODAL FOOTER */}
        {footerButtons && (
          <div
            style={{
              padding: '14px 20px',
              borderTop: '1px solid #e2e8f0',
              backgroundColor: '#f8fafc',
              display: 'flex',
              justifyContent: 'flex-end',
              alignItems: 'center',
              gap: '12px',
              flexWrap: 'wrap',
            }}
          >
            {footerButtons}
          </div>
        )}
      </div>
    </div>
  );
};
