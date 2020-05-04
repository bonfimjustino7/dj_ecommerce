from django.template import Library

from core.models import Menu

register = Library()

@register.inclusion_tag('includes/menu.html', takes_context=True)
def show_menu(context):
    menu_itens_pk = []
    for menu in Menu.objects.filter(is_active=True):
        if menu.have_perm(context.get('request').user):
            menu_itens_pk.append(menu.pk)
    m = Menu.objects.order_by('tree_id').filter(pk__in=menu_itens_pk)
    return {
        'request': context.get('request', None),
        'menu_itens': m,
    }