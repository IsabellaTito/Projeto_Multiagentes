import base64

from io import BytesIO

from pdf2image import convert_from_bytes

from shared.schemas.upload_doc import UploadedDocument


class DocumentPreprocessor:

    @staticmethod
    def image_to_base64(image_bytes: bytes) -> str:
        return (base64.b64encode(image_bytes).decode("utf-8"))

    @staticmethod
    def pdf_to_images_base64(pdf_bytes: bytes) -> list[str]:
        pages = convert_from_bytes(pdf_bytes)

        images = []

        for page in pages:

            buffer = BytesIO()

            page.save(buffer,format="JPEG")

            images.append(base64.b64encode(buffer.getvalue()).decode("utf-8"))

        return images

    def build_multimodal_content(self,documents: list[UploadedDocument],prompt: str):

        content = [{
                "type": "text",
                "text": prompt
        }]

        for document in documents:

            if document.mime_type == "application/pdf":

                images = self.pdf_to_images_base64(document.content)

                for image in images:

                    content.append({
                            "type": "image_url",
                            "image_url": {
                                "url":f"data:image/jpeg;base64,{image}"
                            }
                    })

            else:

                encoded = self.image_to_base64(document.content)

                content.append({
                        "type": "image_url",
                        "image_url": {
                            "url":f"data:{document.mime_type};base64,{encoded}"
                        }
                })

        return content