from datetime import (  # Aggiunta in data 08/02/2024 per il totale solventi acquistati nell'anno
    date,
    datetime,
)
from django.contrib.staticfiles import finders
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from qmsproject.context_processors import nome_sito
from .models import (
    OrdineProdottoChimico,
)

# from core.reports import check_vertical_limit


def generate_order_report(request, ordine_id):
    ordine = OrdineProdottoChimico.objects.get(id=ordine_id)
    fornitore = ordine.fk_fornitore

    logo_path = finders.find("images/Lavezzo LOGO.jpg")
    nome_sito_value = nome_sito(request).get("nome_sito", "")
    nome_utente = f"{request.user.first_name} {request.user.last_name}"

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = (
        f"inline; filename=ordine_{ordine.numero_ordine}.pdf"
    )

    c = canvas.Canvas(response, pagesize=A4)
    width, height = A4
    x_margin = 2 * cm
    y_margin = 1.5 * cm
    bottom_margin = y_margin + 50

    # Calcola il numero totale di pagine
    total_pages = calculate_total_pages(ordine, height, y_margin, bottom_margin)

    # Disegna l'intestazione e ottieni la posizione iniziale per il contenuto
    current_y = draw_header_and_table_headers(
        c,
        ordine,
        width,
        height,
        x_margin,
        y_margin,
        logo_path,
        nome_sito_value,
        1,
        total_pages,
    )

    # Disegna il corpo della tabella
    draw_body(
        c,
        ordine,
        width,
        height,
        x_margin,
        y_margin,
        current_y,
        logo_path,
        nome_sito_value,
        total_pages,
    )

    c.save()
    return response


def draw_header(
    c, fornitore, ordine, width, height, x_margin, y_margin, logo_path, nome_sito_value
):
    # Posizione iniziale
    y_position = height - y_margin

    # Altezza totale dell'intestazione calcolata dinamicamente
    used_height = 0

    # Disegna il logo a sinistra
    if logo_path:
        logo_width = 200
        logo_height = 50
        c.drawImage(
            logo_path,
            x_margin,
            y_position - logo_height,
            width=logo_width,
            height=logo_height,
            mask="auto",
        )
        used_height = max(used_height, logo_height)

    # Aggiungi il nome del sito sotto il logo
    if nome_sito:
        c.setFont("Helvetica", 8)
        c.drawString(x_margin, y_position - used_height - 10, nome_sito_value)
        used_height += 10  # Altezza del testo aggiunto

    # Disegna il box con l'indirizzo del fornitore sulla destra
    box_width = 250
    box_height = 80
    box_x = width - x_margin - box_width
    box_y = y_position - box_height
    corner_radius = 10

    c.setLineWidth(0.5)
    c.setStrokeColor(colors.black)
    c.roundRect(box_x, box_y, box_width, box_height, corner_radius)

    # Testo dell'indirizzo del fornitore nel box
    text_x = box_x + 5
    text_y = box_y + box_height - 12
    c.setFont("Helvetica", 10)
    c.drawString(text_x, text_y, f"Fornitore: {fornitore.ragionesociale}")
    text_y -= 12
    c.drawString(text_x, text_y, f"Indirizzo: {fornitore.indirizzo}")
    text_y -= 12
    c.drawString(text_x, text_y, f"Città: {fornitore.city}, {fornitore.cap}")
    text_y -= 12
    c.drawString(
        text_x, text_y, f"Provincia: {fornitore.provincia}, {fornitore.country.name}"
    )
    text_y -= 12
    c.drawString(text_x, text_y, f"Email: {fornitore.e_mail}")

    # Aggiorna l'altezza utilizzata con il box
    used_height = max(used_height, box_height)

    # Dettagli dell'ordine al centro sotto il logo
    details_x = x_margin
    details_y = y_position - used_height - 20
    c.setFont("Helvetica-Bold", 9)
    c.drawString(details_x, details_y, f"Numero Ordine: {ordine.numero_ordine}")
    details_y -= 14
    c.drawString(
        details_x, details_y, f"Data Ordine: {ordine.data_ordine.strftime('%d/%m/%Y')}"
    )
    used_height += 40  # Altezza stimata per i dettagli dell'ordine

    # Linea orizzontale sotto l'intestazione
    line_y = y_position - used_height - 10
    c.setStrokeColor(colors.black)
    c.setLineWidth(1)
    c.line(x_margin, line_y, width - x_margin, line_y)

    # Aggiorna altezza usata per includere la linea
    used_height += 10

    # Restituisci l'altezza totale dell'intestazione
    return used_height


"""def draw_body(c, ordine, width, height, x_margin, y_margin):
    y_position = height - y_margin - 100  # Posizione sotto l'intestazione

    # Titoli della tabella
    c.setFont("Helvetica-Bold", 10)
    c.drawString(x_margin, y_position, "Prodotto")
    c.drawString(x_margin + 150, y_position, "U. Misura")
    c.drawString(x_margin + 250, y_position, "Quantità")
    c.drawString(x_margin + 350, y_position, "Aspetto dei beni")
    y_position -= 20

    # Corpo della tabella con i dettagli
    c.setFont("Helvetica", 10)
    for dettaglio in ordine.dettagli_ordine.all():
        prodotto = dettaglio.fk_prodotto_chimico
        c.drawString(x_margin, y_position, prodotto.descrizione)
        c.drawString(x_margin + 150, y_position, dettaglio.u_misura)
        c.drawString(x_margin + 250, y_position, str(dettaglio.quantity))
        c.drawString(x_margin + 350, y_position, str(dettaglio.fk_imballaggio))
        y_position -= 12

    # Linea di separazione
    y_position -= 10
    c.line(x_margin, y_position, width - x_margin, y_position)"""

""" Inizio prova con gestione limite verticale """


def draw_body(
    c,
    ordine,
    width,
    height,
    x_margin,
    y_margin,
    current_y,
    logo_path,
    nome_sito_value,
    total_pages,
):
    """
    Disegna il corpo della tabella, gestendo la posizione e le nuove pagine.
    """
    y_position = current_y
    bottom_margin = y_margin + 50  # Margine inferiore per il contenuto
    page_num = 1  # Numero di pagina iniziale

    c.setFont("Helvetica", 10)
    for dettaglio in ordine.dettagli_ordine.all():
        # Verifica se è necessario creare una nuova pagina
        y_position, page_num = check_vertical_limit(
            c=c,
            y_position=y_position,
            bottom_margin=bottom_margin,
            draw_page_content=draw_header_and_table_headers,
            page_num=page_num,
            total_pages=total_pages,
            ordine=ordine,
            width=width,
            height=height,
            x_margin=x_margin,
            y_margin=y_margin,
            logo_path=logo_path,
            nome_sito_value=nome_sito_value,
        )

        # Disegna la riga di dettaglio
        prodotto = dettaglio.fk_prodotto_chimico
        c.drawString(x_margin, y_position, prodotto.descrizione)
        c.drawString(x_margin + 150, y_position, dettaglio.u_misura)
        c.drawString(x_margin + 250, y_position, str(dettaglio.quantity))
        c.drawString(x_margin + 350, y_position, str(dettaglio.fk_imballaggio))
        y_position -= 12  # Sposta verso il basso per la prossima riga

    # Disegna il footer sull'ultima pagina
    draw_footer_date_and_pages(
        c, width, height, x_margin, y_margin, page_num, total_pages
    )
    return page_num


def calculate_total_pages(ordine, height, y_margin, bottom_margin):
    """
    Calcola il numero totale di pagine necessarie per il report.
    """
    max_rows_per_page = int(
        (height - y_margin - bottom_margin - 120) / 12
    )  # 12 è l'altezza di ogni riga
    total_rows = ordine.dettagli_ordine.count()
    total_pages = (total_rows // max_rows_per_page) + (
        1 if total_rows % max_rows_per_page != 0 else 0
    )
    return total_pages


def draw_header_and_table_headers(
    c,
    ordine,
    width,
    height,
    x_margin,
    y_margin,
    logo_path,
    nome_sito_value,
    page_num,
    total_pages,
):
    """
    Disegna l'intestazione e i titoli della tabella su ogni nuova pagina.
    """
    draw_header(
        c,
        ordine.fk_fornitore,
        ordine,
        width,
        height,
        x_margin,
        y_margin,
        logo_path,
        nome_sito_value,
    )

    # Disegna il footer con il numero di pagina
    draw_footer_date_and_pages(
        c, width, height, x_margin, y_margin, page_num, total_pages
    )

    # Posizione iniziale per i titoli della tabella
    y_table_headers = height - y_margin - 120
    c.setFont("Helvetica-Bold", 10)
    c.drawString(x_margin, y_table_headers, "Prodotto")
    c.drawString(x_margin + 150, y_table_headers, "U. Misura")
    c.drawString(x_margin + 250, y_table_headers, "Quantità")
    c.drawString(x_margin + 350, y_table_headers, "Aspetto dei beni")

    return y_table_headers - 20  # Restituisce la nuova posizione per il contenuto


'''def draw_header_and_table_headers(
    c, ordine, width, height, x_margin, y_margin, logo_path, nome_sito_value
):
    """
    Funzione che disegna l'intestazione e i titoli della tabella su ogni pagina nuova.
    """
    """draw_header(
        c, ordine.fk_fornitore, ordine, width, height, x_margin, y_margin, None, None
    )"""
    draw_header(
        c,
        ordine.fk_fornitore,
        ordine,
        width,
        height,
        x_margin,
        y_margin,
        logo_path,
        nome_sito_value,
    )
    
    draw_footer_date_and_pages(
        c, width, height, x_margin, y_margin, 0, 0
    )  # Aggiorna il piè di pagina

    # Ridisegna i titoli della tabella
    c.setFont("Helvetica-Bold", 10)
    c.drawString(x_margin, height - y_margin - 100, "Prodotto")
    c.drawString(x_margin + 150, height - y_margin - 100, "U. Misura")
    c.drawString(x_margin + 250, height - y_margin - 100, "Quantità")
    c.drawString(x_margin + 350, height - y_margin - 100, "Aspetto dei beni")'''


def check_vertical_limit(
    c, y_position, bottom_margin, draw_page_content, page_num, total_pages, **kwargs
):
    """
    Controlla se il contenuto ha raggiunto il margine inferiore.
    Se sì, disegna il footer, crea una nuova pagina e ridisegna l'intestazione.
    """
    if y_position <= bottom_margin:
        # Disegna il footer sulla pagina corrente
        draw_footer_date_and_pages(
            c,
            width=kwargs["width"],
            height=kwargs["height"],
            x_margin=kwargs["x_margin"],
            y_margin=kwargs["y_margin"],
            page_num=page_num,
            total_pages=total_pages,
        )
        c.showPage()  # Crea una nuova pagina
        page_num += 1  # Incrementa il numero di pagina
        # Ridisegna l'intestazione e restituisci la nuova posizione iniziale
        y_position = draw_page_content(
            c=c,
            page_num=page_num,
            total_pages=total_pages,
            **kwargs,
        )
    return y_position, page_num


""" Fine prova gestione limite verticale"""


def draw_footer(c, ordine, width, height, x_margin, y_margin, nome_sito, nome_utente):
    y_position = y_margin + 150  # Posizione del footer

    # Dettagli di consegna e conformità
    c.setFont("Helvetica-Bold", 10)
    c.drawString(x_margin, y_position, "Data Consegna:")
    c.drawString(
        x_margin + 100,
        y_position,
        ordine.data_consegna.strftime("%d/%m/%Y") if ordine.data_consegna else "N/A",
    )
    y_position -= 14
    c.drawString(x_margin, y_position, "Conforme:")
    # c.drawString(x_margin + 100, y_position, "Sì" if ordine.is_conforme else "No")
    # Posizione della checkbox
    checkbox_x = x_margin + 100
    checkbox_y = y_position  # Centra verticalmente rispetto al testo
    checkbox_size = 10

    # Disegna la checkbox
    draw_checkbox(c, checkbox_x, checkbox_y, checkbox_size, ordine.is_conforme)

    # Note
    y_position -= 20
    c.drawString(x_margin, y_position, "Note:")
    y_position -= 14
    c.setFont("Helvetica", 10)
    c.drawString(x_margin, y_position, ordine.note if ordine.note else "Nessuna nota")

    y_position -= 14

    # Disegna il riquadro per la firma a destra
    signature_box_width = 120  # Larghezza del riquadro per la firma
    signature_box_height = 40  # Altezza del riquadro per la firma
    signature_box_x = (
        width - x_margin - signature_box_width
    )  # Posizione orizzontale del riquadro
    signature_box_y = (
        y_position - signature_box_height
    )  # Posizione verticale del riquadro

    # Disegna il riquadro
    c.setStrokeColorRGB(0, 0, 0)  # Colore nero per il bordo
    c.setLineWidth(1)  # Spessore del bordo
    c.rect(signature_box_x, signature_box_y, signature_box_width, signature_box_height)

    # Etichetta "Firma"
    c.setFont("Helvetica", 8)
    text_padding = 4  # Spazio tra le righe

    # Calcola la posizione centrale
    site_width = c.stringWidth(nome_sito, "Helvetica", 8)
    user_width = c.stringWidth(nome_utente, "Helvetica", 8)

    # Posizionamento centrato orizzontalmente
    site_x = signature_box_x + (signature_box_width - site_width) / 2
    user_x = signature_box_x + (signature_box_width - user_width) / 2

    # Posizionamento centrato verticalmente
    total_text_height = 16 + text_padding  # Due righe di testo più padding
    start_y = signature_box_y + (signature_box_height - total_text_height) / 2

    # Disegna le righe
    c.drawString(site_x, start_y + 12, nome_sito)  # Nome sito
    c.drawString(user_x, start_y, nome_utente)  # Nome utente

    # c.drawString(signature_box_x + 5, signature_box_y + signature_box_height - 10, nome_sito)
    # c.drawString(signature_box_x + 5, signature_box_y + signature_box_height - 22, nome_utente)  # Nome utente


def draw_footer_date_and_pages(
    c, width, height, x_margin, y_margin, page_num, total_pages
):
    """
    Disegna il piè di pagina con la data di stampa e la numerazione delle pagine.
    Questa funzione verrà eseguita per ogni pagina.
    """
    y_position = y_margin + 20  # Posizione verticale per il footer
    c.setFont("Helvetica", 8)

    # Disegna la linea orizzontale sopra il footer
    c.setStrokeColorRGB(0, 0, 0)
    c.setLineWidth(1)
    c.line(x_margin, y_position, width - x_margin, y_position)

    y_position = y_margin + 10
    # Disegna la data di stampa
    c.drawString(
        x_margin, y_position, f"Data di Stampa: {datetime.now().strftime('%d/%m/%Y')}"
    )
    # Numerazione pagine
    c.drawString(
        width - x_margin - 100, y_position, f"Pagina {page_num} di {total_pages}"
    )


def draw_vertical_text(c, text, font_size, width, height, x_offset=10):
    """
    Disegna un testo verticale sul lato destro del report.

    :param c: Canvas del PDF
    :param text: Il testo da disegnare
    :param font_size: Dimensione del font
    :param width: Larghezza della pagina
    :param height: Altezza della pagina
    :param x_offset: Offset dal bordo destro della pagina
    """
    # Imposta il font e la dimensione
    c.setFont("Helvetica", font_size)

    # Calcola la posizione del testo (sul lato destro)
    x_position = width - x_offset
    y_position = height / 2  # Centrato verticalmente

    # Salva lo stato del canvas
    c.saveState()

    # Traslazione e rotazione per posizionare il testo in verticale
    c.translate(x_position, y_position)
    c.rotate(-90)  # Ruota di 90 gradi in senso orario

    # Disegna il testo
    c.drawString(0, 0, text)

    # Ripristina lo stato del canvas
    c.restoreState()


def draw_checkbox(c, x, y, size, checked):
    """
    Disegna una checkbox in una posizione specifica.

    :param c: Canvas del PDF
    :param x: Coordinata X per la checkbox
    :param y: Coordinata Y per la checkbox
    :param size: Dimensione della checkbox
    :param checked: Booleano che indica se la checkbox è selezionata
    """
    # Disegna il contorno della checkbox
    c.rect(x, y, size, size)

    # Se la checkbox è selezionata, disegna un segno di spunta
    if checked:
        c.setFont("Helvetica-Bold", size)
        c.drawString(x + 2, y + 2, "✓")
