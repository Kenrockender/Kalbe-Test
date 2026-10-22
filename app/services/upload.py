from fastapi import Request, UploadFile
from starlette.datastructures import UploadFile as StarletteUploadFile

from app.errors import ValidationError


async def read_single_fasta_upload(request: Request, file: UploadFile) -> bytes:
    """Return the request's only upload after enforcing the multipart contract."""
    form = await request.form()
    uploaded_parts = [
        (field_name, value)
        for field_name, value in form.multi_items()
        if isinstance(value, StarletteUploadFile)
    ]

    if len(uploaded_parts) != 1 or uploaded_parts[0][0] != "file":
        raise ValidationError(
            "multiple_files",
            "Exactly one FASTA file must be uploaded in the 'file' field",
        )

    try:
        return await file.read()
    finally:
        await file.close()
