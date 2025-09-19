import re
import csv

# File di input (testo)
file_txt = "articoli.txt"
# File CSV di output
file_csv = "frasi_articoli.csv"

# Funzione per spezzare e normalizzare le frasi
def spezza_in_frasi(testo):
    frasi = testo.split(".")
    risultati = []
    for frase in frasi:
        frase = frase.strip().lower()
        frase = re.sub(r"\s+", " ", frase)  # Rimuove spazi multipli
        if frase:
            risultati.append(f"{frase};0;0;0;0;0")
    return risultati

# 1. Legge l’intero file
with open(file_txt, "r", encoding="utf-8") as f:
    contenuto = f.read()

# 2. Estrae tutti i blocchi dopo le righe che iniziano con "~", fino a "---"
blocchi_articoli = re.findall(r"~ [^\n]+\n(.*?)(?=---)", contenuto, flags=re.DOTALL)

# 3. Per ogni blocco, estrai le frasi
tutte_le_frasi = []
for blocco in blocchi_articoli:
    frasi = spezza_in_frasi(blocco)
    tutte_le_frasi.extend(frasi)

# 4. Scrivi le frasi nel file CSV
with open(file_csv, "w", newline='', encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile, delimiter=";")
    for riga in tutte_le_frasi:
        writer.writerow(riga.split(";"))
