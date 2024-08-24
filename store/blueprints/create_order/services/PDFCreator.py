from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.pdfgen import canvas

from ..models.OrdersModel import OrdersModel


from store.extensions import db


class PDFCreator:
    def __init__(self) -> None:
        self.buffer = BytesIO()
        self.pdf = canvas.Canvas(self.buffer, pagesize=A4)
        self.width, self.height = A4
    
    def draw_header(self):
        self.pdf.drawString(190, 800, 'Order Num 2012/23122 FS')
    
    def draw_items(self, data : list):

        self.providers = [provider[2] for provider in data]
        self.providers = set(self.providers)
        
        

        for index, provider in enumerate(self.providers):

            data2 = [
                ['Article', 'Quantity', 'Provider', 'Unit', 'Estimated Price']
            ]

            data2.extend(
                [item[0], item[1], item[2], item[3], item[4]] for item in data if item[2] == provider
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
                ('GRID', (0, 1), (-1, -1), 1, colors.purple),
                ('GRID', (0, 0), (-1, 0), 1, colors.black),
            ])
            
            table.setStyle(style)
            
            # Calculate the position of the table
            table.wrapOn(self.pdf, self.width, self.height)
            table.drawOn(self.pdf, 50, 700 - index * 100)
    
    def create(self):
        self.pdf.save()
        self.buffer.seek(0)

        return self.buffer
    
    def save_db(self, data):
        Order = OrdersModel(
            store_id = data.get('store_id'),
            file = data.get('file'),
            create_at = data.get('date')
        )

        db.session.add(Order)
        db.session.commit()
