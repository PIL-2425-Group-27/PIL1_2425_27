from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def create_offer(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Tu peux récupérer des champs comme ça
            departure_time = data.get('departure_time')
            arrival_time = data.get('arrival_time')

            # Ici tu pourras sauvegarder en base...

            return JsonResponse({'message': 'Offre reçue !', 'data': data}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Requête JSON invalide'}, status=400)

    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

