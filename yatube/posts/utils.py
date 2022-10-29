from django.conf import settings
from django.core.paginator import Paginator


def paginate_page(request, qs):
    page_num = request.GET.get("page")
    paginator_obj = Paginator(qs, settings.PAGE_LIMIT)
    return paginator_obj.get_page(page_num)
