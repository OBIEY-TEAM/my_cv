import os
from PIL import Image

class ImageProcessor:
    @staticmethod
    def crop_profile_picture(input_path, output_path=None):
        """
        Loads an input profile picture from input_path.
        Crops it to a 1:1 square centered on the face/upper bust area with extra space above head.
        Saves cropped photo to output_path or default _cropped.png path.
        Returns the output file path.
        """
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Image non trouvée: {input_path}")

        if output_path is None:
            base, ext = os.path.splitext(input_path)
            output_path = f"{base}_cropped.png"

        with Image.open(input_path) as img:
            img = img.convert("RGBA") if img.mode in ("RGBA", "P") else img.convert("RGB")
            width, height = img.size

            # Target 1:1 square aspect ratio
            square_side = min(width, height)

            # Center horizontally
            left = (width - square_side) // 2
            right = left + square_side

            # Vertical offset: center slightly higher to preserve head room and bust
            if height > width:
                top = max(0, int((height - square_side) * 0.25))
            else:
                top = 0
            bottom = top + square_side

            cropped_img = img.crop((left, top, right, bottom))
            cropped_img.save(output_path, "PNG")

        return output_path
