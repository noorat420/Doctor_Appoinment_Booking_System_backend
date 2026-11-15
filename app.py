from dotenv import load_dotenv

load_dotenv()

from factory import create_app  # noqa: E402  (env must be loaded before Config is read)

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
