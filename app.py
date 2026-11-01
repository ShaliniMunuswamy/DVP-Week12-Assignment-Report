from flask import Flask, jsonify

app = Flask(__name__)


def add(a, b):
    return a + b


@app.route("/")
def home():
    return jsonify(message="Hello from DVP Week 12 CI/CD pipeline!")


@app.route("/health")
def health():
    return jsonify(status="ok")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
