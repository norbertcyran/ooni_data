from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

root = Path(__file__).parent.parent

db = create_engine(f'sqlite:///{root}/ooni.db')
Session = sessionmaker(bind=db)
