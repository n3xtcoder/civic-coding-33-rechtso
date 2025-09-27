"""
OCR Service for processing documents using Mistral AI.
Handles file upload, OCR processing, and cleanup operations.
"""
import os
from pathlib import Path
from typing import Optional

from mistralai import Mistral
from config import Config


class OCRServiceError(Exception):
    """Custom exception for OCR service errors."""
    pass


class OCRService:
    """
    Service for processing documents using Mistral AI OCR capabilities.
    
    This service handles the complete workflow of uploading a document to Mistral,
    processing it with OCR, and managing the document lifecycle.
    """
    
    def __init__(self, file_path: Path) -> None:
        """
        Initialize the OCR service with the Mistral client.
        The service is initialized for a specific file.

        Args:
            file_path: The path to the file to be processed.
            
        Raises:
            OCRServiceError: If the Mistral API key is not configured.
        """
        if not Config.get_mistral_api_key():
            raise OCRServiceError(Config.get_error_no_api_key())
        
        self.client = Mistral(api_key=Config.get_mistral_api_key())
        self.file_path = file_path
        self.contents: Optional[str] = None
        self.file_id: Optional[str] = None
        self.signed_url: Optional[str] = None

    def process(self) -> str:
        """
        Process the document with Mistral OCR service and return its contents in a text format.
        
        Returns:
            str: The extracted text content from the document.
            
        Raises:
            OCRServiceError: If there's an error processing the document.
        """
        try:
            # Upload the file to the Mistral server
            self._upload_file()

            # Get the signed URL for the uploaded file
            self._get_signed_url()

            # Extract the contents of the document
            self._extract_contents()
            
            return self.contents or ""
        
        except Exception as e:
            raise OCRServiceError(f"Error processing the document: {str(e)}")

    def _upload_file(self) -> None:
        """
        Upload the file to the Mistral server.
        
        Raises:
            OCRServiceError: If there's an error uploading the file.
        """
        try:
            uploaded_file = self.client.files.upload(
                file={
                    "file_name": self.file_path.name,
                    "content": self.file_path.read_bytes(),
                },
                purpose="ocr"
            )
            self.file_id = uploaded_file.id
        except Exception as e:
            raise OCRServiceError(f"Error uploading file: {str(e)}")

    def _get_signed_url(self) -> None:
        """
        Get the signed URL for the uploaded file.
        
        Raises:
            OCRServiceError: If there's an error getting the signed URL.
        """
        if not self.file_id:
            raise OCRServiceError("File must be uploaded before getting signed URL")
        
        try:
            signed_url = self.client.files.get_signed_url(file_id=self.file_id)
            self.signed_url = signed_url.url
        except Exception as e:
            raise OCRServiceError(f"Error getting signed URL: {str(e)}")
    
    def _extract_contents(self) -> None:
        """
        Extract the contents of the document.
        
        Raises:
            OCRServiceError: If there's an error extracting contents.
        """
        if not self.signed_url:
            raise OCRServiceError("Signed URL must be obtained before extracting contents")
        
        try:
            ocr_response = self.client.ocr.process(
                model=Config.get_mistral_ocr_model(),
                document={"type": "document_url", "document_url": self.signed_url},
                include_image_base64=False
            )
            
            contents = ""
            for page in ocr_response.pages:
                contents += page.markdown
            self.contents = contents
        except Exception as e:
            raise OCRServiceError(f"Error extracting contents: {str(e)}")
    
    def delete_from_mistral(self) -> None:
        """
        Delete the file from the Mistral server.
        
        Raises:
            OCRServiceError: If there's an error deleting the file or no file ID is available.
        """
        if not self.file_id:
            raise OCRServiceError("No file ID available for deletion")
        
        try:
            print(f"🔍 Attempting to delete file with ID: {self.file_id}")
            response = self.client.files.delete(file_id=self.file_id)
            print(f"✅ Delete response: {response}")
            
            # Clear the file_id after successful deletion
            self.file_id = None
            self.signed_url = None
            
        except Exception as e:
            print(f"❌ Delete error: {str(e)}")
            raise OCRServiceError(f"Error deleting the file: {str(e)}")
    