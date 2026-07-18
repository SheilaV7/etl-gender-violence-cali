from sqlalchemy import create_engine
from config.settings import DB_URL

engine = create_engine(DB_URL)
