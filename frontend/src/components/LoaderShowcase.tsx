import React, { useState } from 'react';
import { X, Download, Eye, Code, Check, Copy } from 'lucide-react';

interface LoaderShowcaseProps {
  onClose: () => void;
}

const GENERATOR_SOURCE_CODE = `import os
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import imageio

WIDTH, HEIGHT = 600, 400
FPS = 12
DURATION_SEC = 8
TOTAL_FRAMES = FPS * DURATION_SEC  # 96 frames = 8 seconds

# Sample particle positions forming LM monogram...
# Particles (dots, squares, triangles, circles) converge meticulously over 10 seconds max.
# Animate writing of "LUKA MOSSALA" & golden light shimmer.
`;

export const LoaderShowcase: React.FC<LoaderShowcaseProps> = ({ onClose }) => {
  const [activeTab, setActiveTab] = useState<'preview' | 'code'>('preview');
  const [copied, setCopied] = useState(false);
  const [previewModalGif, setPreviewModalGif] = useState<string | null>(null);

  const handleCopyCode = () => {
    navigator.clipboard.writeText(GENERATOR_SOURCE_CODE);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownload = (path: string, filename: string) => {
    const link = document.createElement('a');
    link.href = path;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div style={{
      position: 'fixed', inset: 0, zIndex: 1000,
      backgroundColor: 'rgba(15, 23, 42, 0.75)', backdropFilter: 'blur(4px)',
      display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '20px'
    }}>
      <div style={{
        backgroundColor: '#ffffff', borderRadius: '16px', maxWidth: '900px', width: '100%',
        maxHeight: '90vh', overflowY: 'auto', boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
        display: 'flex', flexDirection: 'column'
      }}>
        {/* Header */}
        <div style={{
          padding: '20px 24px', borderBottom: '1px solid #e2e8f0',
          display: 'flex', alignItems: 'center', justifyContent: 'space-between', backgroundColor: '#f8fafc'
        }}>
          <div>
            <h2 style={{ fontSize: '20px', fontWeight: '800', color: '#0F172A', margin: 0 }}>
              Animations Loader Luka Mosala
            </h2>
            <p style={{ fontSize: '13px', color: '#64748b', margin: '4px 0 0 0' }}>
              Loaders personnalisés Web (Fond Blanc) & Mobile (Fond Noir) - Animation 8s max
            </p>
          </div>
          <button
            onClick={onClose}
            style={{ border: 'none', background: 'transparent', cursor: 'pointer', padding: '8px', color: '#64748b' }}
          >
            <X style={{ width: '20px', height: '20px' }} />
          </button>
        </div>

        {/* Navigation Tabs */}
        <div style={{ display: 'flex', borderBottom: '1px solid #e2e8f0', padding: '0 24px', gap: '24px', backgroundColor: '#ffffff' }}>
          <button
            onClick={() => setActiveTab('preview')}
            style={{
              padding: '14px 0', border: 'none', background: 'transparent', cursor: 'pointer',
              fontWeight: '700', fontSize: '14px',
              color: activeTab === 'preview' ? '#185FA5' : '#64748b',
              borderBottom: activeTab === 'preview' ? '3px solid #185FA5' : '3px solid transparent'
            }}
          >
            Aperçu des Loaders GIF
          </button>
          <button
            onClick={() => setActiveTab('code')}
            style={{
              padding: '14px 0', border: 'none', background: 'transparent', cursor: 'pointer',
              fontWeight: '700', fontSize: '14px', display: 'flex', alignItems: 'center', gap: '6px',
              color: activeTab === 'code' ? '#185FA5' : '#64748b',
              borderBottom: activeTab === 'code' ? '3px solid #185FA5' : '3px solid transparent'
            }}
          >
            <Code style={{ width: '16px', height: '16px' }} />
            <span>Code Source de Génération</span>
          </button>
        </div>

        {/* Content */}
        <div style={{ padding: '24px', flex: 1 }}>
          {activeTab === 'preview' && (
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(350px, 1fr))', gap: '24px' }}>
              {/* Web Loader Card */}
              <div style={{ border: '1px solid #e2e8f0', borderRadius: '12px', overflow: 'hidden', backgroundColor: '#ffffff' }}>
                <div style={{ padding: '12px 16px', backgroundColor: '#f1f5f9', fontWeight: '700', fontSize: '14px', color: '#1e293b' }}>
                  Loader Web (Fond Blanc)
                </div>
                <div style={{ padding: '16px', backgroundColor: '#ffffff', textAlign: 'center' }}>
                  <img src="/loader_white.gif" alt="Loader Web" style={{ width: '100%', maxHeight: '220px', objectFit: 'contain', borderRadius: '8px', border: '1px solid #f1f5f9' }} />
                </div>
                <div style={{ padding: '12px 16px', borderTop: '1px solid #e2e8f0', display: 'flex', gap: '8px', justifyContent: 'flex-end', backgroundColor: '#f8fafc' }}>
                  <button
                    onClick={() => setPreviewModalGif('/loader_white.gif')}
                    style={{ padding: '8px 12px', borderRadius: '6px', border: '1px solid #cbd5e1', background: '#fff', color: '#334155', cursor: 'pointer', fontSize: '12px', fontWeight: '600', display: 'flex', alignItems: 'center', gap: '4px' }}
                  >
                    <Eye style={{ width: '14px', height: '14px' }} /> Voir GIF
                  </button>
                  <button
                    onClick={() => handleDownload('/loader_white.gif', 'loader_luka_mosala_web.gif')}
                    style={{ padding: '8px 12px', borderRadius: '6px', border: 'none', background: '#185FA5', color: '#fff', cursor: 'pointer', fontSize: '12px', fontWeight: '600', display: 'flex', alignItems: 'center', gap: '4px' }}
                  >
                    <Download style={{ width: '14px', height: '14px' }} /> Télécharger
                  </button>
                </div>
              </div>

              {/* Mobile Loader Card */}
              <div style={{ border: '1px solid #e2e8f0', borderRadius: '12px', overflow: 'hidden', backgroundColor: '#ffffff' }}>
                <div style={{ padding: '12px 16px', backgroundColor: '#0f172a', fontWeight: '700', fontSize: '14px', color: '#ffffff' }}>
                  Loader Mobile (Fond Noir)
                </div>
                <div style={{ padding: '16px', backgroundColor: '#0B0F19', textAlign: 'center' }}>
                  <img src="/loader_black.gif" alt="Loader Mobile" style={{ width: '100%', maxHeight: '220px', objectFit: 'contain', borderRadius: '8px' }} />
                </div>
                <div style={{ padding: '12px 16px', borderTop: '1px solid #e2e8f0', display: 'flex', gap: '8px', justifyContent: 'flex-end', backgroundColor: '#f8fafc' }}>
                  <button
                    onClick={() => setPreviewModalGif('/loader_black.gif')}
                    style={{ padding: '8px 12px', borderRadius: '6px', border: '1px solid #cbd5e1', background: '#fff', color: '#334155', cursor: 'pointer', fontSize: '12px', fontWeight: '600', display: 'flex', alignItems: 'center', gap: '4px' }}
                  >
                    <Eye style={{ width: '14px', height: '14px' }} /> Voir GIF
                  </button>
                  <button
                    onClick={() => handleDownload('/loader_black.gif', 'loader_luka_mosala_mobile.gif')}
                    style={{ padding: '8px 12px', borderRadius: '6px', border: 'none', background: '#0F172A', color: '#fff', cursor: 'pointer', fontSize: '12px', fontWeight: '600', display: 'flex', alignItems: 'center', gap: '4px' }}
                  >
                    <Download style={{ width: '14px', height: '14px' }} /> Télécharger
                  </button>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'code' && (
            <div style={{ position: 'relative' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                <span style={{ fontSize: '12px', color: '#64748b', fontWeight: '600' }}>Python Animation Script (Pillow + ImageIO + NumPy)</span>
                <button
                  onClick={handleCopyCode}
                  style={{ padding: '6px 12px', borderRadius: '6px', border: '1px solid #cbd5e1', background: '#fff', cursor: 'pointer', fontSize: '12px', fontWeight: '600', display: 'flex', alignItems: 'center', gap: '4px' }}
                >
                  {copied ? <Check style={{ width: '14px', height: '14px', color: '#16a34a' }} /> : <Copy style={{ width: '14px', height: '14px' }} />}
                  <span>{copied ? 'Copié !' : 'Copier le Code'}</span>
                </button>
              </div>
              <pre style={{
                backgroundColor: '#0f172a', color: '#f8fafc', padding: '16px', borderRadius: '8px',
                fontSize: '12px', fontFamily: 'monospace', overflowX: 'auto', maxHeight: '350px'
              }}>
                {GENERATOR_SOURCE_CODE}
              </pre>
            </div>
          )}
        </div>
      </div>

      {/* Full Preview Modal */}
      {previewModalGif && (
        <div style={{
          position: 'fixed', inset: 0, zIndex: 1100, backgroundColor: 'rgba(0,0,0,0.85)',
          display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '20px'
        }} onClick={() => setPreviewModalGif(null)}>
          <div style={{ position: 'relative', maxWidth: '700px', width: '100%', textAlign: 'center' }} onClick={e => e.stopPropagation()}>
            <img src={previewModalGif} alt="Preview GIF" style={{ width: '100%', borderRadius: '12px', boxShadow: '0 20px 25px -5px rgba(0,0,0,0.5)' }} />
            <button
              onClick={() => setPreviewModalGif(null)}
              style={{ position: 'absolute', top: '-15px', right: '-15px', background: '#fff', border: 'none', borderRadius: '50%', padding: '8px', cursor: 'pointer', boxShadow: '0 4px 6px rgba(0,0,0,0.2)' }}
            >
              <X style={{ width: '20px', height: '20px', color: '#0f172a' }} />
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
