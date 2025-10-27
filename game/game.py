"""Модуль с интерфейсом и реализацией класса игры"""

from abc import ABC, abstractmethod
from typing import Any, List, Optional

from .tamagochi import AbstractTamagochi
from .clicker import AbstractClicker
from .models import Food, Medicine
from .exceptions import NotEnoughMoney


class AbstractGame(ABC):
    """Интерфейс для логики игры"""

    @abstractmethod
    def __init__(
        self,
        tamagochi: AbstractTamagochi,
        clicker: AbstractClicker,
        all_food: list[Food],
        all_medicine: list[Medicine]
    ):
        """
        Абстрактный метод инициализации класса игры

        :param tamagochi: экземпляр тамагочи
        :param clicker: экземпляр кликера
        :param all_food: все доступные варианты еды
        :param all_medicine: все доступные варианты лекарств
        """
        raise NotImplementedError

    @abstractmethod
    def work(self) -> int:
        """
        Абстрактный метод для логики действия "работа

        :return: количество заработанных монет
        """
        raise NotImplementedError

    @abstractmethod
    def buy_food(self, food: Food) -> None:
        """Абстрактный метод для покупки еды"""
        raise NotImplementedError

    @abstractmethod
    def buy_medicine(self, medicine: Medicine) -> None:
        """Абстрактный метод для покупки лекарства"""
        raise NotImplementedError

    @abstractmethod
    def feed_tamagochi(self, index: int = 0) -> None:
        """Абстрактный метод для кормления тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def heal_tamagochi(self, index: int = 0) -> None:
        """Абстрактный метод для лечения тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def rest_tamagochi(self):
        """Абстрактный метод для отдыха тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def play_with_tamagochi(self):
        """Абстрактный метод для игры с тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def get_status(self) -> dict[str, Any]:
        """
        Абстрактный метод для получения статуса (всех характеристик) тамагочи

        :return: словарь со всеми характеристиками тамагочи
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def food(self) -> list[Food]:
        """
        Абстрактное свойство для доступа к сумке с едой

        :return: список с имеющимися (купленными) объектами еды
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def medicine(self) -> list[Medicine]:
        """
        Абстрактное свойство для доступа к сумке с лекарствами

        :return: список с имеющимися (купленными) объектами лекарств
        """
        raise NotImplementedError


class SimpleGame(AbstractGame):
    """Реализация логики игры"""

    def __init__(
        self,
        tamagochi: AbstractTamagochi,
        clicker: AbstractClicker,
        all_food: List[Food],
        all_medicine: List[Medicine],
    ) -> None:
        self.tamagochi = tamagochi
        self.clicker = clicker
        self._all_food = all_food
        self._all_medicine = all_medicine
        self._food_bag: List[Food] = []
        self._medicine_bag: List[Medicine] = []
        self._coins: int = 0

    @property
    def food(self) -> List[Food]:
        """Возвращает сумку с купленной едой"""
        return self._food_bag

    @property
    def medicine(self) -> List[Medicine]:
        """Возвращает сумку с купленными лекарствами"""
        return self._medicine_bag

    def work(self) -> int:
        """Заработок монет через кликер"""
        earned = self.clicker.click()
        if earned is None:
            earned = getattr(self.clicker, "income_per_click", 0)
        self._coins += earned
        self.tamagochi.update()
        return self._coins

    def buy_food(self, food: Optional[Food] = None) -> None:
        """Покупка еды, если хватает монет"""
        if food is None:
            food = self._all_food[0]
        if self._coins < food.price:
            raise NotEnoughMoney("Недостаточно монет для покупки еды")
        self._food_bag.append(food)
        self._coins -= food.price

    def buy_medicine(self, medicine: Optional[Medicine] = None) -> None:
        """Покупка лекарства, если хватает монет"""
        if medicine is None:
            medicine = self._all_medicine[0]
        if self._coins < medicine.price:
            raise NotEnoughMoney("Недостаточно монет для покупки лекарства")
        self._medicine_bag.append(medicine)
        self._coins -= medicine.price

    def feed_tamagochi(self, index: int = 0) -> None:
        """Кормление питомца едой из сумки"""
        if not self._food_bag:
            return
        food_item = self._food_bag.pop(index)
        self.tamagochi.feed(food_item)
        self.tamagochi.update()

    def heal_tamagochi(self, index: int = 0) -> None:
        """Лечение питомца лекарством из сумки"""
        if not self._medicine_bag:
            return
        medicine_item = self._medicine_bag.pop(index)
        self.tamagochi.heal(medicine_item)
        self.tamagochi.update()

    def rest_tamagochi(self) -> None:
        """Отдых питомца"""
        self.tamagochi.rest()
        self.tamagochi.update()

    def play_with_tamagochi(self) -> None:
        """Игровое взаимодействие с питомцем"""
        self.tamagochi.play()
        self.tamagochi.update()

    def get_status(self) -> dict[str, Any]:
        """Возвращает текущее состояние питомца и монет"""
        current_state = self.tamagochi.status.copy()
        current_state["coins"] = self._coins
        return current_state
