from flask import Flask
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
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(usuario_bp, url_prefix='/api/usuarios')
    app.register_blueprint(vacante_bp, url_prefix='/api/vacantes')
    app.register_blueprint(candidato_bp, url_prefix='/api/candidatos')
    app.register_blueprint(documento_bp, url_prefix='/api/documentos')
    app.register_blueprint(entrevista_bp, url_prefix='/api/entrevistas')
    app.register_blueprint(candidatos_posiciones_bp, url_prefix='/api/candidatos-posiciones')
    
    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        # Import models
        from models import Usuario, Vacante, Candidato, Documento, Entrevista, CandidatosPositions
        db.create_all()
    app.run(debug=True)
