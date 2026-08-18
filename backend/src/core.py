import numpy as np
from joblib import dump, load
from sklearn.linear_model import SGDClassifier
from pathlib import Path
from .settings import conf

class Oracle:

    def __init__(self, token: str = conf.DEFAULT_MODEL_NAME) -> None:
        self.model = SGDClassifier(loss='log_loss', random_state=42)
        self.path = self._get_path(token)
        self.load_model()

    @staticmethod
    def _get_path(token: str):
        return Path(f'./weights/{token.lower()}.joblib').resolve()

    def train(self, x: list[list[float]], y: list[int]):
        x_train = np.array(x)
        y_train = np.array(y)
        self.model.partial_fit(x_train, y_train, classes=[0, 1])
        self.save_model()

    def save_model(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        dump(self.model, self.path)

    def load_model(self):
        default_path = self._get_path(conf.DEFAULT_MODEL_NAME)
        model_path = self.path
        if model_path.exists():
            self.model = load(model_path)
            return
        if default_path.exists():
            self.model = load(default_path)
            return

    def predict(self, x: list[list[float]]) -> tuple[int, float]:
        """
        Возвращает:
          - предсказанный класс (0 или 1)
          - уверенность (вероятность предсказания)
        """
        x_arr = np.array(x)
        pred = self.model.predict(x_arr)[0]
        proba = self.model.predict_proba(x_arr)[0, pred]
        return int(pred), float(proba)
