# coding=utf-8
from django.template import Library
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings

register = Library()

DEFAULT_PAGINATION = settings.PAGINATION_DEFAULT_PAGINATION
DEFAULT_ORPHANS = settings.PAGINATION_DEFAULT_ORPHANS

def paginate(current, range):

    current_page = current
    page_range = range
    list_pages_range = []

    if page_range:
        
        for i in page_range:
            list_pages_range.append(i)

        if current_page <= 1: # << 1 2 3 ... 10 11 >>
            start = list_pages_range[:3]
            end = list_pages_range[-2:]
            list_pages_range = start + end
            list_pages_range.sort()
            list_pages_range.insert(3, "...")

        elif current_page != 1 and current_page < 6:  # << 1 2 3 4 5 6 7  ... 10 11 >>
            start = list_pages_range[:(current_page + 2)]
            end = list_pages_range[-2:]
            list_pages_range = start + end
            list_pages_range.sort()
            list_pages_range.insert((current_page + 2), "...")

        elif current_page >= 6 and current_page < (len(list_pages_range) - 4): # << 1 2 ... 6 7 8 ... 10 11
            start = list_pages_range[:2]
            middle = list_pages_range[(current_page - 3):(current_page + 2)]
            end = list_pages_range[-2:]
            list_pages_range = start + middle + end
            list_pages_range.sort()
            list_pages_range.insert(2, "...")
            list_pages_range.insert(len(list_pages_range) - 2, "...")

        else:                               # << 1 2 ... 7 8 9 10 11 >>
            start = list_pages_range[:2]
            end = list_pages_range[(current_page - 5):]
            list_pages_range = start + end
            list_pages_range.sort()
            list_pages_range.insert(2, "...")

    else:
        list_pages_range

    return list_pages_range

@register.inclusion_tag('pagination/pagination.html')
def pagination(request, paginator):
    context={}
    pages = []

    page_range = paginator.paginator.page_range
    page_count = paginator.paginator.num_pages
    page_obj = paginator.number

    if page_count <= 10:
        for i in page_range:
            pages.append(i)
    else:
        pages = paginate(page_obj, page_range)

    context['paginator'] = paginator
    context['pages'] = pages
    context['page_obj'] = page_obj
    if page_count > 1:
        context['page_count'] = page_count

    if request:
        getvars = request.GET.copy()
        if 'page' in getvars:
            del getvars['page']
        if len(getvars) > 0:
            context['getvars'] = '&{0}'.format(getvars.urlencode())
        else:
            context['getvars'] = ''

    return context

def pagina(request, list_obj):
    paginator = Paginator(list_obj, DEFAULT_PAGINATION, DEFAULT_ORPHANS)
    page_obj = request.GET.get('page')
    try:
        page_list_obj = paginator.page(page_obj)
    except PageNotAnInteger:
        page_list_obj = paginator.page(1)
    except EmptyPage:
        page_list_obj = paginator.page(paginator.num_pages)
    return page_list_obj