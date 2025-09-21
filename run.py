# run.py
import os
from app import create_app

app = create_app()

if __name__ == "__main__":
    # Use port 5000 for local development, 5050 for Docker
    # Docker will set FLASK_ENV=production in the environment
    port = 5050 if os.getenv('FLASK_ENV') == 'production' else 15000
    host = '0.0.0.0' if os.getenv('FLASK_ENV') == 'production' else '127.0.0.1'
    
    print(f"Starting Flask app on {host}:{port}")
    app.run(host=host, port=port, debug=True)
