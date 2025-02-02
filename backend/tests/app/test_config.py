from unittest import TestCase
import os

from config import ConfigFromEnvVars

class TestConfigFromEnvVars(TestCase):
    def test_config_from_env_vars_inits_correct_attributes_when_all_env_vars_set(self):
        os.environ['SECRET_KEY_ONE'] = 'somekey'
        os.environ['SECRET_KEY_TWO'] = 'somekey'

        config = ConfigFromEnvVars(env_vars=['SECRET_KEY_ONE','SECRET_KEY_TWO'])
        self.assertEqual(config.SECRET_KEY_ONE,"somekey")
        self.assertEqual(config.SECRET_KEY_TWO,"somekey")


        # discard after test
        _ = os.environ.pop('SECRET_KEY_ONE')
        _ = os.environ.pop('SECRET_KEY_TWO')


    def test_config_from_env_vars_raises_error_when_env_vars_not_set(self):
        self.assertRaises(Exception, ConfigFromEnvVars,['SOME_KEY_NOT_SET'])