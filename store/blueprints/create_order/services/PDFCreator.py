from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.pdfgen import canvas
from ..models.OrdersModel import OrdersModel
from store.extensions import db

from datetime import datetime

class PDFCreator:
    def __init__(self, order = None) -> None:
        self.buffer = BytesIO()
        self.pdf = canvas.Canvas(self.buffer, pagesize=A4)
        self.width, self.height = A4
        self.y_position = self.height - 40  
        self.page_height = self.height
        self.page_margin = 40  
        self.page_index = 0
        self.order : OrdersModel = order
        self.create_order_name()
    
    def create_order_name(self):
        self.order_name = f'Order - {self.order.store.name} Nº {datetime.strftime(self.order.create_at, '%Y-%m')}/{self.order.id}'
        return self.order_name
    
    def draw_header(self):
        self.pdf.drawString(190, self.y_position, self.order_name)
        self.y_position -= 40  

    def draw_items(self, data: list):
        self.providers = [provider[2] for provider in data]
        self.providers = set(self.providers)

        for index, provider in enumerate(self.providers):
            data2 = [
                ['Article', 'Quantity', 'Provider', 'Unit', 'Estimated Price']
            ]
            data2.extend(
                [item[0], item[1], item[2], item[3], item[4]] for item in data if item[2] == provider
            )

            # Cria a tabela
            table = Table(data2, colWidths=[2 * inch, 1 * inch, 1 * inch, 1 * inch, 1 * inch])

            # Adiciona estilo à tabela
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

            # Calcula a altura da tabela e verifica se há espaço suficiente
            table_height = table.wrapOn(self.pdf, self.width, self.page_height)[1]
            if self.y_position - table_height < self.page_margin:
                self.pdf.showPage()
                self.y_position = self.page_height - self.page_margin  # Redefine a posição vertical para o início da nova página
                self.draw_header()  # Redesenha o cabeçalho na nova página

            # Desenha a tabela na página
            table.drawOn(self.pdf, 50, self.y_position - table_height)
            self.y_position -= (table_height + 20)  # Ajusta a posição vertical para o próximo item

    def create(self):
        self.buffer.seek(0)
        self.pdf.save()
        return self.buffer
