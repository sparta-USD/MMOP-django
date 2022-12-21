from rest_framework.pagination import PageNumberPagination

class PerfumePagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    page_query_param = 'page'

    def get_paginated_response(self, data):
        return {
            'next': self.page.next_page_number() if self.page.has_next() else None,
            'previous': self.page.previous_page_number() if self.page.has_previous() else None,
            'last': (self.page.paginator.count//self.page_size)+1,
            'count': self.page.paginator.count,
            'results': data
        }