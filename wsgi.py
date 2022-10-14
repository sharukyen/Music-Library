"""App entry point."""
from music import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host='localhost', port=8007, threaded=False)