import pandas as pd
from sklearn.metrics import f1_score

def calculate_f1_scores_per_label_from_files(true_labels_path, predicted_labels_path):
    """
    Calcola l'F1-score per ogni etichetta leggendo i dati da file CSV.

    Args:
        true_labels_path (str): Percorso del file CSV contenente le etichette vere.
        predicted_labels_path (str): Percorso del file CSV contenente le etichette predette.

    Returns:
        dict: Un dizionario dove le chiavi sono i nomi delle etichette e i valori sono i loro F1-score.
              Ritorna None se ci sono discrepanze nelle colonne o nella lunghezza dei dati.
    """
    try:
        true_df = pd.read_csv(true_labels_path, sep=';')
        predicted_df = pd.read_csv(predicted_labels_path, sep=';')
    except FileNotFoundError:
        print("Errore: Uno o entrambi i file non trovati. Controlla i percorsi.")
        return None
    except Exception as e:
        print(f"Errore durante la lettura dei file: {e}")
        return None

    # Identifica le colonne delle etichette (escludendo 'frase' se presente)
    label_columns_true = true_df.columns[1:] if 'frase' in true_df.columns else true_df.columns
    label_columns_pred = predicted_df.columns[1:] if 'frase' in predicted_df.columns else predicted_df.columns

    if not label_columns_true.equals(label_columns_pred):
        print("Errore: I nomi delle colonne nei dati veri e predetti non corrispondono.")
        return None

    if len(true_df) != len(predicted_df):
        print("Errore: Il numero di righe nei dati veri e predetti non corrisponde.")
        return None

    f1_scores = {}
    for column in label_columns_true:
        true_labels = true_df[column]
        predicted_labels = predicted_df[column]
        score = f1_score(true_labels, predicted_labels, average='binary')
        f1_scores[column] = score

    return f1_scores

true_data_filepath = 'risultati_veri.csv'
predicted_data_filepath = 'single-phrase-single-label.csv'


# Calcola gli F1-score
print(f"Caricamento delle etichette vere da: {true_data_filepath}")
print(f"Caricamento delle etichette predette da: {predicted_data_filepath}")
f1_results = calculate_f1_scores_per_label_from_files(true_data_filepath, predicted_data_filepath)

if f1_results:
    print("\nF1-Scores per etichetta:")
    for label, score in f1_results.items():
        print(f"- {label}: {score:.4f}")
