"""Модуль с интерфейсом и реализацией кликера."""

# Стандартная библиотека
import random
from abc import ABC, abstractmethod


class AbstractClicker(ABC):
    """Интерфейс для кликера."""

    @abstractmethod
    def __init__(self) -> None:
        """Абстрактный метод инициализации."""
        raise NotImplementedError

    @abstractmethod
    def click(self) -> None:
        """Абстрактный метод клика для накапливания монет."""
        raise NotImplementedError

    @property
    @abstractmethod
    def income_per_click(self) -> int:
        """Абстрактное свойство для доступа к количеству монет за клик."""
        raise NotImplementedError


class SimpleRandomClicker(AbstractClicker):
    """Кликер со случайным доходом."""

    def __init__(self, min_income: int, max_income: int) -> None:
        self._min_income = min_income
        self._max_income = max_income
        self._last_income = 0

    def click(self) -> int:
        """Логика клика: генерируем случайный доход и возвращаем его."""
        self._last_income = random.randint(self._min_income, self._max_income)
        return self._last_income

    @property
    def income_per_click(self) -> int:
        """Возвращает количество монет последнего клика."""
        return self._last_income
