import tempfile
from datetime import datetime
from io import BytesIO

from anagrafiche.models import Facility
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from qmsproject.context_processors import nome_sito


class PDFReport:
    def __init__(self, title, margins=(50, 50), page_size=A4):
        """
        Classe base per la generazione di report PDF.

        :param title: Titolo del report.
        :param margins: Margini (sinistro, destro).
        :param page_size: Dimensioni della pagina.
        """
        self.title = title
        self.margins = margins
        self.page_size = page_size
        self.buffer = BytesIO()
        self.canvas = canvas.Canvas(self.buffer, pagesize=page_size)
        self.width, self.height = page_size

    def draw_header(self):
        facility = Facility.objects.first()
        company_name = facility.nome_sito if facility else "Nome Azienda"
        """Disegna l'header del report."""
        self.canvas.setFont("Helvetica-Bold", 12)        
        self.canvas.drawString(self.margins[0], self.height - 50, company_name)
        self.canvas.drawRightString(self.width - self.margins[1], self.height - 50, self.title)
        # Linea orizzontale sotto l'header
        self.canvas.setStrokeColorRGB(0, 0, 0)
        self.canvas.setLineWidth(1)
        self.canvas.line(self.margins[0], self.height - 60, self.width - self.margins[1], self.height - 60)

    def draw_footer(self, page_number, total_pages):
        """Disegna il footer del report."""
        # Linea orizzontale sopra il footer
        self.canvas.setStrokeColorRGB(0, 0, 0)
        self.canvas.setLineWidth(1)
        self.canvas.line(self.margins[0], 50, self.width - self.margins[1], 50)

        # Data e ora
        current_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.canvas.setFont("Helvetica", 6)
        self.canvas.drawString(self.margins[0], 30, f"Stampa: {current_datetime}")

        # Numerazione pagine
        self.canvas.drawRightString(self.width - self.margins[1], 30, f"Pagina {page_number} di {total_pages}")

    def calculate_total_pages(self):
        """Calcola il numero totale di pagine."""
        temp_buffer = BytesIO()
        temp_canvas = canvas.Canvas(temp_buffer, pagesize=self.page_size)
        self.draw_body(temp_canvas)
        temp_canvas.save()
        temp_buffer.seek(0)
        temp_canvas = canvas.Canvas(temp_buffer, pagesize=self.page_size)
        return temp_canvas.getPageNumber()

    def draw_body(self, canvas):
        """
        Metodo da sovrascrivere per disegnare il contenuto del report.
        Deve essere implementato nei report specifici.
        """
        raise NotImplementedError("Il metodo 'draw_body' deve essere implementato nel report specifico.")

    def generate_pdf(self):
        """Genera il PDF completo con header, footer e contenuto."""
        total_pages = self.calculate_total_pages()

        # Disegna ogni pagina
        for page_number in range(1, total_pages + 1):
            self.draw_header()
            self.draw_body(self.canvas)
            self.draw_footer(page_number, total_pages)
            self.canvas.showPage()

        # Salva il canvas nel buffer
        self.canvas.save()

        # Prepara il buffer per la lettura
        self.buffer.seek(0)
        return self.buffer


