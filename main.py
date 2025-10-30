# Стандартная библиотека
import os

# Локальные модули проекта
from game.clicker import SimpleRandomClicker
from game.game import SimpleGame
from game.models import Food, Medicine
from game.tamagochi import SimpleTamagochi


def main():
    """Запускает игру и управляет игровым циклом."""
    all_food = [
        Food(name="Бургер", satiety=20, price=40),
        Food(name="Салат", satiety=10, price=20),
        Food(name="Яблоко", satiety=10, price=15),
    ]

    all_medicine = [
        Medicine(name="Ибупрофен", price=30, heal_hp=20, number_of_uses=2)
    ]

    tamagochi = SimpleTamagochi()
    clicker = SimpleRandomClicker(10, 20)
    game = SimpleGame(
        tamagochi,
        clicker,
        all_food=all_food,
        all_medicine=all_medicine
    )

    def choose_item_and_buy(items, buy_method, item_type):
        """Выбор и покупка еды или лекарства."""
        menu_lines = [
            f"{i}. {item.name} ({item.price} монет)"
            for i, item in enumerate(items)]
        print(f"Выберите {item_type} для покупки:\n" + "\n".join(menu_lines))

        index = int(input("Введите номер: "))
        try:
            buy_method(items[index])
            return f"Вы купили {items[index].name}"
        except Exception as e:
            return str(e)

    print("Добро пожаловать в Тамагочи-кликер!")
    output = ""

    while True:
        status = game.get_status()
        food_str = ", ".join(f.name for f in game.food)
        medicine_str = ", ".join(m.name for m in game.medicine)

        output_lines = [
            output,
            f"Сумка с едой: {food_str}",
            f"Сумка с лекарствами: {medicine_str}",
            f"Статус: голод {status['hunger']}, "
            f"здоровье {status['hp']}, "
            f"энергия {status['energy']}, "
            f"монет {status['coins']}"
        ]

        if game.tamagochi.is_sick():
            MENU = "\n".join([
                "=======Тамагочи болеет======",
                "=======Отдых действует менее эффективно=======",
                "1. Пойти на работу",
                "2. Купить еду",
                "3. Купить лекарство",
                "4. Покормить",
                "5. Вылечить",
                "6. Играть",
                "7. Отдых",
                "0. Выход"
            ])
            output_lines.append(MENU)

        print("\n".join(output_lines))

        match input("Выберите действие: "):
            case "1":
                income = game.work()
                output = f"Вы заработали {income} монет"
                game.tamagochi.update()
            case "2":
                output = choose_item_and_buy(all_food, game.buy_food, "еду")
            case "3":
                output = choose_item_and_buy(
                    all_medicine, game.buy_medicine, "лекарство")
            case "4":
                if game.food:
                    game.feed_tamagochi(0)
                    output = "Питомец покормлен"
                else:
                    output = "Еды нет в сумке"
            case "5":
                if game.medicine:
                    game.heal_tamagochi(0)
                    output = "Питомец вылечен"
                else:
                    output = "Лекарства нет в сумке"
            case "6":
                game.play_with_tamagochi()
                output = "Вы поиграли с питомцем"
            case "7":
                game.rest_tamagochi()
                output = "Питомец отдохнул"
            case "0":
                break
            case _:
                output = "Неверная команда"

        os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == "__main__":
    main()
