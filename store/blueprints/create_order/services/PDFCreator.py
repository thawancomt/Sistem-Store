from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.pdfgen import canvas


class PDFCreator:
    def __init__(self) -> None:
        self.buffer = BytesIO()
        self.pdf = canvas.Canvas(self.buffer, pagesize=A4)
        self.width, self.height = A4
    
    def draw_header(self):
        self.pdf.drawString(190, 800, 'Order Num 2012/23122 FS')
    
    def draw_items(self, data : dict):
        data2 = [
            ['Amount', 'Quantity', 'Provider', 'Unit']
        ]

        data2.extend(
            [str(amount[0].name), amount[1], amount[0].provider.name, amount[0].type.name] for item, amount in data.items()
        )

        table = Table(data2, colWidths=[2 * inch, 1 * inch])

        # Adding style to the table
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])
        
        table.setStyle(style)
        
        # Calculate the position of the table
        table.wrapOn(self.pdf, self.width, self.height)
        table.drawOn(self.pdf, 50, 600)
    
    def create(self):
        self.pdf.save()
        self.buffer.seek(0)
        return self.buffer