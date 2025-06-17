from django.db import models
from django.conf import settings
from offers.models import RideRequest, RideOffer
from accounts.models import Vehicle
from decimal import Decimal
from io import BytesIO
from django.core.files import File
from django.utils.timezone import now

class RideInvoice(models.Model):
    # Références essentielles
    ride_request = models.OneToOneField(RideRequest, on_delete=models.CASCADE, related_name="invoice")
    ride_offer = models.ForeignKey(RideOffer, on_delete=models.SET_NULL, null=True, blank=True, related_name="invoices")
    
    # Participants
    passenger = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="invoices_received")
    driver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="invoices_given")

    # Véhicule utilisé (snapshot)
    vehicle_brand = models.CharField(max_length=100)
    vehicle_model = models.CharField(max_length=100)
    vehicle_plate = models.CharField(max_length=50)

    # Trajet
    start_point = models.CharField(max_length=255)
    end_point = models.CharField(max_length=255)
    date_trajet = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    # Prix
    price_type = models.CharField(max_length=10, choices=[("FIXE", "Fixe"), ("DYNAMIQUE", "Automatique"), ("GRATUIT", "Gratuit")])
    price_applied = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal(0))

    # Tracking + matching
    start_latitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    start_longitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    end_latitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    end_longitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    eta_minutes = models.PositiveIntegerField(null=True, blank=True)

    # Technique
    generated_at = models.DateTimeField(auto_now_add=True)
    pdf = models.FileField(upload_to='invoices/', null=True, blank=True)

    def __str__(self):
        return f"Facture {self.pk} – {self.passenger.get_full_name()} vers {self.end_point}"

    def generate_pdf(self):
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.units import cm

        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        w, h = A4

        p.setFont("Helvetica-Bold", 16)
        p.drawString(2 * cm, h - 2 * cm, "Facture de Covoiturage - IFRI Comotorage")

        p.setFont("Helvetica", 11)
        p.drawString(2 * cm, h - 3 * cm, f"Date d'émission : {self.generated_at.date()}")
        p.drawString(2 * cm, h - 4 * cm, f"Passager : {self.passenger.get_full_name()} ({self.passenger.email})")
        p.drawString(2 * cm, h - 4.8 * cm, f"Conducteur : {self.driver.get_full_name()} ({self.driver.email})")
        p.drawString(2 * cm, h - 5.6 * cm, f"Véhicule : {self.vehicle_brand} {self.vehicle_model} ({self.vehicle_plate})")

        p.drawString(2 * cm, h - 7 * cm, f"Trajet : {self.start_point} → {self.end_point}")
        p.drawString(2 * cm, h - 7.8 * cm, f"Heure : {self.start_time} - {self.end_time} / ETA : {self.eta_minutes} min")

        p.drawString(2 * cm, h - 9 * cm, f"Type de tarification : {self.price_type}")
        p.drawString(2 * cm, h - 9.8 * cm, f"Montant total : {self.price_applied} FCFA")

        p.setFont("Helvetica-Oblique", 10)
        p.drawString(2 * cm, 2 * cm, "Merci d'avoir utilisé notre service. Bon voyage !")

        p.showPage()
        p.save()

        buffer.seek(0)
        self.pdf.save(f"facture_{self.pk}.pdf", File(buffer), save=True)
