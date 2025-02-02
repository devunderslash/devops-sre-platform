import os
from dotenv import load_dotenv

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
