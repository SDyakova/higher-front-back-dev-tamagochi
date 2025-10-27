"""Модуль с интерфейсом и реализациями класса тамагочи"""

from abc import ABC, abstractmethod
from .models import Food, Medicine


class AbstractTamagochi(ABC):
    """Интерфейс логики тамагочи"""

    @abstractmethod
    def feed(self, food: Food) -> None:
        """
        Абстрактный метод для кормления тамагочи

        :param food: объект еды для кормления
        """
        raise NotImplementedError

    @abstractmethod
    def play(self) -> None:
        """Абстрактный метод для игры с тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def rest(self) -> None:
        """Абстрактный метод для отдыха тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def heal(self, medicine: Medicine) -> None:
        """
        Абстрактный метод для лечения тамагочи

        :param medicine: лекарство для лечения
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def status(self) -> dict[str, int]:
        """
        Абстрактное свойство для доступа ко всем состояниям тамагочи

        :return: словарь со всеми состояниями тамагочи
        """
        raise NotImplementedError

    @abstractmethod
    def is_alive(self) -> bool:
        """
        Абстрактный метод для проверки жив ли тамагочи

        :return: True если жив, иначе False
        """
        raise NotImplementedError

    @abstractmethod
    def is_sick(self) -> bool:
        """
        Абстрактный метод для проверки, не заболел ли тамагочи

        :return: True если тамагочи болеет, иначе False
        """
        raise NotImplementedError

    @abstractmethod
    def update(self) -> None:
        """
        Абстрактный метод для обновления состояний тамагочи.
        Должен использоваться после каждого взаимодействия с тамагочи
        """
        raise NotImplementedError


class SimpleTamagochi(AbstractTamagochi):
    """Реализация логики питомца"""

    def __init__(self):
        self._state = {
            'hunger': 50,
            'hp': 100,
            'energy': 50
        }

    def _limit_state(self, key: str) -> None:
        """Ограничивает значение показателя в диапазоне 0–100"""
        if self._state[key] < 0:
            self._state[key] = 0
        elif self._state[key] > 100:
            self._state[key] = 100

    def feed(self, food: Food) -> None:
        """Питомец ест — голод уменьшается, тратится энергия"""
        self._state["hunger"] -= food.satiety
        self._state["energy"] -= 5
        self._limit_state("hunger")
        self._limit_state("energy")

    def play(self) -> None:
        """Питомец играет — тратит энергию и становится голоднее"""
        self._state["energy"] -= 10
        self._state["hunger"] += 5
        self._limit_state("energy")
        self._limit_state("hunger")

    def rest(self) -> None:
        """Питомец отдыхает — восстанавливает энергию, немного голодает"""
        possible_gain = 100 - self._state['energy']
        gain = min(20, possible_gain)
        self._state['energy'] += gain
        self._state['hunger'] += 5
        self._limit_state('energy')
        self._limit_state('hunger')

    def heal(self, medicine: Medicine) -> None:
        """Лечим питомца, восстанавливая здоровье"""
        if medicine.is_empty():
            return
        medicine.uses += 1
        self._state["hp"] += medicine.heal_hp
        self._limit_state("hp")

    @property
    def status(self):
        """Возвращаем текущие показатели питомца"""
        return self._state.copy()

    def is_alive(self) -> bool:
        """Проверяем, жив ли питомец"""
        return self._state['hp'] > 0

    def is_sick(self) -> bool:
        """Проверяем, болен ли питомец"""
        return self._state['hp'] < 50

    def update(self) -> None:
        """Обновляем состояние питомца после каждого действия"""
        self._state["hunger"] += 2
        self._state["energy"] -= 2
        if self._state["hunger"] > 80:
            self._state["hp"] -= 5
        self._limit_state("hunger")
        self._limit_state("energy")
        self._limit_state("hp")
