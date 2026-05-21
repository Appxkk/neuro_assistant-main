from datetime import datetime
from io import BytesIO

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


router = APIRouter(prefix="/api/pdf", tags=["pdf"])


class PdfRequest(BaseModel):
    recognized_text: str | None = None
    intent: str | None = None
    source: str | None = None
    result_text: str | None = None
    parameters: dict | None = None
    data: list[dict] | None = None


def register_font() -> str:
    possible_paths = [
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/calibri.ttf",
        "C:/Windows/Fonts/tahoma.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]

    for path in possible_paths:
        try:
            pdfmetrics.registerFont(TTFont("AppFont", path))
            return "AppFont"
        except Exception:
            continue

    return "Helvetica"


def safe_value(value):
    if value is None or value == "":
        return "—"

    if isinstance(value, float):
        return f"{value:,.2f}".replace(",", " ")

    if isinstance(value, int):
        return str(value)

    if isinstance(value, (dict, list)):
        return str(value)

    return str(value)


def make_paragraph(value, style):
    return Paragraph(safe_value(value), style)


@router.post("/download")
def download_pdf(payload: PdfRequest):
    font_name = register_font()

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        rightMargin=14 * mm,
        leftMargin=14 * mm,
        topMargin=14 * mm,
        bottomMargin=14 * mm,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Title"],
        fontName=font_name,
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=10,
    )

    subtitle_style = ParagraphStyle(
        "SubtitleStyle",
        parent=styles["Normal"],
        fontName=font_name,
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#64748b"),
        spaceAfter=8,
    )

    normal_style = ParagraphStyle(
        "NormalStyle",
        parent=styles["Normal"],
        fontName=font_name,
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#1e293b"),
    )

    small_style = ParagraphStyle(
        "SmallStyle",
        parent=styles["Normal"],
        fontName=font_name,
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#1e293b"),
    )

    section_style = ParagraphStyle(
        "SectionStyle",
        parent=styles["Heading2"],
        fontName=font_name,
        fontSize=13,
        leading=16,
        textColor=colors.HexColor("#2563eb"),
        spaceBefore=10,
        spaceAfter=6,
    )

    elements = []

    elements.append(Paragraph("Отчёт нейропомощника", title_style))
    elements.append(
        Paragraph(
            f"Дата формирования: {datetime.now().strftime('%d.%m.%Y %H:%M')}",
            subtitle_style,
        )
    )

    elements.append(Spacer(1, 6))

    elements.append(Paragraph("Распознанная команда", section_style))
    elements.append(make_paragraph(payload.recognized_text, normal_style))

    elements.append(Paragraph("Результат выполнения", section_style))
    elements.append(make_paragraph(payload.result_text, normal_style))

    elements.append(Paragraph("Информация о команде", section_style))

    meta_data = [
        [
            Paragraph("Параметр", normal_style),
            Paragraph("Значение", normal_style),
        ],
        [
            Paragraph("Интент", normal_style),
            Paragraph(safe_value(payload.intent), normal_style),
        ],
        [
            Paragraph("Источник обработки", normal_style),
            Paragraph(safe_value(payload.source), normal_style),
        ],
    ]

    if payload.parameters:
        for key, value in payload.parameters.items():
            if value is not None and value != "":
                meta_data.append(
                    [
                        Paragraph(str(key), normal_style),
                        Paragraph(safe_value(value), normal_style),
                    ]
                )

    meta_table = Table(meta_data, colWidths=[55 * mm, 145 * mm])
    meta_table.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (-1, -1), font_name),
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#dbeafe")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#0f172a")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    elements.append(meta_table)

    elements.append(Paragraph("Данные", section_style))

    if payload.data:
        columns = list(payload.data[0].keys())

        table_data = [
            [Paragraph(str(column), small_style) for column in columns]
        ]

        for item in payload.data:
            table_data.append(
                [
                    Paragraph(safe_value(item.get(column)), small_style)
                    for column in columns
                ]
            )

        page_width = landscape(A4)[0] - 28 * mm
        column_width = page_width / max(len(columns), 1)

        data_table = Table(
            table_data,
            colWidths=[column_width for _ in columns],
            repeatRows=1,
        )

        data_table.setStyle(
            TableStyle(
                [
                    ("FONTNAME", (0, 0), (-1, -1), font_name),
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2563eb")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#cbd5e1")),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 4),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                    ("TOPPADDING", (0, 0), (-1, -1), 4),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                    (
                        "ROWBACKGROUNDS",
                        (0, 1),
                        (-1, -1),
                        [colors.white, colors.HexColor("#f8fafc")],
                    ),
                ]
            )
        )

        elements.append(data_table)
    else:
        elements.append(Paragraph("Нет данных для отображения.", normal_style))

    document.build(elements)

    buffer.seek(0)

    filename = f"neuro_assistant_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"'
        },
    )