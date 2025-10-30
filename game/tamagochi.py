"""Модуль с интерфейсом и реализациями класса."""

# Стандартная библиотека
from abc import ABC, abstractmethod

# Локальные модули проекта
from game.models import Food, Medicine
from game.constants import (
    MIN_STATE_VALUE,
    MAX_STATE_VALUE,
    INITIAL_HUNGER,
    INITIAL_HP,
    INITIAL_ENERGY,
    ENERGY_LOSS_PLAY,
    HUNGER_GAIN_PLAY,
    ENERGY_GAIN_REST,
    HUNGER_GAIN_REST,
    HUNGER_DAMAGE_THRESHOLD,
    HP_LOSS_HUNGER,
    HUNGER_INCREASE_PER_UPDATE,
    ENERGY_LOSS_PER_UPDATE
)


class AbstractTamagochi(ABC):
    """Интерфейс логики тамагочи."""

    @abstractmethod
    def feed(self, food: Food) -> None:
        """
        Абстрактный метод для кормления тамагочи.

        :param food: объект еды для кормления
        """
        raise NotImplementedError

    @abstractmethod
    def play(self) -> None:
        """Абстрактный метод для игры с тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def rest(self) -> None:
        """Абстрактный метод для отдыха тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def heal(self, medicine: Medicine) -> None:
        """
        Абстрактный метод для лечения тамагочи.

        :param medicine: лекарство для лечения
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def status(self) -> dict[str, int]:
        """
        Абстрактное свойство для доступа ко всем состояниям тамагочи.

        :return: словарь со всеми состояниями тамагочи
        """
        raise NotImplementedError

    @abstractmethod
    def is_alive(self) -> bool:
        """
        Абстрактный метод для проверки жив ли тамагочи.

        :return: True если жив, иначе False
        """
        raise NotImplementedError

    @abstractmethod
    def is_sick(self) -> bool:
        """
        Абстрактный метод для проверки, не заболел ли тамагочи.

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
    """Реализация логики питомца."""

    def __init__(self) -> None:
        self._state: dict[str, int] = {
            "hunger": INITIAL_HUNGER,
            "hp": INITIAL_HP,
            "energy": INITIAL_ENERGY,
        }

    def _limit_state(self, key: str) -> None:
        """Ограничивает значение показателя в диапазоне."""
        if self._state[key] < MIN_STATE_VALUE:
            self._state[key] = MIN_STATE_VALUE
        elif self._state[key] > MAX_STATE_VALUE:
            self._state[key] = MAX_STATE_VALUE

    def feed(self, food: Food) -> None:
        """Кормление питомца"""
        self._state["hunger"] -= food.satiety
        self._limit_state("hunger")
        self._limit_state("energy")

    def play(self) -> None:
        """Питомец играет — тратит энергию и становится голоднее."""
        self._state["energy"] -= ENERGY_LOSS_PLAY
        self._state["hunger"] += HUNGER_GAIN_PLAY
        self._limit_state("energy")
        self._limit_state("hunger")

    def rest(self) -> None:
        """Питомец отдыхает — восстанавливает энергию, немного голодает."""
        self._state["energy"] += ENERGY_GAIN_REST
        self._state["hunger"] += HUNGER_GAIN_REST
        self._limit_state("energy")
        self._limit_state("hunger")

    def heal(self, medicine: Medicine) -> None:
        """Лечим питомца, восстанавливая здоровье."""
        if medicine.is_empty():
            return
        medicine.uses += 1
        self._state["hp"] += medicine.heal_hp
        self._limit_state("hp")

    @property
    def status(self):
        """Возвращаем текущие показатели питомца."""
        return self._state.copy()

    def is_alive(self) -> bool:
        """Проверяем, жив ли питомец."""
        return self._state['hp'] > 0

    def is_sick(self) -> bool:
        """Проверяем, болен ли питомец."""
        return self._state['hp'] < 50

    def update(self) -> None:
        """Обновляем состояние питомца после каждого действия."""
        self._state["hunger"] += HUNGER_INCREASE_PER_UPDATE
        self._state["energy"] -= ENERGY_LOSS_PER_UPDATE

        if self._state["hunger"] > HUNGER_DAMAGE_THRESHOLD:
            self._state["hp"] -= HP_LOSS_HUNGER

        self._limit_state("hunger")
        self._limit_state("energy")
        self._limit_state("hp")
