import cloudinary
import cloudinary.uploader
import logging

logger = logging.getLogger(__name__)

class CloudinaryService:
    @staticmethod
    def upload_image(file_or_bytes, folder="profiles", public_id=None):
        """
        Uploads an image (file object, path, or BytesIO) to Cloudinary.
        Returns the secure URL of the uploaded image.
        """
        try:
            options = {
                "folder": folder,
                "resource_type": "image",
                "overwrite": True
            }
            if public_id:
                options["public_id"] = public_id

            response = cloudinary.uploader.upload(file_or_bytes, **options)
            secure_url = response.get("secure_url") or response.get("url")
            return secure_url
        except Exception as e:
            logger.error(f"Error uploading image to Cloudinary: {e}")
            print(f"Error uploading image to Cloudinary: {e}")
            return None

    @staticmethod
    def upload_pdf(file_or_bytes, folder="documents", public_id=None):
        """
        Uploads a PDF file to Cloudinary.
        Returns the secure URL of the uploaded PDF.
        """
        try:
            options = {
                "folder": folder,
                "resource_type": "raw",
                "overwrite": True
            }
            if public_id:
                options["public_id"] = public_id

            response = cloudinary.uploader.upload(file_or_bytes, **options)
            secure_url = response.get("secure_url") or response.get("url")
            return secure_url
        except Exception as e:
            logger.error(f"Error uploading PDF to Cloudinary: {e}")
            print(f"Error uploading PDF to Cloudinary: {e}")
            return None
