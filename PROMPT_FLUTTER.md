# PROMPT SPÉCIFICATION APPLICATIVE FLUTTER & FRONTEND

## 1. VISION D'ENSEMBLE
Développement et optimisation des applications Web (React) et Mobile (Flutter) pour la plateforme "AI JobApply SaaS" avec intégration de l'agent `AGENT_IA_CV` et des passerelles de paiement Mobile Money.

---

## 2. SPÉCIFICATIONS FONCTIONNELLES APPLICATION WEB (REACT / TYPESCRIPT)
1. **Design & Spacing Dashboard :**
   - Amélioration de la hiérarchie visuelle, typographie moderne et espacement aéré.
   - Section 'Formules d'Abonnement' avec affichage clair des logos/modes de paiement : Airtel Money, MTN Mobile Money et Carte Bancaire.

2. **Vue 'Générer un Dossier' :**
   - Formulaire dynamic acceptant URL, texte brut ou téléchargement direct de document PDF / Image d'offre.

3. **Vue 'Profil Utilisateur' :**
   - Bouton contextuel unique regroupant 'Modifier', 'Uploader' et 'Caméra'.
   - Conservation stricte du ratio et de l'orientation d'origine de la photo de profil.
   - Champs de profil organisés en blocs logiques avec sélecteur de date interactif.
   - Saisie explicite des dates de début et de fin pour les 'Expériences Professionnelles'.

4. **Modales de Prévisualisation (CV, LM, EMAIL) :**
   - Suppression du bouton de recharge de crédits au sein des modales de consultation de document.

---

## 3. SPÉCIFICATIONS FONCTIONNELLES APPLICATION MOBILE (FLUTTER / DART)
1. **Interface & Ergonomie Candidatures :**
   - Remplacement des formes sombres des boutons par des icônes explicites.
   - Optimisation de l'alignement et augmentation de l'espacement entre les cartes.

2. **Vue 'Générer' :**
   - Option d'upload de document PDF ou Image de l'offre d'emploi.

3. **Vue 'Profil' :**
   - Menu contextuel d'actions photo ('Caméra', 'Galerie', 'Supprimer').
   - Affichage de la photo de profil réelle et masquage des champs non renseignés.

4. **Modales & Formulaires :**
   - Bouton de basculement plein écran en haut des fenêtres modales.
   - Sélecteurs de date (calendrier) pour la sélection d'années.
   - Alignement strict des champs des modales de profil (Expériences, Certifications, Diplômes, Projets) avec l'application web.
