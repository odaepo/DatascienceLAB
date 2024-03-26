# Come scaricare il dataset da Kaggle in Google Clolab

Automatizzare lo scaricamento dei dataset da Kaggle in Google Colab puo' essere comodo per avere sempre a disposizione i dati necessari per i propri progetti.


### Creare il file kaggle.json e copiarlo in Google Drive:

Per accedere al dataset è necessario avere un account Kaggle e generare un file di credenziali kaggle.json.

 - Creare un account su Kaggle e accedere al proprio profilo: cliccare sull'icona dell'account in alto a destra e selezionare "Settings".
 - Nella sezione API, cliccare "Create New Token" per scaricare il file kaggle.json.
 - Copiare il file kaggle.json in Google Drive. Nel nostro esempio lo copieremo nella cartella "AI" quindi il percorso del file sarà "AI/kaggle2.json". Questo file conterrà le vostre credenziali e ci permetterà di accedere al dataset di Kaggle. Verrà copiato nella directory locale di Google Colab e sarà letto automaticamente dalla libreria per usare le vostre credenziali e scaricare il dataset.


### Installare la libreria:
Nel codice in colab installare la libreria:

```python
!pip install opendatasets --upgrade --quiet
```


### Importare la libreria:

```python
import opendatasets as od

# Assign the Kaggle data set URL into variable
dataset = 'https://www.kaggle.com/datasets/fedesoriano/stroke-prediction-dataset'

# Using opendatasets let's download the data sets
od.download(dataset)

```

montare il drive:

```python
from google.colab import drive
drive.mount('/content/drive')
```
copiare il file con le credenziali kaggle.json nella cartella locale:

```python
!cp /content/drive/MyDrive/AI/kaggle.json .
```
verificare che il file sia stato copiato correttamente:

```python
!ls
```


# Altre informazioni utili
https://www.kaggle.com/docs/api
