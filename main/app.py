from flask import Flask
from routes import all_blueprints

app = Flask(__name__)
app.secret_key = "mysecret"

for bp in all_blueprints:
    app.register_blueprint(bp)

if __name__ == "__main__":
    app.run(debug=True)