import joblib
import os
from loguru import logger


class EngineProvider:
    def __init__(self):
        # TODO: check files and load models
        self.keys = ['catalogue', 'carts', 'shipping', 'user', 'orders', 'payment']
        self.params = ['rt', 'cpu']
        self.models = {}
        self.scalers = {}

        self.load_files()

    def load_files(self):
        """Tensor flow models and scalers have been stored in the 'models' directory with joblib. This function loads them to
           restore the original python objects"""
        for param in self.params:
            self.models[param] = {}
            self.scalers[param] = {}

            models_folder_name = f'models/{param}'
            scalers_folder_name = f'scalers/{param}'

            for key in self.keys:
                model_name = f'{key}.model.sav'
                scaler_name = f'{key}.scaler.sav'

                model_filepath = f'{models_folder_name}/{model_name}'
                scaler_filepath = f'{scalers_folder_name}/{scaler_name}'

                logger.debug(f'Loading {model_filepath}')
                file_exists = os.path.exists(model_filepath)

                if not file_exists:
                    logger.error(f'Could not load {model_filepath}')
                    raise FileNotFoundError

                logger.debug(f'Loading {scaler_filepath}')
                file_exists = os.path.exists(scaler_filepath)

                if not file_exists:
                    logger.error(f'Could not load {scaler_filepath}')
                    raise FileNotFoundError

                self.models[param][key] = joblib.load(model_filepath)
                self.scalers[param][key] = joblib.load(scaler_filepath)

            logger.debug(self.models[param])

    def get_model(self, param, key):
        return self.models[param][key]

    def get_scaler(self, param, key):
        return self.scalers[param][key]

    def predict(self, param, key, payload):
        """It performs a prediction for the given service type"""
        model = self.get_model(param, key)
        scaler = self.get_scaler(param, key)

        # TODO: PAYLOAD PRE-PROCESSING

        # TODO: PREDICTION

        # TODO: INVERSE SCALING PREDICTION

        # TODO: RETURN RESULT
