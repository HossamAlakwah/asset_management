"""OpenAPI helpers: per-resource tags and reusable response shapes."""

from drf_spectacular.openapi import AutoSchema
from drf_spectacular.utils import OpenApiExample, OpenApiResponse, OpenApiTypes

XLSX_MEDIA_TYPE = (
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)


class TaggedAutoSchema(AutoSchema):
    """Group operations in Swagger by the resource's UI title."""

    def get_tags(self):
        title = getattr(self.view, "ui_title", None)
        if title:
            return [title]
        return super().get_tags()


XLSX_FILE_RESPONSE = OpenApiResponse(
    response=OpenApiTypes.BINARY,
    description="An .xlsx workbook.",
)

EXCEL_UPLOAD_REQUEST = {
    "multipart/form-data": {
        "type": "object",
        "properties": {
            "file": {
                "type": "string",
                "format": "binary",
                "description": "An .xlsx workbook matching the download template.",
            }
        },
        "required": ["file"],
    }
}

EXCEL_IMPORT_RESPONSE = OpenApiResponse(
    response={
        "type": "object",
        "properties": {
            "created": {"type": "integer"},
            "failed": {"type": "integer"},
            "errors": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "row": {"type": "integer"},
                        "errors": {"type": "object", "additionalProperties": True},
                    },
                },
            },
        },
    },
    description="Per-row import outcome.",
    examples=[
        OpenApiExample(
            "Partial import",
            value={
                "created": 18,
                "failed": 2,
                "errors": [
                    {"row": 5, "errors": {"serial": ["This field must be unique."]}},
                    {"row": 9, "errors": {"branch": ["No branch with name 'HQ2'."]}},
                ],
            },
        )
    ],
)
