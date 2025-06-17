# PIL1_2425_27
## Dépôt Github projet intégrateur Groupe 27
 L’application développée met en correspondance des conducteurs et des passagers sur des trajets quotidiens entre leur domicile et le campus. Notre application est basée sur une plateforme de partage de trajet, de covoiturage et de messageri instantannée que nous nommons **« You Go App »**. Les instructions pour le démarrage de l'application sont décrites dans la suite de ce document.


## 🚗 YouGo Frontend – Plateforme de Covoiturage (React): 
Aller dans le dossier frontend dans le terminal de vs code avec 'cd you_go_app/frontend' ou 'cd you_go_app' puis 'cd frontend'

1-    npm install :pour installer toutes les dependances du projet
2-    npm install react-router-dom axios postcss autoprefixer
3-    npm install tailwindcss @tailwindcss/vite
4-    npm install @react-oauth/google(pour l'authentification avec compte google)
5-    npm run dev

## 🚗 YouGo Backend – Plateforme de Covoiturage (Django): 
Le backend du projet est développé avec Django; **Django**, **Django REST Framework**, **WebSockets**, et connecté à une base de données **MySQL** dont les identifiants de connexion sont stockés dans un fichier .env. Il est nécessaire de créer un environnement virtuel avec python si vous developpez deja d'autres solutions sur votre machine avec le langage Python...

 ### 📦 Fonctionnalités principales

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

---

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

### ⚙️ Installation

1. Cloner le repo
2. Créer et configurer `.env` :
    ```env
    DJANGO_SECRET_KEY=...
    DEBUG=True
    DB_NAME=ifri_comotorage_db
    DB_USER=root
    DB_PASSWORD=...
    EMAIL_HOST_USER=note.yougo@outlook.fr
    EMAIL_HOST_PASSWORD=...
    ```

3. Installer les dépendances :
    ```bash
    pip install -r requirements.txt
    ```

4. Appliquer les migrations :
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5. Lancer le serveur :
    ```bash
    python manage.py runserver
    ```

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
