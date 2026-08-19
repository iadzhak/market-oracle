from pathlib import Path

import numpy as np
from joblib import dump, load
from sklearn.linear_model import SGDClassifier
from sklearn.preprocessing import StandardScaler

from .settings import conf

# Путь относительно расположения этого модуля
_BASE_DIR = Path(__file__).resolve().parent.parent / "weights"


class Oracle:
    GLOBAL_SCALER_PATH = _BASE_DIR / "global_scaler.joblib"

    def __init__(self, token: str = conf.DEFAULT_MODEL_NAME) -> None:
        self.model = SGDClassifier(loss='log_loss', random_state=42)
        self.path = self._get_path(token)
        self.scaler: StandardScaler | None = None
        self.load_model()

    @staticmethod
    def _get_path(token: str):
        return _BASE_DIR / f'{token.lower()}.joblib'

    def train(self, x: list[list[float]], y: list[int]):
        if self.scaler is None:
            self._create_scaler(x)
        x_train = self.scaler.transform(np.array(x))
        y_train = np.array(y)
        self.model.partial_fit(x_train, y_train, classes=[0, 1])
        self.save_model()

    def _create_scaler(self, x: list[list[float]]):
        self.scaler = StandardScaler()
        self.scaler.fit(x)
        self.GLOBAL_SCALER_PATH.parent.mkdir(parents=True, exist_ok=True)
        dump(self.scaler, self.GLOBAL_SCALER_PATH)

    def save_model(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        dump(self.model, self.path)

    def load_model(self):
        # Загружаем scaler первым — он общий для всех моделей
        if self.GLOBAL_SCALER_PATH.exists():
            self.scaler = load(self.GLOBAL_SCALER_PATH)

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
        if self.scaler is None:
            raise RuntimeError('Scaler не создан')

        x_arr = self.scaler.transform(np.array(x))
        pred = self.model.predict(x_arr)[0]
        proba = self.model.predict_proba(x_arr)[0, pred]
        return int(pred), float(proba)

    def contributions(self, x: list[list[float]]):
        coef = self.model.coef_[0]
        x_scaled = self.scaler.transform(x)
        return x_scaled[0] * coef
