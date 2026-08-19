# PROMPT SPÉCIFICATION ARCHITECTURALE & DÉVELOPPEMENT D'APPLICATION MOBILE FLUTTER & WEB
# NOM DU PROJET : "AI JobApply SaaS" - Application Mobile Flutter & Plateforme Web
# SYSTEME AGENTIQUE INTEGRÉ : AGENT_IA_CV

---

## 1. SPECIFICATIONS UI/UX DÉTAILLÉES POUR APPLICATION MOBILE FLUTTER
1. **Interface Candidatures & Ergonomie :**
   - Remplacement de toutes les formes sombres et boutons génériques par des **icônes explicites**.
   - Alignement optimisé des éléments et augmentation de l'espacement inter-cartes pour aérer la vue.

2. **Vue 'Générer' Mobile :**
   - Option permettant de téléverser au choix un document (PDF) ou une image de l'offre d'emploi (capture d'écran galerie/caméra), un lien URL ou un texte brut.

3. **Vue 'Profil' Mobile :**
   - Regroupement des options 'Modifier', 'Uploader' et 'Caméra' en un **seul bouton contextuel fonctionnel**.
   - Remplacement de l'icône générique de profil par l'**affichage réel de la photo de profil chargée**.
   - **Masquage dynamique des champs vides** sur la vue profil pour n'afficher que les données renseignées.

4. **Fenêtres Modales Mobile (Profil, Expériences, Certifications, Diplômes, Projets) :**
   - Ajout d'un **bouton en haut de la modale pour passer en affichage plein écran (Full-screen Dialog)**.
   - Utilisation d'un **sélecteur de date interactif (Calendrier / Datepicker)** pour la sélection des années.
   - **Correspondance exacte et stricte des champs** des modales de profil mobile avec ceux définis dans l'application web.
   - **Suppression du bouton 'Payer / Recharger Crédits'** dans les modales de prévisualisation (CV, LM, EMAIL).

---

## 2. FLUX AUTOMATISÉ ET HARMONISATION AGENT_IA_CV
1. **Profil utilisateur & Offre :** Exportés vers `/commandes/info/<ID>.txt` et `/commandes/photo/<ID>.png` lors de la validation du paiement.
2. **Traitement autonome par AGENT_IA_CV :** Recadrage photo centré visage/buste (`_cropped.png`), extraction d'offre, génération du CV 1-page (2 colonnes), de la Lettre de Motivation 1-page, de l'Offre PDF et de l'Email TXT.
3. **Livraison :** Stockage dans `/resultat/<ID>/<site>/<poste>/` pour téléchargement immédiat sur l'App Mobile Flutter.
