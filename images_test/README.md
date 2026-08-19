# Test Proof Deliverables and Visual Screenshots - Luka Mosala SaaS

This directory contains test proof deliverables, interface previews, and system architecture verification for **Luka Mosala SaaS** (Automated Application Generator).

## Key Features & Interfaces Verified

1. **Structured Candidate Profile:**
   - 10 Info fields: Nom, Prénom, Genre dropdown, Date de naissance, Numéro principal, Numéro secondaire, Adresse, Pays, Arrondissement, Quartier, Résumé.
   - Section CRUD forms for Experiences, Certifications, Diplomas, and Projects.
   - Google Drive PDF document uploads for certificates & diplomas embedded into generated CVs.
   - 4 Photo action buttons: **Modifier**, **Uploader**, **Caméra**, **Voir**.

2. **Candidature Package Actions & Statuses:**
   - Explicit buttons: **CV**, **LM**, **EMAIL**, **Payer**.
   - Details modal showing `payment_status` (`approuved`, `pending`, `failed`) and `processing_status` (`finalized`, `pending`, `inprocess`).

3. **Commandes & Resultat Sync:**
   - Automated creation of `/commandes/info/<USER_ID>.txt` and `/commandes/photo/<USER_ID>.png`.
   - Jules agent output directory `/resultat/<USER_ID>/<SITE>/<POSTE>/` containing custom deliverables (`CV.pdf`, `LM.pdf`, `OFFRE.pdf`, `EMAIL.txt`).

4. **Jules AI API & OpenAPI Specs:**
   - Admin REST endpoints at `/api/jules/sessions/`.
   - Live Swagger UI at `/api/docs/swagger/`, Redoc at `/api/docs/redoc/`, and schema at `/api/docs/schema/`.

5. **Server Script:**
   - Git synchronization script `auto_pull.sh` at project root.
