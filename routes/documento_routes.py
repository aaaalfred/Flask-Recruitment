from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from services.auth_service import token_required
from services.s3_service import S3Service
from models import Documento, Candidato, db
from utils.file_utils import validate_file_upload

documento_bp = Blueprint('documento', __name__)

@documento_bp.route('/upload', methods=['POST'])
@token_required
def upload_documento(current_user):
    try:
        # Verificar que se envió un archivo
        if 'file' not in request.files:
            return jsonify({'message': 'No se encontró archivo'}), 400
        
        file = request.files['file']
        candidato_id = request.form.get('candidato_id')
        tipo = request.form.get('tipo', 'otro')
        
        if not candidato_id:
            return jsonify({'message': 'candidato_id es requerido'}), 400
        
        # Verificar que el candidato existe
        candidato = Candidato.query.get(candidato_id)
        if not candidato:
            return jsonify({'message': 'Candidato no encontrado'}), 404
        
        # Verificar permisos
        if (current_user.rol == 'reclutador' and 
            candidato.reclutador_id != current_user.id):
            return jsonify({'message': 'Sin permisos para subir archivos a este candidato'}), 403
        
        # Validar archivo
        validation = validate_file_upload(file)
        if not validation['valid']:
            return jsonify({'message': validation['error']}), 400
        
        # Subir a S3
        s3_service = S3Service()
        upload_result = s3_service.upload_file(
            file_obj=file,
            file_name=secure_filename(file.filename),
            content_type=file.content_type,
            folder=f'candidatos/{candidato_id}'
        )
        
        if not upload_result['success']:
            return jsonify({'message': upload_result['error']}), 500
        
        # Guardar en base de datos
        nuevo_documento = Documento(
            nombre_original=file.filename,
            url_s3=upload_result['url'],
            key_s3=upload_result['key'],
            tipo=tipo,
            candidato_id=candidato_id,
            tamaño_bytes=validation['size'],
            content_type=file.content_type
        )
        
        db.session.add(nuevo_documento)
        
        # Si es un CV, actualizar el candidato
        if tipo == 'cv':
            candidato.cv_url = upload_result['url']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Archivo subido exitosamente',
            'documento': nuevo_documento.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error subiendo archivo: {str(e)}'}), 500

@documento_bp.route('/<int:documento_id>', methods=['GET'])
@token_required
def get_documento(current_user, documento_id):
    try:
        documento = Documento.query.get_or_404(documento_id)
        
        # Verificar permisos
        if (current_user.rol == 'reclutador' and 
            documento.candidato_rel.reclutador_id != current_user.id):
            return jsonify({'message': 'Sin permisos para ver este documento'}), 403
        
        # Generar URL firmada para descarga
        s3_service = S3Service()
        url_result = s3_service.generate_presigned_url(documento.key_s3)
        
        if not url_result['success']:
            return jsonify({'message': url_result['error']}), 500
        
        documento_dict = documento.to_dict()
        documento_dict['download_url'] = url_result['url']
        
        return jsonify(documento_dict), 200
        
    except Exception as e:
        return jsonify({'message': f'Error obteniendo documento: {str(e)}'}), 500

@documento_bp.route('/<int:documento_id>', methods=['DELETE'])
@token_required
def delete_documento(current_user, documento_id):
    try:
        documento = Documento.query.get_or_404(documento_id)
        
        # Verificar permisos
        if (current_user.rol == 'reclutador' and 
            documento.candidato_rel.reclutador_id != current_user.id):
            return jsonify({'message': 'Sin permisos para eliminar este documento'}), 403
        
        # Eliminar de S3
        s3_service = S3Service()
        s3_service.delete_file(documento.key_s3)
        
        # Eliminar de base de datos
        db.session.delete(documento)
        db.session.commit()
        
        return jsonify({'message': 'Documento eliminado exitosamente'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error eliminando documento: {str(e)}'}), 500
