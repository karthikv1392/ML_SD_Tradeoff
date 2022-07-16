import joblib
import os
from loguru import logger
import numpy as np
import ast


class PredictionEngine:
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

    def predict(self, key, payload):
        """It performs a prediction for the given service type"""

        # GRAB CORRECT MODELS
        model_rt = self.get_model('rt', key)
        scaler_rt = self.get_scaler('rt', key)

        model_cpu = self.get_model('cpu', key)
        scaler_cpu = self.get_scaler('cpu', key)

        # PAYLOAD PRE-PROCESSING

        rt_array = np.array(ast.literal_eval(payload['calls']))
        cpu_array = np.array(ast.literal_eval(payload['statuses']))

        rt_array = rt_array.reshape(1, 10, 5)
        cpu_array = cpu_array.reshape(1, 3, 5)

        # PREDICTION

        pred_rt = model_rt.predict(rt_array)
        pred_cpu = model_cpu.predict(cpu_array)

        # INVERSE SCALING PREDICTION

        pred_rt_inv = scaler_rt.inverse_transform(pred_rt)
        pred_cpu_inv = scaler_cpu.inverse_transform(pred_cpu)

        logger.debug(f"rt predictions: {pred_rt_inv}")
        logger.debug(f"cpu predictions: {pred_cpu_inv}")

        # RETURN RESULT
        data = {'key': key,
                'pred_rt': pred_rt_inv,
                'pred_cpu': pred_cpu_inv}
        return data
