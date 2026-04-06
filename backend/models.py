import uuid
from datetime import datetime
from extensions import db

class User(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    agents = db.relationship('Agent', backref='owner', lazy=True)

class Agent(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    game = db.Column(db.String(50), nullable=False) # e.g., 'Snake', 'Pong'
    algorithm = db.Column(db.String(50), nullable=False) # e.g., 'DQN', 'PPO'
    
    # Hyperparameters
    learning_rate = db.Column(db.Float, default=0.001)
    episodes = db.Column(db.Integer, default=1000)
    exploration_rate = db.Column(db.Float, default=1.0) # initial epsilon
    
    # Status
    status = db.Column(db.String(20), default='pending') # pending, training, completed, failed
    model_path = db.Column(db.String(200), nullable=True) # path to .pt file
    
    # Training results
    final_reward = db.Column(db.Float, nullable=True)
    duration_seconds = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    
    matches_played = db.Column(db.Integer, default=0)
    matches_won = db.Column(db.Integer, default=0)

class MatchHistory(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    agent1_id = db.Column(db.String(36), db.ForeignKey('agent.id'), nullable=False)
    agent2_id = db.Column(db.String(36), db.ForeignKey('agent.id'), nullable=False)
    game = db.Column(db.String(50), nullable=False)
    winner_id = db.Column(db.String(36), db.ForeignKey('agent.id'), nullable=True) # Null for draw
    score_agent1 = db.Column(db.Float, nullable=True)
    score_agent2 = db.Column(db.Float, nullable=True)
    played_at = db.Column(db.DateTime, default=datetime.utcnow)
