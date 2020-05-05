from urllib.parse import urlparse

from django.template import Library

from core.models import Menu

register = Library()

@register.inclusion_tag('includes/menu.html', takes_context=True)
def show_menu(context):
    menu_itens_pk = []
    m = Menu.objects.order_by('tree_id').filter(is_active=True)
    return {
        'request': context.get('request', None),
        'menu_itens': m,
    }
@register.filter
def is_active(menu, request):
    menu_url = menu.get_link()
    if menu_url:
        parsed_menu_url = urlparse(menu_url)
        return parsed_menu_url.path == request.path

    return False

@register.filter
def path(menu, request):
    url = request.META['PATH_INFO']
    if url == menu.get_link():
        return True
    return False