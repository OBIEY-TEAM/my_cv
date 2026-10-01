# Luka Mosala - Plateforme IA de Génération de Candidatures (SaaS)

## Nature du Projet
**Luka Mosala** est une solution SaaS (Software as a Service) multiplateforme (Web et Mobile) conçue pour automatiser et optimiser la création de dossiers de candidature professionnels sur mesure (Curriculum Vitae sur 1 page, Lettre de Motivation sur 1 page, et texte d'accompagnement par email).

La plateforme repose sur une architecture moderne intégrant l'intelligence artificielle pour l'analyse d'offres d'emploi et la rédaction ciblée, la gestion de profil utilisateur structuré, ainsi que l'intégration de paiements Mobile Money (Airtel Money & MTN Mobile Money).

## Architecture & Technologies
- **Backend API REST** : Python / Django, Django REST Framework, Groq Cloud API (Modèles LLM Llama3/Mixtral), ReportLab (Génération PDF), PostgreSQL / SQLite.
- **Frontend Web** : TypeScript, React, Vite, Tailwind CSS / UI Responsive.
- **Application Mobile** : Dart, Flutter (Android & iOS).
- **Services Fintech & Stockage** : Intégration Airtel Money (préfixe `05`), MTN Mobile Money (préfixe `06`), Google Drive / Cloudinary pour les pièces jointes (diplômes, certifications).

## Fonctionnalités Principales
1. **Génération Intelligente de Dossiers** : Traitement d'offres d'emploi (texte ou lien URL) et génération instantanée de CV 1P, Lettre de Motivation 1P et Email de candidature.
2. **Profil Utilisateur Structuré** : Gestion centralisée des informations personnelles, expériences, certifications, diplômes et projets, synchronisés sur Web et Mobile.
3. **Système de Crédits & Recharge Mobile Money** : Achat de recharges de crédits via Airtel Money (05) et Mobile Money MTN (06) avec tarification dynamique :
   - 1 Crédit : 200 FCFA
   - 5 Crédits : 500 FCFA
   - 25 Crédits : 1000 FCFA
