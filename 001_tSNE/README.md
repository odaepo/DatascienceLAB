# Scopo del drill di data analysis:
Utilizzare nella pipeline il non-linear embedder t-SNE

# Descrizione t-SNE

Sostanzialmente il t-SNE è un non-linear embedder adatto alla riduzione della dimensionalità elevata di un dataset.

https://www.youtube.com/watch?v=MnRskV3NY1k

In questo video Dmitri Kobak spiega la teoria matematica e le sue evoluzioni dietro al t-SNE.
Kobak è attualmente il ricercatore più attivo sul t-SNE ed ha contribuito maggiormente negli ultimi anni alla forma corrente ed ottimizzata.
Il t-SNE è stato proposto per la prima volta da Geoffry Hinton intorno nei primissimi anni 2000.


## Codice

- `00_tSNE.ipynb` contiene codice pytorch per tSNE (ancora non e' stato discusso
- `laboratorio_data_analisi.py` contiene il codice discusso negli incontri
- `data/healthcare-dataset-stroke-data.csv` contiene il dataset selezionato e scaricato da Kaggle https://www.kaggle.com/datasets/fedesoriano/stroke-prediction-dataset

