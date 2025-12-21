import os

from orders import create_app

FLASK_RUN_PORT = int(os.environ.get("FLASK_RUN_PORT", "5000"))

application = create_app()

if __name__ == "__main__":
    application.run(host="0.0.0.0", port=FLASK_RUN_PORT)
