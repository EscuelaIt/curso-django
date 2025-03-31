from django import template
import datetime

register = template.Library()

@register.simple_tag
def fecha_actual(formato="%d/%m/%Y"):
    """
    Muestra la fecha actual en el formato especificado.
    
    Ejemplo:
    {% fecha_actual %} -> 21/03/2024
    {% fecha_actual "%Y-%m-%d" %} -> 2024-03-21
    """
    return datetime.datetime.now().strftime(formato)

@register.simple_tag
def combinar_strings(valor1, valor2, separador=' '):
    """
    Combina dos strings con un separador.
    
    Ejemplo:
    {% combinar_strings "Hola" "Mundo" %} -> Hola Mundo
    {% combinar_strings "Django" "Templates" "-" %} -> Django-Templates
    """
    return f"{valor1}{separador}{valor2}"

@register.inclusion_tag('users/partials/lista_numerada.html')
def lista_numerada(items, titulo=None):
    """
    Renderiza una lista numerada con los elementos proporcionados.
    
    Ejemplo:
    {% lista_numerada elementos "Mi Lista" %}
    """
    return {
        'items': items,
        'titulo': titulo
    }

@register.tag(name="upper_block")
def do_upper_block(parser, token):
    """
    Convierte todo el contenido del bloque a mayúsculas.
    
    Ejemplo:
    {% upper_block %}
        Este texto aparecerá en mayúsculas
    {% end_upper_block %}
    """
    nodelist = parser.parse(('end_upper_block',))
    parser.delete_first_token()
    return UpperNode(nodelist)

class UpperNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist
    
    def render(self, context):
        output = self.nodelist.render(context)
        return output.upper()

@register.tag(name="repeat")
def do_repeat(parser, token):
    """
    Repite el contenido un número específico de veces.
    
    Ejemplo:
    {% repeat 3 %}
        <p>Este párrafo se repetirá 3 veces</p>
    {% endrepeat %}
    """
    try:
        tag_name, times = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires 1 argument" % token.contents.split()[0]
        )
    
    nodelist = parser.parse(('endrepeat',))
    parser.delete_first_token()
    return RepeatNode(nodelist, times)

class RepeatNode(template.Node):
    def __init__(self, nodelist, times):
        self.nodelist = nodelist
        self.times = times
    
    def render(self, context):
        times = int(self.times)
        output = ""
        for _ in range(times):
            output += self.nodelist.render(context)
        return output 