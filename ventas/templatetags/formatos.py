from django import template

register = template.Library()

@register.filter
def formato_chileno(valor):
    try:
        valor = int(round(float(valor)))
        return '{0:,}'.format(valor).replace(',', '.')
    except:
        return valor