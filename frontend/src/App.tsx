import React, { useState } from 'react';
import { Sparkles, Briefcase, FileText, Download } from 'lucide-react';

export default function App() {
  return (
    <div className="min-h-screen bg-slate-900 text-white p-8">
      <div className="max-w-4xl mx-auto space-y-6">
        <div className="flex items-center space-x-3">
          <Sparkles className="w-8 h-8 text-sky-400" />
          <h1 className="text-3xl font-bold">AI JobApply SaaS - Générateur Automatisé</h1>
        </div>
        <p className="text-slate-300">Plateforme de génération automatique de candidatures sur mesure (CV 1-Page & LM 1-Page).</p>
      </div>
    </div>
  );
}
