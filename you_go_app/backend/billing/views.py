from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.http import FileResponse
from django.db import models
from billing.models import RideInvoice
from offers.models import RideRequest
from billing.serializers import RideInvoiceSerializer
from mailing.utils import send_transactional_email  # Assure you have this function in billing/utils.py

class InvoiceListView(generics.ListAPIView):
    """
    Liste toutes les factures pour l'utilisateur connecté (passager ou conducteur).
    """
    serializer_class = RideInvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return RideInvoice.objects.filter(
            models.Q(passenger=user) | models.Q(driver=user)
        ).order_by('-generated_at')


class InvoiceDetailView(generics.RetrieveAPIView):
    """
    Détail d'une facture spécifique.
    """
    serializer_class = RideInvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = RideInvoice.objects.all()

    def get_object(self):
        invoice = super().get_object()
        if self.request.user != invoice.passenger and self.request.user != invoice.driver:
            raise PermissionDenied("Vous n'avez pas accès à cette facture.")
        return invoice


class InvoicePDFDownloadView(APIView):
    """
    Permet de télécharger le PDF de la facture.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, invoice_id):
        invoice = get_object_or_404(RideInvoice, pk=invoice_id)

        if request.user not in [invoice.passenger, invoice.driver]:
            raise PermissionDenied("Accès interdit à ce PDF.")

        if not invoice.pdf:
            invoice.generate_pdf()

        return FileResponse(invoice.pdf.open(), as_attachment=True, filename=f"facture_{invoice.pk}.pdf")


class GenerateInvoiceView(APIView):
    """
    Génère manuellement une facture liée à une demande acceptée.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, ride_request_id):
        ride_request = get_object_or_404(RideRequest, id=ride_request_id)

        if ride_request.status != "ACCEPTEE":
            return Response({"error": "La demande n'est pas encore acceptée."}, status=status.HTTP_400_BAD_REQUEST)

        # Vérifie si la facture existe déjà
        if hasattr(ride_request, 'invoice'):
            return Response({"message": "Facture déjà existante."}, status=status.HTTP_200_OK)

        ride_offer = ride_request.offre_associee
        driver = ride_offer.driver

        # Construction de la facture
        invoice = RideInvoice.objects.create(
            ride_request=ride_request,
            ride_offer=ride_offer,
            passenger=ride_request.passenger,
            driver=driver,
            vehicle_brand=ride_offer.get_vehicle_info().get("brand", "N/A"),
            vehicle_model=ride_offer.get_vehicle_info().get("model", "N/A"),
            vehicle_plate=ride_offer.get_vehicle_info().get("plate", "N/A"),
            start_point=ride_offer.start_point,
            end_point=ride_offer.end_point,
            date_trajet=ride_offer.date_trajet,
            start_time=ride_offer.start_time,
            end_time=ride_offer.end_time,
            price_type=ride_offer.price_type,
            price_applied=ride_offer.price or 0,
            start_latitude=ride_offer.start_latitude,
            start_longitude=ride_offer.start_longitude,
            end_latitude=ride_offer.end_latitude,
            end_longitude=ride_offer.end_longitude,
            eta_minutes=ride_request.eta_minutes or None,
        )

        invoice.generate_pdf()
        # Enregistre le PDF dans le modèle
        invoice.pdf.save(f"facture_{invoice.pk}.pdf", invoice.pdf, save=True)
        send_transactional_email(
        subject="🧾 Facture YouGo - Trajet effectué",
        to_email=invoice.user.email,
        template_name="emails/facture_traject.html",
        context={
            "user": invoice.user,
            "invoice": invoice,
            "passenger": invoice.passenger,
            "driver": invoice.driver,
            "prix": invoice.amount,
            "pdf_url": invoice.pdf_file.url if invoice.pdf_file else None
        }
    )
        
        return Response({"message": "Facture générée avec succès."}, status=status.HTTP_201_CREATED)
