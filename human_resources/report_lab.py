import io
import math
import os
import tempfile
from datetime import date, datetime
from io import BytesIO

import matplotlib.pyplot as plt
from core.pdf_utils import PDFReport
from django.db.models import Count
from django.http import FileResponse, HttpResponse
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.ticker import FixedLocator
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape, letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas

from .charts import get_gender_perc
from .models import HumanResource


def generate_gender_report(request):

    PAGE_WIDTH, PAGE_HEIGHT = A4
    # Definisci i margini
    MARGIN_LEFT = 50
    MARGIN_RIGHT = 50
    # Creazione del buffer
    buffer = BytesIO()

    # Creazione del PDF con ReportLab
    p = canvas.Canvas(buffer)

    # Header
    text = "Azienda XYZ - Performance Aziendale"
    FONT_NAME = "Helvetica"
    FONT_SIZE = 16
    #p.setFont("Helvetica-Bold", 16)
    #p.drawString(200, 800, "Azienda XYZ - Performance Aziendale")
    # Calcola la larghezza del testo
    text_width = pdfmetrics.stringWidth(text, FONT_NAME, FONT_SIZE)

    # Calcola la posizione orizzontale centrata
    x_position = (PAGE_WIDTH - text_width) / 2

    # Disegna il testo centrato
    p.setFont(FONT_NAME, FONT_SIZE)
    p.drawString(x_position, 800, text)
    p.line(MARGIN_LEFT, 790, PAGE_WIDTH - MARGIN_RIGHT, 790)

    # Grafico (Matplotlib)
    fig = Figure(figsize=(4, 2.5))
    ax = fig.add_subplot(111)

    # Dati per il grafico
    hrs = HumanResource.objects.filter(datadimissioni__isnull=True)
    male_count = hrs.filter(gender='M').count()
    female_count = hrs.filter(gender='F').count()
    total_count = hrs.count()

    if total_count > 0:
        male_percentage = (male_count / total_count) * 100
        female_percentage = (female_count / total_count) * 100
    else:
        male_percentage = female_percentage = 0

    labels = ['Maschi', 'Femmine']
    sizes = [male_percentage, female_percentage]
    #colors = plt.get_cmap('Blues')(sizes.linspace(0.2, 0.7, len(sizes)))
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['blue', 'pink'])
    #ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
    ax.axis('equal')

    # Converti il grafico in immagine
    fig_canvas = FigureCanvas(fig)
    img_buffer = BytesIO()
    fig_canvas.print_png(img_buffer)
    img_buffer.seek(0)

    # Inserisci il grafico nel PDF
    p.drawImage(ImageReader(img_buffer), 40, 400, width=300, height=200)

    # Footer
    p.setFont("Helvetica", 10)
    p.line(MARGIN_LEFT, 50, PAGE_WIDTH - MARGIN_RIGHT, 50)

    current_datetime = datetime.now().strftime("%d/%m/%Y %H:%M")
    p.drawString(50, 35, f"Data e Ora di stampa: {current_datetime}")    
    p.drawRightString(550, 35, "Pagina 1 di 1")

    # Finalizza il PDF
    p.showPage()
    p.save()

    # Posizionare il buffer al punto iniziale
    buffer.seek(0)

    # Restituisci il PDF come risposta
    return HttpResponse(buffer, content_type='application/pdf')



# Funzione per generare il grafico "Operatori per Reparto"
def generate_operatori_per_reparto_chart():
    queryset = HumanResource.objects.values('fk_reparto__description').annotate(hr_count=Count('pk'))
    labels = [entry['fk_reparto__description'] for entry in queryset]
    data = [entry['hr_count'] for entry in queryset]

    fig, ax = plt.subplots()
    ax.bar(labels, data, color='skyblue')
    ax.set_title('Operatori per Reparto')
    ax.set_ylabel('Numero Operatori')
    ax.set_xticks(range(len(labels)))  # Imposta la posizione per ogni etichetta
    ax.set_xticklabels(labels, rotation=45, ha='right')

    buffer = BytesIO()
    plt.savefig(buffer, format='png', dpi=150)
    buffer.seek(0)
    plt.close(fig)
    return buffer

# Funzione per generare il grafico delle fasce d'età
def generate_age_groups_chart_old():
    hrs = HumanResource.objects.filter(datadimissioni__isnull=True).filter(data_nascita__isnull=False)
    labels = ['18-30', '31-40', '41-50', '51-60', '>60']
    data = [0, 0, 0, 0, 0]
    
    for hr in hrs:
        in_days = (datetime.now() - hr.data_nascita).days
        age = in_days // 365
        if 18 <= age <= 30:
            data[0] += 1
        elif 31 <= age <= 40:
            data[1] += 1
        elif 41 <= age <= 50:
            data[2] += 1
        elif 51 <= age <= 60:
            data[3] += 1
        elif age > 60:
            data[4] += 1

    fig, ax = plt.subplots()
    ax.pie(data, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.set_title('Distribuzione Fasce d\'Età')

    buffer = BytesIO()
    plt.savefig(buffer, format='png', dpi=150)
    buffer.seek(0)
    plt.close(fig)
    return buffer

# Funzione per generare il PDF
def generate_report_pdf(request):
    # Creare un oggetto BytesIO per scrivere il PDF in memoria
    pdf_buffer = BytesIO()
    
    # Creare un oggetto canvas per disegnare il PDF
    pdf_canvas = canvas.Canvas(pdf_buffer, pagesize=A4)
     # Funzione dell'header
    draw_header(pdf_canvas, "report_name")
    width, height = A4

    # Inserire Grafici
    row_y = height - 250  # Altezza iniziale
    col_x = 50  # Spazio a sinistra

    # Primo Grafico: Operatori per Reparto
    operatori_chart = generate_operatori_per_reparto_chart()

    # Crea un file temporaneo per memorizzare l'immagine del grafico
    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
        temp_file.write(operatori_chart.getvalue())
        temp_file_path = temp_file.name

    # Usa il percorso del file temporaneo con drawImage
    pdf_canvas.drawImage(temp_file_path, col_x, row_y, width=250, height=150)

    # Secondo Grafico: Fasce d'età
    age_groups_chart = generate_age_groups_chart()

    # Crea un file temporaneo per il grafico delle fasce d'età
    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
        temp_file.write(age_groups_chart.getvalue())
        temp_file_path = temp_file.name

    # Usa il percorso del file temporaneo con drawImage
    pdf_canvas.drawImage(temp_file_path, col_x + 300, row_y, width=250, height=150)

    # Nuova riga per altri grafici
    row_y -= 200
    # Funzione del footer
    draw_footer(pdf_canvas)
    # Altri grafici...
    # Esempio: aggiungi altre chiamate per nuovi grafici e posizione

    # Salva il PDF nel buffer
    pdf_canvas.save()

    # Imposta la posizione del buffer per la lettura dall'inizio
    pdf_buffer.seek(0)

    # Restituisce il PDF come risposta HTTP
    return FileResponse(pdf_buffer, as_attachment=True, filename='report.pdf', content_type='application/pdf')

def generate_age_groups_chart():
    hrs = HumanResource.objects.filter(datadimissioni__isnull=True).filter(data_nascita__isnull=False)
    labels = ['18-30', '31-40', '41-50', '51-60', '>60']
    data = [0, 0, 0, 0, 0]

    for hr in hrs:
        # Assicurati che `hr.data_nascita` sia trattato come un oggetto datetime
        if isinstance(hr.data_nascita, datetime):
            birth_date = hr.data_nascita
        else:
            # Se è un oggetto `datetime.date`, aggiungi un orario fittizio (00:00:00)
            birth_date = datetime.combine(hr.data_nascita, datetime.min.time())

        # Ora entrambi sono datetime, quindi puoi fare la sottrazione
        in_days = (datetime.now() - birth_date).days
        age = in_days // 365
        
        if 18 <= age <= 30:
            data[0] += 1
        elif 31 <= age <= 40:
            data[1] += 1
        elif 41 <= age <= 50:
            data[2] += 1
        elif 51 <= age <= 60:
            data[3] += 1
        elif age > 60:
            data[4] += 1

    fig, ax = plt.subplots()
    ax.pie(data, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.set_title('Distribuzione Fasce d\'Età')

    buffer = BytesIO()
    plt.savefig(buffer, format='png', dpi=150)
    buffer.seek(0)
    plt.close(fig)
    return buffer



class ChartReport(PDFReport):
    def draw_body(self, canvas):
        """Disegna i grafici nel report."""
        width, height = self.page_size
        row_y = height - 230  # Partenza dopo l'header
        col_x = 50  # Margine sinistro

        # Grafico 1: Operatori per Reparto
        operatori_chart = generate_operatori_per_reparto_chart()

        # Crea un file temporaneo per il grafico
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
            temp_file.write(operatori_chart.getvalue())
            temp_file_path = temp_file.name

        # Inserisci il grafico nel canvas
        canvas.drawImage(temp_file_path, col_x, row_y, width=250, height=150)

        # Grafico 2: Fasce d'età
        age_groups_chart = generate_age_groups_chart()

        # Crea un altro file temporaneo per il secondo grafico
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
            temp_file.write(age_groups_chart.getvalue())
            temp_file_path = temp_file.name

        # Inserisci il grafico nel canvas
        canvas.drawImage(temp_file_path, col_x + 300, row_y, width=250, height=150)

        # Aggiorna posizione per il prossimo contenuto
        row_y -= 200

        # Controlla se serve un'altra pagina
        if row_y < 60:  # Spazio per il footer
            canvas.showPage()
            row_y = height - 100