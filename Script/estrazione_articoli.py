import csv
import re

input_file = "articoli_Parma.txt"
output_pool_esempi = "pool_esempi.csv"
output_pool_articoli = "pool_articoli.csv"

def estrai_corpo(lines):
    # Trova la riga che inizia con ~ (data)
    start_idx = None
    for idx, line in enumerate(lines):
        if line.strip().startswith("~"):
            start_idx = idx
            break
    if start_idx is None or start_idx == len(lines) - 1:
        return ""
    # Prendi tutte le righe DOPO la data (esclude la riga data stessa)
    corpo = [l.strip() for l in lines[start_idx + 1:] if l.strip()]
    # Escludi righe "IN AGGIORNAMENTO"
    corpo = [l for l in corpo if not l.upper().startswith("IN AGGIORNAMENTO")]
    return " ".join(corpo)

with open(input_file, "r", encoding="latin-1") as f:
    content = f.read()

raw_articles = content.split('--- .')

with open(output_pool_esempi, "w", newline="", encoding="utf-8-sig") as f_es, \
     open(output_pool_articoli, "w", newline="", encoding="utf-8-sig") as f_art:

    writer_es = csv.writer(f_es, delimiter=';')
    writer_art = csv.writer(f_art, delimiter=';')
    header = ["articolo", "localizzazione", "tempo", "grave", "moto", "utenti_deboli"]
    writer_es.writerow(header)
    writer_art.writerow(header)

    for idx, raw_article in enumerate(raw_articles):
        article = raw_article.strip()
        if not article:
            continue

        lines = article.splitlines()
        article_text = estrai_corpo(lines)
        article_text = re.sub(r'[\x00-\x1F\x7F]', ' ', article_text)
        article_text = article_text.replace('\xa0', ' ')
        article_text = " ".join(article_text.split())

        if article_text:
            row = [article_text, 0, 0, 0, 0, 0]
            if idx < 200:
                writer_es.writerow(row)
            else:
                writer_art.writerow(row)

print(f"Estrazione completata.\nPrimi 200 articoli in {output_pool_esempi}\nRestanti in {output_pool_articoli}")