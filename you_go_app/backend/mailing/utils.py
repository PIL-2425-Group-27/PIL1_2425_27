from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags


def send_transactional_email(subject, to_email, template_name, context):
    """
    Envoie un email HTML transactionnel basé sur un template.
    - subject : Sujet du mail.
    - to_email : Destinataire (string ou liste).
    - template_name : Chemin relatif du template HTML.
    - context : Dictionnaire de données pour le rendu du template.
    """

    if isinstance(to_email, str):
        to_email = [to_email]

    from_email = settings.DEFAULT_FROM_EMAIL if hasattr(settings, "DEFAULT_FROM_EMAIL") else settings.EMAIL_HOST_USER

    # Rendu HTML
    html_content = render_to_string(template_name, context)

    # Optionnel : version texte (extrait du HTML de manière simplifiée)
    text_content = render_to_string(template_name, context).replace('<br>', '\n').replace('<p>', '').replace('</p>', '\n')

    # Construction de l’email
    msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    msg.attach_alternative(html_content, "text/html")

    try:
        msg.send()
    except Exception as e:
        print(f"[EMAIL ERROR] Impossible d'envoyer l'email à {to_email} → {str(e)}")
