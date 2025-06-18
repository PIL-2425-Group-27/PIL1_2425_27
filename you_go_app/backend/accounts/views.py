from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import RegisterSerializer
from django.http import JsonResponse


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Utilisateur créé avec succès"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ActiveStatusView(APIView):
    permission_classes = [permissions.AllowAny]

    from django.http import JsonResponse

    def active_status(request):
        return JsonResponse({'active': True})


    def get(self, request):
        # Example: always return True; adapt to your logic (e.g., user.is_authenticated)
        return Response({"active": True})
