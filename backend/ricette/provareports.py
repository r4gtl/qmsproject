import os
import subprocess

from django.conf import settings
from django.http import HttpResponse

from .models import *


def ricetta_rifinizione_jasper(request, pk):
    report_path = os.path.join(settings.BASE_DIR, "jreports", "Finishing_recipe.jasper")
    output_path = os.path.join(settings.BASE_DIR, "jreports", "output_report.pdf")

    # Get database credentials from environment variables or settings
    db_host = os.environ.get("POSTGRES_DB_HOST", "localhost")
    db_port = os.environ.get("POSTGRES_DB_PORT", "5433")
    db_user = os.environ.get("POSTGRES_DB_USER", "postgres")
    db_password = os.environ.get("POSTGRES_DB_PASSWORD", "")
    db_name = os.environ.get("POSTGRES_DB_NAME", "postgres")

    # Create JDBC URL
    db_url = f"jdbc:postgresql://{db_host}:{db_port}/{db_name}"

    # Get the object to verify it exists
    try:
        ricetta = RicettaRifinizione.objects.get(pk=pk)
        print(f"ricetta: {ricetta.data_ricetta}")
        print(f"Generating report with PK: {pk}")
    except RicettaRifinizione.DoesNotExist:
        return HttpResponse(f"RicettaRifinizione with PK {pk} not found", status=404)

    # Build Java command
    command = [
        "java",
        "-cp",
        ".:/opt/jasperreports/lib/*",  # Assicurati che i jar siano nel classpath
        "ReportGenerator",  # Questo è il nome della classe ReportGenerator
        report_path,
        output_path,
        db_url,
        db_user,
        db_password,
        f"PK={pk}",  # Pass PK parameter
    ]

    print(f"Executing command: {' '.join(command)}")

    # Execute Java command
    try:
        result = subprocess.run(
            command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        print(f"Output: {result.stdout.decode()}")
    except subprocess.CalledProcessError as e:
        error_message = e.stderr.decode() if e.stderr else str(e)
        print(f"Error: {error_message}")
        return HttpResponse(f"Error generating report: {error_message}", status=500)

    # Verify file exists
    if not os.path.exists(output_path):
        return HttpResponse("Generated PDF file not found", status=500)

    # Return PDF file
    with open(output_path, "rb") as pdf_file:
        response = HttpResponse(pdf_file.read(), content_type="application/pdf")
        response["Content-Disposition"] = 'inline; filename="report.pdf"'
        return response
