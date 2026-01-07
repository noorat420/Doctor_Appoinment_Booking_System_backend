
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from extensions import init_extensions
from routes import register_routes


load_dotenv()

app = Flask(__name__)
app.config.from_object("config.Config")


CORS(
    app,
    origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "https://docappointments.in",
        "https://www.docappointments.in"
    ],
    supports_credentials=True
)


init_extensions(app)
register_routes(app)

if __name__ == "__main__":
    app.run(debug=True)

