import os
from kaggle.api.kaggle_api_extended import KaggleApi

# Crea un'istanza dell'API di Kaggle
api = KaggleApi()
api.authenticate()

# Scarica il file
dataset_name = "giobbu/belgium-obu"
api.dataset_download_files(dataset_name, path=".", unzip=True)
print("Download completato.")