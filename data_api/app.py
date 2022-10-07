from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv

load_dotenv()

# Load all Envs/Secrets
DB = os.getenv('DB')
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_PORT = os.getenv('DB_PORT')
DB_SCHEMA = os.getenv('DB_SCHEMA')
DB_TABLE = os.getenv('DB_TABLE')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#DB Model (future improvement to move this to it's own file away from the main app).
class Metrics(db.Model):
    __tablename__ = f'{DB_TABLE}'
    __table_args__ = {"schema": f"{DB_SCHEMA}"}

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.Integer())
    cpu_load = db.Column(db.Integer())
    concurrency = db.Column(db.Integer())

    def __init__(self, timestamp, cpu_load, concurrency):
        self.timestamp = timestamp
        self.cpu_load = cpu_load
        self.concurrency = concurrency

    def __repr__(self):
        return f"<ID {self.id}>"

# Health Route to be used by Uptime Checks to ensure API is alive
@app.route('/healthz')
def hello():
    return {"Ping!"}

# API Metrics Route to query the data
@app.route('/api/metrics', methods=['GET'])
def handle_metrics():
    # IF block to handle start/end values if they are both present. If not, return all data.
    # Future improvement to handle dates better (a user may only want start and not end, and vice versa).
    if request.args.get('start') and request.args.get('end') is not None:
        start = request.args.get('start')
        end = request.args.get('end')
        metrics = Metrics.query.filter(Metrics.timestamp.between(start, end)).all()
        results = [
            {
                "timestamp": metric.timestamp,
                "cpu_load": metric.cpu_load,
                "concurrency": metric.concurrency
            } for metric in metrics]

        return {"count": len(results), "metrics": results, "message": "success"}
    else:
        metrics = Metrics.query.all()
        results = [
            {
                "timestamp": metric.timestamp,
                "cpu_load": metric.cpu_load,
                "concurrency": metric.concurrency
            } for metric in metrics]

        return {"count": len(results), "metrics": results, "message": "success"}


if __name__ == '__main__':
    app.run(debug=True)