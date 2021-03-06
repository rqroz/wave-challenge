"""
App Initializer.
"""
from dotenv import load_dotenv

from app.config import Config
from app.setup import create_app

load_dotenv('.env')
server = create_app()
if __name__ == '__main__':
    server.run('0.0.0.0', debug=Config.DEBUG)
