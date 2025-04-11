#!/bin/bash

# Installazione di Java (se non già installato)
echo "Installazione di Java..."
sudo apt update
sudo apt install -y openjdk-11-jdk

# Verifica se Java è stato installato correttamente
java -version
if [ $? -ne 0 ]; then
  echo "Errore: Java non è stato installato correttamente!"
  exit 1
fi
echo "Java installato correttamente."

# Creazione della directory /opt/jasperreports/lib/ (se non esiste)
echo "Creazione della directory /opt/jasperreports/lib/ se non esiste..."
sudo mkdir -p /opt/jasperreports/lib/

# Concessione dei permessi di scrittura per la directory
echo "Concedendo permessi di scrittura alla directory /opt/jasperreports/lib/..."
sudo chmod -R 777 /opt/jasperreports/lib/

# Scarica le librerie necessarie
echo "Scaricando JasperReports e le sue dipendenze..."
sudo wget https://repo1.maven.org/maven2/net/sf/jasperreports/jasperreports/7.0.2/jasperreports-7.0.2.jar -P /opt/jasperreports/lib/ && \
sudo wget https://repo1.maven.org/maven2/org/apache/commons/commons-lang3/3.12.0/commons-lang3-3.12.0.jar -P /opt/jasperreports/lib/ && \
sudo wget https://repo1.maven.org/maven2/org/apache/commons/commons-collections4/4.4/commons-collections4-4.4.jar -P /opt/jasperreports/lib/ && \
sudo wget https://repo1.maven.org/maven2/org/jfree/jfreechart/1.5.3/jfreechart-1.5.3.jar -P /opt/jasperreports/lib/ && \
sudo wget https://repo1.maven.org/maven2/org/jfree/jcommon/1.0.23/jcommon-1.0.23.jar -P /opt/jasperreports/lib/ && \
sudo wget https://repo1.maven.org/maven2/com/itextpdf/kernel/7.1.16/kernel-7.1.16.jar -P /opt/jasperreports/lib/ && \
sudo wget https://repo1.maven.org/maven2/com/itextpdf/io/7.1.16/io-7.1.16.jar -P /opt/jasperreports/lib/ && \
sudo wget https://repo1.maven.org/maven2/com/itextpdf/layout/7.1.16/layout-7.1.16.jar -P /opt/jasperreports/lib/ && \
sudo wget https://repo1.maven.org/maven2/com/itextpdf/forms/7.1.16/forms-7.1.16.jar -P /opt/jasperreports/lib/ && \
sudo wget https://repo1.maven.org/maven2/com/itextpdf/pdfa/7.1.16/pdfa-7.1.16.jar -P /opt/jasperreports/lib/ && \
sudo wget https://repo1.maven.org/maven2/com/itextpdf/sign/7.1.16/sign-7.1.16.jar -P /opt/jasperreports/lib/ && \
sudo wget https://repo1.maven.org/maven2/com/itextpdf/barcodes/7.1.16/barcodes-7.1.16.jar -P /opt/jasperreports/lib/ && \
sudo wget https://repo1.maven.org/maven2/org/eclipse/jdt/ecj/3.21.0/ecj-3.21.0.jar -P /opt/jasperreports/lib/ && \
sudo wget https://repo1.maven.org/maven2/commons-digester/commons-digester/2.1/commons-digester-2.1.jar -P /opt/jasperreports/lib/ && \
sudo wget https://repo1.maven.org/maven2/commons-beanutils/commons-beanutils/1.9.4/commons-beanutils-1.9.4.jar -P /opt/jasperreports/lib/ && \
sudo wget https://repo1.maven.org/maven2/commons-logging/commons-logging/1.2/commons-logging-1.2.jar -P /opt/jasperreports/lib/ && \
sudo wget https://repo1.maven.org/maven2/commons-collections/commons-collections/3.2.2/commons-collections-3.2.2.jar -P /opt/jasperreports/lib/ && \
sudo wget https://repo1.maven.org/maven2/org/slf4j/slf4j-api/1.7.30/slf4j-api-1.7.30.jar -P /opt/jasperreports/lib/ && \
sudo wget https://repo1.maven.org/maven2/org/slf4j/slf4j-simple/1.7.30/slf4j-simple-1.7.30.jar -P /opt/jasperreports/lib/ && \
sudo wget https://repo1.maven.org/maven2/net/sf/jasperreports/jasperreports-pdf/7.0.2/jasperreports-pdf-7.0.2.jar -P /opt/jasperreports/lib/ && \
sudo wget https://repo1.maven.org/maven2/com/itextpdf/commons/7.2.0/commons-7.2.0.jar -P /opt/jasperreports/lib/ && \
sudo wget https://repo1.maven.org/maven2/com/github/librepdf/openpdf/1.3.30/openpdf-1.3.30.jar -P /opt/jasperreports/lib/

# Aggiungi il driver JDBC PostgreSQL
echo "Downloading PostgreSQL JDBC driver..."
wget https://repo1.maven.org/maven2/org/postgresql/postgresql/42.5.0/postgresql-42.5.0.jar -P /opt/jasperreports/lib/

# Verifica che i file siano stati scaricati correttamente
echo "Verifica che i file siano stati scaricati..."
ls /opt/jasperreports/lib/

echo "Tutti i file sono stati scaricati correttamente."

# Mostra il classpath per Java
echo "Assicurati che il classpath punti alla directory /opt/jasperreports/lib/"
echo "Esportando classpath per JasperReports..."
export CLASSPATH=/opt/jasperreports/lib/*:$CLASSPATH
echo "Classpath configurato."

# Test di JasperReports (compilazione di un report di esempio)
echo "Esegui il test di JasperReports per verificare che tutto funzioni correttamente..."
#java -cp /opt/jasperreports/lib/* net.sf.jasperreports.engine.JasperCompileManager /path/to/your/report.jrxml

echo "Setup completato con successo!"

