"""WSGI entry point for production deployment"""
from app import create_app

# Create the application instance
application = create_app()
app = application

if __name__ == "__main__":
    app.run()
