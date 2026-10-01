# Luka Mosala - Plateforme IA de Génération de Candidatures (SaaS)

## Nature du Projet
**Luka Mosala** est une solution SaaS (Software as a Service) multiplateforme (Web et Mobile) conçue pour automatiser et optimiser la création de dossiers de candidature professionnels sur mesure (Curriculum Vitae sur 1 page, Lettre de Motivation sur 1 page, et texte d'accompagnement par email).

La plateforme repose sur une architecture moderne intégrant l'intelligence artificielle pour l'analyse d'offres d'emploi et la rédaction ciblée, la gestion de profil utilisateur structuré, ainsi que l'intégration de paiements Mobile Money (Airtel Money & MTN Mobile Money).

## Architecture & Technologies
- **Backend API REST** : Python / Django, Django REST Framework, Groq Cloud API (Modèles LLM Llama3/Mixtral), ReportLab (Génération PDF), PostgreSQL / SQLite.
- **Frontend Web** : TypeScript, React, Vite, Tailwind CSS / UI Responsive. Architecture modulaire basée sur des composants et services réutilisables.
- **Application Mobile** : Dart, Flutter (Android & iOS). Architecture modulaire organisée en écrans (`screens/`), onglets (`tabs/`), et services API (`services/`).
- **Services Fintech & Stockage** : Intégration Airtel Money (préfixe `05`), MTN Mobile Money (préfixe `06`), Google Drive / Cloudinary pour les pièces jointes (diplômes, certifications).

## Sécurité & Déploiement (Variables d'Environnement)
> ⚠️ **Remarque Importante concernant les Clés API & Sécurité :**
> Aucune clé d'API (Groq API, Cloudinary, Secret Key Django, Identifiants de base de données, etc.) ne doit être codée en dur dans le code source ou dans les fichiers de configuration versionnés.
>
> Lors du déploiement sur **Render**, **Docker** ou tout autre hébergeur cloud :
> 1. Définissez les clés API via le panneau de configuration des variables d'environnement de l'hébergeur.
> 2. Variables requises :
>    - `GROQ_API_KEY` : Clé d'API Groq Cloud pour la génération LLM.
>    - `GROQ_MODEL` : Modèle sélectionné (ex: `openai/gpt-oss-20b` ou `llama3-70b-8192`).
>    - `SECRET_KEY` : Clé secrète Django.
>    - `DATABASE_URL` / `SUPABASE_DATABASE_URL` : URL de connexion PostgreSQL.
>    - `CLOUDINARY_URL`, `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET` : Identifiants Cloudinary pour l'hébergement des médias.

## Fonctionnalités Principales
1. **Génération Intelligente de Dossiers** : Traitement d'offres d'emploi (texte ou lien URL) et génération instantanée de CV 1P, Lettre de Motivation 1P et Email de candidature.
2. **Profil Utilisateur Structuré** : Gestion centralisée des informations personnelles, expériences, certifications, diplômes et projets, synchronisés sur Web et Mobile.
3. **Système de Crédits & Recharge Mobile Money** : Achat de recharges de crédits via Airtel Money (05) et Mobile Money MTN (06) avec tarification dynamique :
   - 1 Crédit : 200 FCFA
   - 5 Crédits : 500 FCFA
   - 25 Crédits : 1000 FCFA
