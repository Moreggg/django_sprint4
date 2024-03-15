from django.core.paginator import Paginator

from . import const


def paginate(request, posts):
    paginator = Paginator(posts, const.POSTS_ON_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj
