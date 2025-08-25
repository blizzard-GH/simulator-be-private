from flask import Flask
import elasticapm
from elasticapm.contrib.flask import ElasticAPM

app = Flask(__name__)

# Elastic APM configuration
app.config['ELASTIC_APM'] = {
    'SERVICE_NAME': 'flask-apm-test',
    'SERVER_URL': 'http://apm-server:8200',   # APM Server inside docker
    'CAPTURE_HEADERS': True,
    'ENVIRONMENT': 'development',
}

# Attach Elastic APM
apm = ElasticAPM(app)

@app.route("/")
def index():
    return "Hello from Flask APM Test!"

@app.route("/error")
def error():
    # This will show up in APM Errors tab
    raise ValueError("This is a test error for APM!")

@app.route("/apm-test")
def apm_test():
    apm.client.capture_message("APM test message from Flask ✅")
    return {"status": "apm message sent"}
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5060, debug=True)
