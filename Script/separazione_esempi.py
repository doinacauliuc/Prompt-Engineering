import csv
import re

input_file = "articoli_Parma.txt"
output_pool_esempi = "pool_esempi.csv"
output_pool_articoli = "pool_articoli.csv"

with open(input_file, "r", encoding="latin-1") as f:
    content = f.read()

raw_articles = content.split('--- .')

# apriamo i file di output
with open(output_pool_esempi, "w", newline="", encoding="utf-8-sig") as f_es, \
     open(output_pool_articoli, "w", newline="", encoding="utf-8-sig") as f_art:

    writer_es = csv.writer(f_es, delimiter=';')
    writer_art = csv.writer(f_art, delimiter=';')

    # header identico per entrambi
    header = ["articolo", "localizzazione", "tempo", "grave", "moto", "utenti_deboli"]
    writer_es.writerow(header)
    writer_art.writerow(header)

    for idx, raw_article in enumerate(raw_articles):
        article = raw_article.strip()
        if not article:
            continue

        lines = article.splitlines()
        if lines[0].startswith("#https://"):
            lines = lines[1:]

        # ignora titolo e data (~)
        content_lines = [line.strip() for line in lines if line.strip() and not line.startswith("~")]

        article_text = " ".join(content_lines).strip()

        # rimuove la frase finale "IN AGGIORNAMENTO"
        article_text = re.sub(r'\bIN AGGIORNAMENTO\b\.?$', '', article_text, flags=re.IGNORECASE).strip()

        # pulizia caratteri strani e spazi
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
