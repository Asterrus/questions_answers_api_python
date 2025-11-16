from dotenv import load_dotenv

from app.app_factory import create_production_app
from app.config.logging import setup_logging

load_dotenv()
setup_logging()


app = create_production_app()
