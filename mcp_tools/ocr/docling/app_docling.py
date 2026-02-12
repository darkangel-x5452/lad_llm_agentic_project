import json
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
from IPython import display
from pydantic import BaseModel, Field
from rich import print


class DoclingApp:
    def __init__(self):
        pass

    def extract_any_text(self, document_path):
        """
        Docstring for extract_text

        :param self: Description
        :param document_path: Description
        """

        # PDF Example
        # source = "https://arxiv.org/pdf/2408.09869"  # document per local path or URL
        converter = DocumentConverter()
        result = converter.convert(document_path)
        print(
            result.document.export_to_markdown()
        )  # output: "## Docling Technical Report[...]"
        print(
            result.document.export_to_dict()
        )  # output: "## Docling Technical Report[...]"

        with open("./data/ocr/docling_image_text.json", "w") as f:
            json.dump(result.document.export_to_dict(), f, indent=2)


    def extract_image_text(self, document_path):
        """
        Docstring for extract_text

        :param self: Description
        :param document_path: Description
        """

        file_path = document_path
        display.HTML(f"<img src='{file_path}' height='1000'>")

        from docling.datamodel.base_models import InputFormat
        from docling.document_extractor import DocumentExtractor

        extractor = DocumentExtractor(
            allowed_formats=[InputFormat.IMAGE, InputFormat.PDF]
        )

        result = extractor.extract(
            source=file_path,
            # template='{"bill_no": "string", "total": "float"}',
            template='{}',
        )
        print(result.pages)


if __name__ == "__main__":
    app = DoclingApp()
    import os
    root_dir = os.get("ROOT_DIR")
    app.extract_any_text(f"{root_dir}/espn_match.jpg")
