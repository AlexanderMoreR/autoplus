import os
from app import create_app

app = create_app()

if __name__ == "__main__":
    host = os.environ.get('HOST', 'ip')
    port = os.environ.get('PORT', 'puerto')
    app.run(host="0.0.0.0", port="5000")