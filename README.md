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
1. **Génération Intelligente de Dossiers (Word & PDF)** : Traitement d'offres d'emploi (texte ou lien URL) et génération instantanée de CV 1P, Lettre de Motivation 1P et Email de candidature. Les fichiers Word (.docx) sont également générés par le backend pour permettre l'édition directe depuis Microsoft Word via l'application Web React et Mobile Flutter.
2. **Gestion Cloudinary & Suppression Automatique** : Après modification des textes de candidature (CV, Lettre de motivation ou Email), les nouveaux fichiers PDF/DOCX sont sauvegardés et mis à jour sur Cloudinary en supprimant automatiquement l'ancien fichier enregistré via l'API Cloudinary.
3. **Gestion des Documents en cours de rédaction** : Dans le cas où les fichiers (CV, LM, EMAIL) ne sont pas encore générés ni disponibles, un message d'alerte explicite "Document en cours de rédaction ..." est affiché lors du clic sur le document.
4. **Profil Utilisateur & Actions Photo Mobile** : Sur l'application mobile Flutter, les boutons d'action de photo de profil permettent :
   - **Uploader** : Choisir une image depuis la galerie.
   - **Caméra** : Prendre une photo directement avec l'appareil.
   - **Voir** : Consulter la photo de profil actuelle dans une modale.
   *(Le bouton "Modifier" à été retiré sur la version mobile au profit d'actions claires).*
5. **Règles de Crédits & Tarification** :
   - **Création de candidature** : 1 candidature = 1 crédit.
   - **Modifications** : 1 modification de CV, de LM ou d'Email coûte 1 crédit pour chaque élément modifié.
   - **Tarifs des packs de crédits (Web & Mobile)** :
     - 1 Crédit : 200 FCFA
     - 5 Crédits : 500 FCFA
     - 25 Crédits : 1000 FCFA
