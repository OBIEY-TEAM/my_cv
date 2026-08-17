#!/bin/bash
# Script d'automatisation des mises a jour Git pour le serveur professionnel
echo "[Git Auto-Pull] Verification des mises a jour sur le depot Git..."
cd "$(dirname "$0")" || true
git fetch origin
echo "[Git Auto-Pull] Synchronisation du code source..."
git checkout main || git checkout master
