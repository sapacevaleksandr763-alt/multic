"""Review PDF generator - creates PDF documents for video review"""

import logging
from pathlib import Path
from typing import List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class ReviewGenerator:
    """Generates PDF documents for video review"""

    def __init__(self, output_dir: str = None):
        self.output_dir = Path(output_dir) if output_dir else Path.cwd()
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_review_document(self, videos: list,
                                output_filename: str = None) -> Optional[str]:
        """
        Generate PDF review document for found videos

        Args:
            videos: List of PendingReview objects
            output_filename: Name of output PDF file

        Returns:
            Path to generated PDF file
        """
        try:
            from reportlab.lib.pagesizes import letter, A4
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
            from reportlab.lib import colors
            from datetime import datetime

            if not output_filename:
                output_filename = f"videos_review_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

            output_path = self.output_dir / output_filename

            # Create PDF
            doc = SimpleDocTemplate(str(output_path), pagesize=A4)
            story = []
            styles = getSampleStyleSheet()

            # Title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#1f4788'),
                spaceAfter=30,
                alignment=1  # Center
            )

            title = Paragraph("📋 ПРОВЕРКА ВИДЕО", title_style)
            story.append(title)
            story.append(Spacer(1, 0.2*inch))

            # Summary
            summary_text = f"Дата создания: {datetime.now().strftime('%d.%m.%Y %H:%M')}<br/>Всего видео: {len(videos)}"
            story.append(Paragraph(summary_text, styles['Normal']))
            story.append(Spacer(1, 0.3*inch))

            # Videos table
            table_data = [['#', 'Название', 'Платформа', 'Длительность', 'Размер (МБ)', 'URL']]

            for i, video in enumerate(videos, 1):
                duration_str = self._format_duration(video.duration_seconds)
                file_size_str = f"{video.file_size_mb:.1f}"

                # Truncate long title
                title_display = video.title[:50] + "..." if len(video.title) > 50 else video.title

                table_data.append([
                    str(i),
                    title_display,
                    video.platform,
                    duration_str,
                    file_size_str,
                    video.original_url[:40] + "..." if len(video.original_url) > 40 else video.original_url
                ])

            # Create table
            table = Table(table_data, colWidths=[0.5*inch, 2*inch, 1*inch, 1*inch, 1*inch, 2*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')]),
            ]))

            story.append(table)
            story.append(Spacer(1, 0.3*inch))

            # Instructions
            instructions = Paragraph(
                "<b>ИНСТРУКЦИИ ДЛЯ ПРОВЕРКИ:</b><br/>"
                "1. Проверьте название и описание видео<br/>"
                "2. Убедитесь, что длительность и размер файла в порядке<br/>"
                "3. Используйте команды для одобрения или редактирования<br/>"
                "<br/><b>КОМАНДЫ:</b><br/>"
                "/approve [номер] - Одобрить видео<br/>"
                "/reject [номер] - Отклонить видео<br/>"
                "/edit [номер] 'Описание изменений' - Редактировать видео",
                styles['Normal']
            )
            story.append(instructions)

            # Build PDF
            doc.build(story)

            logger.info(f"Review PDF generated: {output_path}")
            print(f"✅ PDF готов для просмотра: {output_path}")

            return str(output_path)

        except ImportError:
            logger.error("reportlab not installed. Install with: pip install reportlab")
            return None
        except Exception as e:
            logger.error(f"Error generating PDF: {e}")
            return None

    @staticmethod
    def _format_duration(seconds: int) -> str:
        """Format seconds to HH:MM:SS"""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60

        if hours > 0:
            return f"{hours}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes}:{secs:02d}"

    def generate_detailed_review(self, video, output_filename: str = None) -> Optional[str]:
        """
        Generate detailed PDF review for single video

        Args:
            video: PendingReview object
            output_filename: Name of output PDF file

        Returns:
            Path to generated PDF file
        """
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
            from reportlab.lib import colors

            if not output_filename:
                output_filename = f"video_review_{video.video_id}.pdf"

            output_path = self.output_dir / output_filename

            # Create PDF
            doc = SimpleDocTemplate(str(output_path), pagesize=A4)
            story = []
            styles = getSampleStyleSheet()

            # Title
            title = Paragraph(f"📹 {video.title}", styles['Heading1'])
            story.append(title)
            story.append(Spacer(1, 0.2*inch))

            # Details table
            details_data = [
                ['Поле', 'Значение'],
                ['ID', video.video_id],
                ['Платформа', video.platform],
                ['Длительность', self._format_duration(video.duration_seconds)],
                ['Размер файла', f"{video.file_size_mb:.1f} МБ"],
                ['URL', video.original_url],
                ['Путь файла', video.file_path],
                ['Создано', video.created_at.strftime('%d.%m.%Y %H:%M:%S')],
            ]

            details_table = Table(details_data, colWidths=[2*inch, 4*inch])
            details_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')]),
            ]))

            story.append(details_table)
            story.append(Spacer(1, 0.3*inch))

            # Description
            story.append(Paragraph("<b>ОПИСАНИЕ:</b>", styles['Heading2']))
            story.append(Paragraph(video.description, styles['Normal']))
            story.append(Spacer(1, 0.2*inch))

            # Issues if any
            if video.issues:
                story.append(Paragraph("<b>ПРОБЛЕМЫ:</b>", styles['Heading2']))
                for issue in video.issues:
                    story.append(Paragraph(f"• {issue}", styles['Normal']))

            # Build PDF
            doc.build(story)

            logger.info(f"Detailed review PDF generated: {output_path}")
            return str(output_path)

        except ImportError:
            logger.error("reportlab not installed")
            return None
        except Exception as e:
            logger.error(f"Error generating detailed PDF: {e}")
            return None
