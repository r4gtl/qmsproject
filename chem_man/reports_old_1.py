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
from core.reports import check_vertical_limit


def generate_order_report(request, ordine_id):
    # Recupera l'ordine e il fornitore associato
    ordine = OrdineProdottoChimico.objects.get(id=ordine_id)
    fornitore = ordine.fk_fornitore

    logo_path = finders.find("images/Lavezzo LOGO.jpg")
    print(f"logo_path: {logo_path}")
    # Recupera il nome del sito dal context processor
    nome_sito_value = nome_sito(request).get("nome_sito", "")
    nome_utente = f"{request.user.first_name} {request.user.last_name}"
    # Imposta la risposta HTTP per il PDF
    response = HttpResponse(content_type="application/pdf")
    # response['Content-Disposition'] = f'attachment; filename="ordine_{ordine.numero_ordine}.pdf"'
    response["Content-Disposition"] = (
        f"inline; filename=ordine_{ordine.numero_ordine}.pdf"
    )
    # Crea il canvas per il PDF
    c = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # Margini di pagina
    x_margin = 2 * cm
    y_margin = 1.5 * cm

    # Numero di pagina totale (per la numerazione)
    # total_pages = 1  # Iniziamo con una pagina, verrà aggiornata durante il processo

    header_height = draw_header(
        c,
        fornitore,
        ordine,
        width,
        height,
        x_margin,
        y_margin,
        logo_path,
        nome_sito_value,
    )

    # Calcola la posizione verticale dopo l'intestazione
    current_y = height - y_margin - header_height - 20  # -20 per il margine interno

    # Disegna il testo verticale sul lato destro
    draw_vertical_text(
        c,
        "M.7.4.2/01 - Rev. 1 del 04/12/2006 - Redatto da x - Approvato da RQ",
        font_size=6,
        width=width,
        height=height,
    )

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
    )
    draw_footer(
        c, ordine, width, height, x_margin, y_margin, nome_sito_value, nome_utente
    )
    page_num = 1
    total_pages = 1  # Modificabile se hai pagine multiple
    draw_footer_date_and_pages(
        c, width, height, x_margin, y_margin, page_num, total_pages
    )

    # Salva il PDF
    c.showPage()
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
    c, ordine, width, height, x_margin, y_margin, current_y, logo_path, nome_sito_value
):
    # Posizione iniziale sotto l'intestazione
    y_position = current_y

    # Margine inferiore per il contenuto
    bottom_margin = y_margin + 200

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
        # Verifica il limite verticale
        y_position = check_vertical_limit(
            c,
            y_position,
            bottom_margin,
            height,
            draw_page_content=draw_header_and_table_headers(
                c, ordine, width, height, x_margin, y_margin, logo_path, nome_sito_value
            ),
            # ordine=ordine,
            # width=width,
            # height=height,
            # x_margin=x_margin,
            # y_margin=y_margin,
        )

        # Aggiungi la riga di dati
        prodotto = dettaglio.fk_prodotto_chimico
        c.drawString(x_margin, y_position, prodotto.descrizione)
        c.drawString(x_margin + 150, y_position, dettaglio.u_misura)
        c.drawString(x_margin + 250, y_position, str(dettaglio.quantity))
        c.drawString(x_margin + 350, y_position, str(dettaglio.fk_imballaggio))
        y_position -= 12

    return y_position  # Restituisci la posizione finale


def draw_header_and_table_headers(
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
    c.drawString(x_margin + 350, height - y_margin - 100, "Aspetto dei beni")


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
    y_position = y_margin + 20  # Posizione verticale per il piè di pagina
    c.setFont("Helvetica", 8)

    # Disegna la riga orizzontale
    c.setStrokeColorRGB(0, 0, 0)  # Colore nero per la riga
    c.setLineWidth(1)  # Spessore della riga
    c.line(x_margin, y_position, width - x_margin, y_position)
    y_position = y_margin + 10
    # Data di stampa
    c.drawString(
        x_margin, y_position, f"Data di Stampa: {datetime.now().strftime('%d/%m/%Y')}"
    )

    # Pagina x di y
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
