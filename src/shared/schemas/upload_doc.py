from pydantic import BaseModel


class UploadedDocument(BaseModel):
    filename: str
    mime_type: str
    content: bytes