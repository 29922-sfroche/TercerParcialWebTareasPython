import os
import importlib.util
import sys
import traceback
import re
import gc
from io import BytesIO 
from flask import Flask, render_template, send_from_directory, request

# Importaciones para manejar Apps Flask y Middlewares
from werkzeug.test import Client
from werkzeug.wrappers import Response

# ==========================================
# CONFIGURACIÓN INICIAL
# ==========================================
directorio_base = os.path.dirname(os.path.abspath(__file__))
ruta_templates = os.path.join(directorio_base, 'templates')

app = Flask(__name__, template_folder=ruta_templates)

# ==========================================
# LÓGICA DE LIMPIEZA Y EJECUCIÓN
# ==========================================

def limpiar_modulos_de_directorio(directorio):
    """Elimina de la memoria de Python cualquier módulo cargado desde una carpeta específica"""
    directorio = os.path.abspath(directorio)
    para_eliminar = []
    for nombre_mod, mod in list(sys.modules.items()):
        if hasattr(mod, '__file__') and mod.__file__:
            path_mod = os.path.abspath(mod.__file__)
            if path_mod.startswith(directorio):
                para_eliminar.append(nombre_mod)
    
    for nombre in para_eliminar:
        del sys.modules[nombre]
    
    # Forzar al recolector de basura
    gc.collect()

def ejecutar_flask_hijo(ruta_archivo_py, metodo='GET', datos=None, ruta_interna='/'):
    directorio_script = os.path.dirname(ruta_archivo_py)
    nombre_modulo = "modulo_dinamico" # Usamos un nombre fijo para evitar saturación
    
    try:
        # 1. Limpieza previa antes de cargar (por si acaso)
        limpiar_modulos_de_directorio(directorio_script)
        
        # 2. Configuración del cargador
        spec = importlib.util.spec_from_file_location(nombre_modulo, ruta_archivo_py)
        modulo = importlib.util.module_from_spec(spec)
        
        # Insertar el directorio al inicio de sys.path para que los imports locales funcionen
        if directorio_script not in sys.path:
            sys.path.insert(0, directorio_script)
        
        spec.loader.exec_module(modulo)
        
        if hasattr(modulo, 'app'):
            app_hija = modulo.app
            app_hija.root_path = directorio_script
            
            # Cliente de ejecución
            cliente = app_hija.test_client()

            try:
                # Ejecutar la petición dentro del contexto de la app hija
                with app_hija.app_context():
                    if metodo == 'POST':
                        respuesta = cliente.post(ruta_interna, data=datos, follow_redirects=True)
                    else:
                        respuesta = cliente.get(ruta_interna, follow_redirects=True)
                    
                    # Extraer datos antes de destruir todo
                    data = respuesta.get_data()
                    status = respuesta.status_code
                    headers = dict(respuesta.headers)
                    return data, status, headers

            except Exception as e:
                return f"<h1>Error en ejecución interna</h1><p>{str(e)}</p>".encode(), 500, {}
        else:
            return "<h1>Error</h1><p>No se encontró la variable 'app' en el script.</p>".encode(), 500, {}

    except Exception:
        return f"<h1>Error Crítico</h1><pre>{traceback.format_exc()}</pre>".encode(), 500, {}
    
    finally:
        # 3. LIMPIEZA PROFUNDA (Esto evita que el servidor se cuelgue)
        limpiar_modulos_de_directorio(directorio_script)
        if directorio_script in sys.path:
            sys.path.remove(directorio_script)

# ==========================================
# ESCANEO Y RUTAS (Sin cambios importantes aquí)
# ==========================================

def escanear_arbol(ruta_actual):
    estructura = {'archivos': [], 'subcarpetas': {}}
    try:
        items = sorted(os.listdir(ruta_actual))
        for item in items:
            ruta_completa = os.path.join(ruta_actual, item)
            if item in ['__pycache__', '.git', 'static', 'venv'] or item == 'menu.html':
                continue
            if os.path.isdir(ruta_completa):
                contenido = escanear_arbol(ruta_completa)
                if contenido['archivos'] or contenido['subcarpetas']:
                    estructura['subcarpetas'][item] = contenido
            elif os.path.isfile(ruta_completa) and item.lower().endswith('.py'):
                estructura['archivos'].append(item)
    except Exception: pass
    return estructura

@app.route('/')
def menu_principal():
    arbol = escanear_arbol(ruta_templates)
    return render_template('menu.html', arbol=arbol)

@app.route('/ver/<path:ruta_archivo>', methods=['GET', 'POST'])
def servir_proyecto(ruta_archivo):
    if '.py' in ruta_archivo:
        partes = ruta_archivo.split('.py', 1)
        ruta_script_rel = partes[0] + '.py'
        ruta_interna = partes[1] if partes[1] else '/'
    else:
        ruta_script_rel = ruta_archivo
        ruta_interna = '/'

    ruta_abs = os.path.normpath(os.path.join(ruta_templates, ruta_script_rel))

    if not os.path.exists(ruta_abs):
        return "404 No encontrado", 404

    # Manejo de archivos estáticos (CSS, Imágenes)
    extensiones_web = ('.png', '.jpg', '.jpeg', '.gif', '.css', '.js', '.ico')
    if ruta_interna.lower().endswith(extensiones_web):
        return send_from_directory(os.path.dirname(ruta_abs), ruta_interna.lstrip('/'))

    if ruta_abs.endswith('.py'):
        datos_post = None
        if request.method == 'POST':
            datos_post = {}
            for k, v in request.form.items(): datos_post[k] = v
            for k, f in request.files.items():
                datos_post[k] = (BytesIO(f.read()), f.filename, f.mimetype)

        # --- CORRECCIÓN INICIO: Propagar Query String (GET params) ---
        if request.query_string:
            qs = request.query_string.decode("utf-8")
            # Concatenar correctamente dependiendo de si ya existe un '?'
            if '?' in ruta_interna:
                ruta_interna += f"&{qs}"
            else:
                ruta_interna += f"?{qs}"
        # --- CORRECCIÓN FIN ---

        res_data, status, headers = ejecutar_flask_hijo(ruta_abs, request.method, datos_post, ruta_interna)
        
        ctype = headers.get('Content-Type', '')
        if 'text/html' in ctype:
            try:
                html = res_data.decode('utf-8')
                prefix = f"/ver/{ruta_script_rel}"
                # Inyectar el prefijo en las rutas para que el proxy funcione
                html = re.sub(r'(src|href|action)=["\'](/.*?)["\']', rf'\1="{prefix}\2"', html)
                return html, status
            except: pass
        return res_data, status

    return send_from_directory(os.path.dirname(ruta_abs), os.path.basename(ruta_abs))

if __name__ == '__main__':
    # threaded=False es MÁS ESTABLE para carga dinámica de módulos
    # debug=False evita que el reloader bloquee archivos
    app.run(port=5000, debug=False, threaded=False)