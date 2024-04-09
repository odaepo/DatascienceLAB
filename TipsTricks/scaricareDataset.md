# Come scaricare il dataset da Kaggle in Google Clolab

Automatizzare lo scaricamento dei dataset da Kaggle in Google Colab puo' essere comodo per avere sempre a disposizione i dati necessari per i propri progetti.


### Creare il file kaggle.json e copiarlo in Google Drive:

Per accedere al dataset è necessario avere un account Kaggle e generare un file di credenziali kaggle.json.

 - Creare un account su Kaggle e accedere al proprio profilo: cliccare sull'icona dell'account in alto a destra e selezionare "Settings".
 - Nella sezione API, cliccare "Create New Token" per scaricare il file kaggle.json.
 - Copiare il file kaggle.json in Google Drive. Nel nostro esempio lo copieremo nella cartella "AI" quindi il percorso del file sarà "AI/kaggle.json". Questo file conterrà le vostre credenziali e ci permetterà di accedere al dataset di Kaggle. Verrà copiato nella directory locale di Google Colab e sarà letto automaticamente dalla libreria per usare le vostre credenziali e scaricare il dataset.

montare il drive:

```python
from google.colab import drive
drive.mount('/content/drive')
```
copiare il file con le credenziali kaggle.json nella cartella locale del progetto in Google Colab:

```python
!cp /content/drive/MyDrive/AI/kaggle.json .
```
verificare che il file sia stato copiato correttamente:

```python
!ls
```


### Installare la libreria:
Nel codice in colab installare la libreria:

```python
!pip install opendatasets --upgrade --quiet
```


### Importare la libreria:

```python
import opendatasets as od

# scegliere il dataset da scaricare
dataset = 'https://www.kaggle.com/datasets/fedesoriano/stroke-prediction-dataset'

# il metodo download prendera' le credenziali direttamente dal file kaggle.json
od.download(dataset)

```



# Altre informazioni utili

 - https://www.kaggle.com/docs/api
 - https://www.kaggle.com/discussions/general/74235
 - https://www.freecodecamp.org/news/how-to-download-kaggle-dataset-to-google-colab/
 - https://saturncloud.io/blog/how-to-use-kaggle-datasets-in-google-colab/
