from django.http import HttpResponse
from django.template import loader
import django

def welcome(request):
    """
    Vista que muestra la página de bienvenida de Django
    """
    django_version = django.get_version()
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Bienvenido a Django</title>
        <style>
            body {{
                background-color: #f9f9f9;
                color: #333;
                font-family: 'Roboto', 'Lucida Grande', 'DejaVu Sans', 'Bitstream Vera Sans', Verdana, Arial, sans-serif;
                margin: 0;
                padding: 0;
            }}
            #header {{
                background-color: #0C4B33;
                color: white;
                padding: 20px 40px;
                text-align: center;
            }}
            #content {{
                max-width: 800px;
                margin: 20px auto;
                padding: 20px;
                background-color: white;
                border-radius: 5px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }}
            h1 {{
                color: #0C4B33;
                font-weight: 300;
            }}
            h2 {{
                color: #0C4B33;
                font-weight: 300;
            }}
            a {{
                color: #0C4B33;
                text-decoration: none;
            }}
            a:hover {{
                text-decoration: underline;
            }}
            .button {{
                display: inline-block;
                padding: 10px 15px;
                background-color: #0C4B33;
                color: white;
                border-radius: 5px;
                margin-right: 10px;
            }}
            .button:hover {{
                background-color: #0A3929;
                text-decoration: none;
            }}
            .footer {{
                margin-top: 30px;
                border-top: 1px solid #eee;
                padding-top: 10px;
                color: #777;
                font-size: 0.9em;
            }}
        </style>
    </head>
    <body>
        <div id="header">
            <h1>Curso de Django</h1>
            <p>Bienvenido a nuestro curso de Django en Escuela IT</p>
        </div>
        <div id="content">
            <h1>La instalación funcionó correctamente</h1>
            <p>¡Felicidades por tu primera aplicación Django!</p>
            <p>Estás ejecutando Django {django_version}.</p>
            
            <h2>Ejemplos disponibles:</h2>
            <p>
                <a href="/users/" class="button">Gestión de Usuarios</a>
                <a href="/admin/" class="button">Administración</a>
            </p>
            
            <h2>Ejemplos de URLs y vistas:</h2>
            <ul>
                <li><a href="/users/">Home de usuarios</a></li>
                <li><a href="/users/list/">Lista de usuarios</a></li>
                <li><a href="/users/create/">Crear usuario</a></li>
                <li><a href="/users/detail/1/">Detalle de usuario</a></li>
                <li><a href="/users/profile/admin/">Perfil de usuario</a></li>
                <li><a href="/users/archive/2023/12/">Archivo por año/mes</a></li>
                <li><a href="/users/history/2023/">Historial por año</a></li>
                <li><a href="/users/search/admin/">Búsqueda</a></li>
                <li><a href="/users/groups/">Grupos</a></li>
            </ul>
            
            <div class="footer">
                <p>Este es un proyecto de ejemplo para el curso de Django.</p>
            </div>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html) 