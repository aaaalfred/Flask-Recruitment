import boto3
from botocore.exceptions import ClientError, NoCredentialsError
import uuid
import os
from flask import current_app

class S3Service:
    def __init__(self):
        self.s3_client = None
        self.bucket_name = None
        self._initialize_client()
    
    def _initialize_client(self):
        try:
            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=current_app.config['AWS_ACCESS_KEY_ID'],
                aws_secret_access_key=current_app.config['AWS_SECRET_ACCESS_KEY'],
                region_name=current_app.config['AWS_S3_REGION']
            )
            self.bucket_name = current_app.config['AWS_S3_BUCKET']
        except Exception as e:
            current_app.logger.error(f"Error inicializando cliente S3: {str(e)}")
            raise
    
    def upload_file(self, file_obj, file_name, content_type, folder='documents'):
        """
        Sube un archivo a S3 y retorna la URL y key
        """
        try:
            # Generar nombre único para el archivo
            file_extension = os.path.splitext(file_name)[1]
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            key = f"{folder}/{unique_filename}"
            
            # Subir archivo
            self.s3_client.upload_fileobj(
                file_obj,
                self.bucket_name,
                key,
                ExtraArgs={
                    'ContentType': content_type,
                    'ACL': 'private'  # Archivos privados por defecto
                }
            )
            
            # Generar URL
            url = f"https://{self.bucket_name}.s3.{current_app.config['AWS_S3_REGION']}.amazonaws.com/{key}"
            
            return {
                'success': True,
                'url': url,
                'key': key,
                'message': 'Archivo subido exitosamente'
            }
            
        except NoCredentialsError:
            return {
                'success': False,
                'error': 'Credenciales de AWS no configuradas correctamente'
            }
        except ClientError as e:
            return {
                'success': False,
                'error': f'Error del cliente S3: {str(e)}'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Error inesperado: {str(e)}'
            }
    
    def delete_file(self, key):
        """
        Elimina un archivo de S3
        """
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=key)
            return {'success': True, 'message': 'Archivo eliminado exitosamente'}
        except ClientError as e:
            return {'success': False, 'error': f'Error eliminando archivo: {str(e)}'}
    
    def generate_presigned_url(self, key, expiration=3600):
        """
        Genera una URL firmada para descargar un archivo privado
        """
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': key},
                ExpiresIn=expiration
            )
            return {'success': True, 'url': url}
        except ClientError as e:
            return {'success': False, 'error': f'Error generando URL: {str(e)}'}
