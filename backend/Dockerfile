FROM python:3.11  

# Installez les dépendances nécessaires  
RUN apt-get update && apt-get install -y \
    gdal-bin \
    libgdal-dev \
    && apt-get clean  

# Créez le répertoire de travail  
WORKDIR /app  

# Copiez le requirements.txt et installez les dépendances  
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt  

# Copiez les fichiers de votre projet  
COPY . . 

# Définissez la commande à exécuter  
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]  
EXPOSE 8000