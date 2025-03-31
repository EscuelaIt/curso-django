from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def saludo(value):
    """
    Añade un saludo al valor proporcionado.
    
    Ejemplo:
    {{ nombre|saludo }} -> Hola, nombre!
    """
    return f"¡Hola, {value}!"

@register.filter
def multiplicar(value, arg):
    """
    Multiplica el valor por el argumento.
    
    Ejemplo:
    {{ 5|multiplicar:3 }} -> 15
    """
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0
    
@register.filter
@stringfilter
def primera_palabra(value):
    """
    Devuelve solo la primera palabra de un texto.
    
    Ejemplo:
    {{ "Hola mundo cruel"|primera_palabra }} -> Hola
    """
    return value.split()[0] if value else ""

@register.filter
def rango(value):
    """
    Crea un rango de números desde 1 hasta el valor proporcionado.
    Útil para hacer bucles for con un número específico de iteraciones.
    
    Ejemplo:
    {% for i in 5|rango %}
        {{ i }}
    {% endfor %}
    Mostrará: 1 2 3 4 5
    """
    try:
        return range(1, int(value) + 1)
    except (ValueError, TypeError):
        return range(0)

@register.filter
def clase_par_impar(value):
    """
    Devuelve 'par' si el número es par, 'impar' si es impar.
    Útil para aplicar clases CSS alternativas en listas.
    
    Ejemplo:
    <li class="{{ forloop.counter|clase_par_impar }}">
    """
    try:
        if int(value) % 2 == 0:
            return "par"
        return "impar"
    except (ValueError, TypeError):
        return "" 