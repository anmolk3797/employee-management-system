from django.core.exceptions import ValidationError
import os

def validate_pdf_extension(value):
    ext = os.path.splitext(value.name)[1]
    if ext.lower() != '.pdf':
        raise ValidationError('Only PDF files are allowed.')