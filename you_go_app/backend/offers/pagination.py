# offers/pagination.py

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size = 15  # Nombre par défaut d’éléments par page
    page_size_query_param = 'page_size'  # Permet à l’utilisateur de définir ?page_size=30
    max_page_size = 100  # Pour éviter l’abus de ressources

    def get_paginated_response(self, data):
        return Response({
            "pagination": {
                "current_page": self.page.number,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "total_items": self.page.paginator.count,
                "total_pages": self.page.paginator.num_pages,
            },
            "results": data
        })
