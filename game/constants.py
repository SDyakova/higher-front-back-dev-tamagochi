"""Константы приложения Тамагочи"""

# Границы характеристик питомца
MIN_STATE_VALUE = 0
MAX_STATE_VALUE = 100

# Начальные показатели питомца
INITIAL_HUNGER = 50
INITIAL_HP = 100
INITIAL_ENERGY = 50

# Энергия/голод при взаимодействиях
ENERGY_LOSS_PLAY = 10          # энергия теряется при игре
HUNGER_GAIN_PLAY = 5           # голод увеличивается при игре
ENERGY_GAIN_REST = 20          # энергия восстанавливается при отдыхе
HUNGER_GAIN_REST = 5           # голод увеличивается при отдыхе

# Пороговые значения для урона и болезни
HUNGER_DAMAGE_THRESHOLD = 60   # если голод выше, теряется HP
HP_LOSS_HUNGER = 10             # количество HP, теряемое при сильном голоде

# Прирост голода и потеря энергии за один update
HUNGER_INCREASE_PER_UPDATE = 1
ENERGY_LOSS_PER_UPDATE = 1
