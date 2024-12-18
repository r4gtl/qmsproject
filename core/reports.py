# Esempio di struttura iniziale per il modulo `reports.py`

# Funzioni per la gestione dei report


def export_to_csv(queryset, file_path, fields):
    """
    Esporta un queryset in formato CSV.

    Args:
        queryset (QuerySet): Il queryset da esportare.
        file_path (str): Il percorso del file CSV.
        fields (list): I campi da includere nel CSV.

    Returns:
        str: Percorso del file CSV generato.
    """
    import csv

    with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        for obj in queryset:
            writer.writerow({field: getattr(obj, field, "") for field in fields})

    return file_path


def generate_pdf_report(template_path, context, output_path):
    """
    Genera un report PDF basato su un template.

    Args:
        template_path (str): Percorso al file del template.
        context (dict): Contesto per il rendering del template.
        output_path (str): Percorso per salvare il PDF generato.

    Returns:
        str: Percorso del file PDF generato.
    """
    from weasyprint import HTML
    from django.template.loader import render_to_string

    html_content = render_to_string(template_path, context)
    HTML(string=html_content).write_pdf(output_path)

    return output_path


def aggregate_field(queryset, field, agg_func):
    """
    Aggrega un campo in un queryset usando una funzione specifica.

    Args:
        queryset (QuerySet): Il queryset da aggregare.
        field (str): Il campo su cui applicare l'aggregazione.
        agg_func (function): La funzione di aggregazione (es. Sum, Avg).

    Returns:
        any: Il risultato dell'aggregazione.
    """
    from django.db.models import Sum, Avg, Max, Min, Count

    aggregation = {field: agg_func(field)}
    return queryset.aggregate(**aggregation)[field]


def create_summary_report(queryset, fields):
    """
    Crea un report di riepilogo per un queryset.

    Args:
        queryset (QuerySet): Il queryset da riepilogare.
        fields (list): I campi da includere nel riepilogo.

    Returns:
        dict: Riepilogo con i campi e i valori calcolati.
    """
    summary = {}
    for field in fields:
        summary[field] = aggregate_field(queryset, field, Sum)

    return summary