import numpy as np
import os
from joblib import load


class MushroomPredictor(object):
  def __init__(self, model):
    self._model = model

  def predict(self, instances, **kwargs):
    inputs = np.asarray(instances)
    if kwargs.get('probabilities'):
      return self._model.predict_proba(inputs)
    else:
      return self._model.predict(inputs)

  @classmethod
  def from_path(cls, model_dir):
     model_path = os.path.join(model_dir, 'model.pkl')
     model = load(model_path)

     return cls(model)
