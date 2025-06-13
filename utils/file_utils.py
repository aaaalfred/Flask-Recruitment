import os
from flask import current_app

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def get_file_size(file_obj):
    file_obj.seek(0, os.SEEK_END)
    size = file_obj.tell()
    file_obj.seek(0)
    return size

def validate_file_upload(file):
    """Valida que el archivo cumple con los requisitos"""
    if not file or file.filename == '':
        return {'valid': False, 'error': 'No se seleccionó ningún archivo'}
    
    if not allowed_file(file.filename):
        return {'valid': False, 'error': 'Tipo de archivo no permitido'}
    
    # Verificar tamaño
    file_size = get_file_size(file)
    if file_size > current_app.config['MAX_CONTENT_LENGTH']:
        return {'valid': False, 'error': 'El archivo es demasiado grande'}
    
    return {'valid': True, 'size': file_size}
