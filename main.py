#!/usr/bin/env python3
"""
Sistema de Inventario con Arquitectura MVC
Punto de entrada principal de la aplicación
"""
import os
import sys
import django

# Agregar el directorio raíz al path de Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configurar Django
from config.settings import configure_django
configure_django()

# Importar después de configurar Django
from django.core.management import execute_from_command_line
from django.core.wsgi import get_wsgi_application

if __name__ == '__main__':
    # Crear tablas de sesión si no existen
    from django.core.management import call_command
    try:
        call_command('migrate', '--run-syncdb', verbosity=0)
    except Exception as e:
        print(f"Advertencia al crear tablas: {e}")
    
    # Iniciar servidor
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:8081'])
