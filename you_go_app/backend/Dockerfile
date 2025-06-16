# Utilise une image officielle Python
FROM python:3.11-slim

# Crée le dossier de travail dans le conteneur
WORKDIR /app

# Copie les fichiers de dépendances
COPY requirements.txt .

# Installe les dépendances système nécessaires
RUN apt-get update && apt-get install -y gcc libpq-dev build-essential

# Installe les dépendances Python
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copie tout le code source dans le conteneur
COPY . .

# Port exposé (si nécessaire pour accès local)
EXPOSE 8000

# Commande de démarrage du conteneur
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
# Optionnel : si vous utilisez une base de données, vous pouvez ajouter des migrations
# RUN python manage.py migrate