import os
from PIL import Image

def process_profile_photo(user_id: str, root_dir: str = ".") -> str:
    """
    Récupère la photo présent dans /commandes/photo/<ID_UTILISATEUR>.png
    (ou fallback sur image/profile_cropped.png / image/OBIEY-CHRIST-DANY.jfif si absent),
    effectue un recadrage centré (visage et haut du buste, format carré/portrait),
    et l'enregistre sous /commandes/photo/<ID_UTILISATEUR>_cropped.png.
    """
    photo_dir = os.path.join(root_dir, "commandes", "photo")
    os.makedirs(photo_dir, exist_ok=True)

    input_photo_path = os.path.join(photo_dir, f"{user_id}.png")
    output_photo_path = os.path.join(photo_dir, f"{user_id}_cropped.png")

    # Fallback paths
    fallback_paths = [
        os.path.join(root_dir, "image", "profile_cropped.png"),
        os.path.join(root_dir, "image", "OBIEY-CHRIST-DANY.jfif"),
        os.path.join(root_dir, "image", "profile.jpg")
    ]

    source_path = None
    if os.path.exists(input_photo_path):
        source_path = input_photo_path
    else:
        for fb in fallback_paths:
            if os.path.exists(fb):
                source_path = fb
                break

    if not source_path:
        print(f"[ImageProcessor] Aucune photo trouvée pour {user_id}. Création d'une image factice.")
        img = Image.new("RGB", (300, 300), color=(200, 200, 200))
        img.save(output_photo_path)
        return output_photo_path

    try:
        with Image.open(source_path) as img:
            img = img.convert("RGB")
            width, height = img.size

            # Recadrage centré haut (visage/buste)
            min_dim = min(width, height)
            left = (width - min_dim) / 2
            top = max(0, (height - min_dim) / 4) # Légèrement relevé pour le visage
            right = (width + min_dim) / 2
            bottom = top + min_dim

            if bottom > height:
                bottom = height
                top = height - min_dim

            cropped_img = img.crop((left, top, right, bottom))
            cropped_img = cropped_img.resize((400, 400), Image.Resampling.LANCZOS)
            cropped_img.save(output_photo_path, "PNG")
            print(f"[ImageProcessor] Photo traitée avec succès : {output_photo_path}")
            return output_photo_path
    except Exception as e:
        print(f"[ImageProcessor] Erreur lors du traitement de l'image ({e}). Copie directe.")
        if os.path.exists(source_path):
            with Image.open(source_path) as img:
                img.convert("RGB").save(output_photo_path)
        return output_photo_path
