import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

import logging 

logging.basicConfig(level=logging.INFO,format='[%(asctime)s] [%(levelname)s] %(message)s',datefmt="%Y-%m-%d %H:%M:%S %z")

logger = logging.getLogger(__name__)

load_dotenv()


class ConfigFromEnvVars:
    def __init__(self, env_vars:list):
        for env_var in env_vars:
            try:
                setattr(self, env_var, os.environ[env_var])
            except Exception as err:
                raise Exception(f'cannot init configuration from env vars. error={err}')
            

# class DatabaseConfig:

#     def __init__(self, app):
#         self.db = SQLAlchemy(app)
#         self.engine = self.create_db_url_from_env_or_local()

#     def create_db_url_from_env_or_local(self):

#         engine =  self.db.create_engine(os.getenv('DATABASE_URL'))
#         return engine

