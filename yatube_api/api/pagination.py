from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class CustomPagination(LimitOffsetPagination):

    def get_paginated_response(self, data):
        return Response({
            'links': {},
            'count': self.page.paginator.count,
            'response': data
        })