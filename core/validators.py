from django.conf import settings
from django.core.exceptions import ValidationError
import os


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1].lower()
    valid_extensions = getattr(settings, "BOOK_FILE_VALID_EXTENSIONS")
    if ext not in valid_extensions:
        raise ValidationError(
            f'Unsupported file extension. Only the following\
            extensions are allowed: {", ".join(valid_extensions)}'
        )


def validate_file_size(value):
    filesize = value.size
    megabyte_limit = getattr(settings, "BOOK_FILE_SIZE_LIMIT_MB")
    if filesize > megabyte_limit * 1024 * 1024:
        raise ValidationError(f"Max file size is {megabyte_limit}MB")
