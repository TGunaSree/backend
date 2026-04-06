

import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
from extensions import db, socketio

jwt = JWTManager()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["100 per minute"],
    storage_uri="memory://",
)

def create_app():
    app = Flask(app.py)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'x7_8a2k9_m3p5_v1q8_z9_w2_x1_y8_z3')
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'n9_b2_v7_c1_x8_z3_m5_p1_q9_w2_k8_l2')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///aigameplatform.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    limiter.init_app(app)
    socketio.init_app(app, async_mode='threadings', cors_allowed_origins="*")
    
    # Register SocketIO namespaces
    from sockets.handlers import TrainingNamespace, ArenaNamespace
    socketio.on_namespace(TrainingNamespace('/training'))
    socketio.on_namespace(ArenaNamespace('/arena'))
    
    # Register blueprints
    from api.auth import auth_bp
    from api.agents import agents_bp
    from api.stats import stats_bp
    from api.report import report_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(agents_bp, url_prefix='/api/agents')
    app.register_blueprint(stats_bp, url_prefix='/api/stats')
    app.register_blueprint(report_bp, url_prefix='/api/reports')
    
    # Create database tables
    with app.app_context():
        db.create_all()
        
    return app

if __name__ == '__main__':
    app = create_app()
    socketio.run(app, debug=True, port=5000)
