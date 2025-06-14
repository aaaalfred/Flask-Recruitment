from flask import Flask, jsonify
from extensions import db, login_manager, jwt, migrate, cors
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)
    
    # Configure login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor inicia sesión para acceder a esta página.'
    
    # Import models for migrations
    from models import Usuario, Vacante, Candidato, Documento, Entrevista, CandidatosPositions
    
    # Register blueprints
    from routes.auth_routes import auth_bp
    from routes.usuario_routes import usuario_bp
    from routes.vacante_routes import vacante_bp
    from routes.candidato_routes import candidato_bp
    from routes.documento_routes import documento_bp
    from routes.entrevista_routes import entrevista_bp
    from routes.candidatos_posiciones_routes import candidatos_posiciones_bp
    from routes.reports_routes import reports_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(usuario_bp, url_prefix='/api/usuarios')
    app.register_blueprint(vacante_bp, url_prefix='/api/vacantes')
    app.register_blueprint(candidato_bp, url_prefix='/api/candidatos')
    app.register_blueprint(documento_bp, url_prefix='/api/documentos')
    app.register_blueprint(entrevista_bp, url_prefix='/api/entrevistas')
    app.register_blueprint(candidatos_posiciones_bp, url_prefix='/api/candidatos-posiciones')
    app.register_blueprint(reports_bp, url_prefix='/api/reports')
    
    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'healthy',
            'message': 'API funcionando correctamente',
            'version': '1.0.0'
        }), 200
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'message': 'Endpoint no encontrado'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({'message': 'Error interno del servidor'}), 500
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'message': 'Petición inválida'}), 400
    
    # ❌ REMOVIDO: CORS duplicado que causaba el error
    # ❌ El @app.after_request estaba duplicando los headers CORS
    # ✅ Ahora solo usamos la configuración en extensions.py
    
    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        # Import models
        from models import Usuario, Vacante, Candidato, Documento, Entrevista, CandidatosPositions
        db.create_all()
        print("🚀 Servidor iniciado en http://localhost:5000")
        print("📋 API disponible en http://localhost:5000/api")
        print("💊 Health check en http://localhost:5000/api/health")
        print("✅ CORS configurado correctamente (sin duplicados)")
    app.run(debug=True, host='0.0.0.0', port=5000)
