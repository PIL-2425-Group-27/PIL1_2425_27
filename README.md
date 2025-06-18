# PIL1_2425_27
## Dépôt Github projet intégrateur Groupe 27
 L’application développée met en correspondance des conducteurs et des passagers sur des trajets quotidiens entre leur domicile et le campus. Notre application est basée sur une plateforme de partage de trajet, de covoiturage et de messagerie instantannée que nous nommons **« You Go App »**. Les instructions pour le démarrage de l'application sont décrites dans la suite de ce document.


![](/capture%20travaux/logo.jpeg)

 ### 📦 Fonctionnalités principales (privilégier le mobile first)

- Authentification personnalisée (email/numéro + mot de passe)
- Gestion des utilisateurs avec rôles (conducteur/passager)
- Support du thème clair/sombre
- KYC (vérification d'identité)
- Suivi GPS avec gestion de consentement + historique des positions
- Création et gestion des offres & demandes de covoiturage
- Estimation dynamique du prix avec OSRM 
- Estimation d'un lieu de rendez-vous entre conducteur - passager
- Matching automatique entre passagers & conducteurs
- Messagerie instantanée texte/audio en temps réel (WebSocket)
- Système de notification (événements, ETA, validation)
- Génération de factures PDF après chaque trajet
- Envoi d'email pour chaque action du KYC, demande accepté ou refusé, etc.
- Statistiques personnalisées (trajets, kilometrage)
- Interface Admin optimisée (Django + Jazzmin)

## 🚗 YouGo Frontend – Plateforme de Covoiturage (React): 
Le frontend a été développé avec **React JS**, **Tailwind CSS**, **Axios**, **Leaflet**. **NodeJS** est requis pour le fonctionnement du projet. Téléchargez **NodeJS** sur le site officiel [NodeJS](https://nodejs.org/en/download) .

## 🚗 YouGo Backend – Plateforme de Covoiturage (Django): 
Le backend du projet est développé avec **Django**, **Django REST Framework**, **WebSockets**, et connecté à une base de données **MySQL** dont les identifiants de connexion sont stockés dans un fichier .env. Il est nécessaire de créer un environnement virtuel avec python si vous developpez deja d'autres solutions sur votre machine avec le langage Python...

### 🛠 Technologies utilisées

- **Backend** : Django 5.2, Django REST Framework
- **Auth** : SimpleJWT + gestion de session sécurisée
- **WebSocket** : Django Channels + Redis
- **Notifications** : Signaux, tâches asynchrones, WebSocket + mail
- **Base de données** : MySQL
- **Asynchrone** : Celery + Redis
- **Email transactionnel** : SMTP (Outlook)
- **Cartographie** : OSRM API + Nominatim
- **PDF** : ReportLab
- **Stockage media** : Local (peut être adapté à S3, Cloudinary, etc.)
- **Thème utilisateur** : `theme_preference` (dark/light)

---

### 📁 Structure principale

- `accounts/` → Authentification, KYC, tracking, profil, reinitialisation password, consentement tracking(GPS)
- `offers/` → Gestion des offres, demandes, matching
- `billing/` → Factures PDF, 
- `geoassist/` → Point de rendez-vous intelligent 
- `notifications/` → Notifications internes, WebSocket
- `chat/` → Messagerie en temps réel
- `*/admin.py` → Interface administrateur avec Jazzmin
- `reviews/` → Fonctions de notations et d'evaluation conducteurs - pssagers
- `mailing/` → Gestion d'envoi de emails 
- `core/` → Configuration principale Django

---

### ⚙️ Installation

Cloner le repo

**Frontend**

1. Ouvrir le dossier principal:
```bash
    cd you_go_app
```
2. Ouvrir le dossier frontend:
```bash
    cd frontend
```
3. Installer les dependances:
```bash
    npm install
    npm install jspdf
```

4. Lancer le projet:
```bash
    npm run dev
```
5. Cliquer sur le lien obtenu en console.

**Backend**

1. Créer et configurer `.env` :
    ```env
    SECRET_KEY=...
    DEBUG=True
    DB_NAME=ifri_comotorage_db
    DB_USER=root
    DB_PASSWORD=...
    DB_HOST=localhost
    DB_PORT=3306
    EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
    EMAIL_HOST=smtp.office365.com
    EMAIL_HOST_USER=note.yougo@outlook.fr
    EMAIL_HOST_PASSWORD=...
    ALLOWED_HOSTS=127.0.0.1,localhost
    ACCESS_TOKEN_LIFETIME_MINUTES=60
    REFRESH_TOKEN_LIFETIME_DAYS=5
    TIME_ZONE=Africa/Porto-Novo
    LOG_LEVEL=INFO
    FRONTEND_BASE_URL=http://localhost:3000

    ```

2. Installer les dépendances :
    ```bash
    pip install -r requirements.txt
    ```

3. Appliquer les migrations :
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

4. Lancer le serveur :
    ```bash
    python manage.py runserver
    ```

---

### 🧪 Tests effectués

- Création utilisateur / login JWT
- Gestion du changement role 
- Publication d'offres et demandes
- Matching / validation covoiturage
- Gestion des notifications (email, push, etc.)
- Envoi de messages WebSocket + vocal
- Gestion des préférences utilisateur (thème, etc.)
- Notifications + facturation
- Gestion des cartes (OSRM, Nominatim, etc.)
- Gestion des événements (calendrier, etc.)
- Gestion des utilisateurs (inscription, connexion, etc.)
- Suivi GPS + ETA en direct
- Gestion des déplacements (itinéraires, etc.)
- Admin KYC / gestion utilisateurs


**Développé avec ❤️ pour une utilisation pratique des outils et techniques apprises dans les enseignements de la 1ère année.**
