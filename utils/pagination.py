from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    # Default page number, you can save as constant
    page = 1
    # Default page size
    page_size = 10
    # Query parameter for dynamically setting page size
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),  # Link to the next page of results
                'previous': self.get_previous_link()  # Link to the previous page of results
            },
            'total': self.page.paginator.count,  # Total count of objects across all pages
            'page': int(self.request.GET.get('page', 1)),  # can not set default = self.page # Current page number
            'page_size': int(self.request.GET.get('page_size', self.page_size)),  # Current page size
            'results': data  # Results of the current page
        })
