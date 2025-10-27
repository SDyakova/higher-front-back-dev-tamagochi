import os

from game.models import Food, Medicine
from game.tamagochi import SimpleTamagochi
from game.clicker import SimpleRandomClicker
from game.game import SimpleGame


def main():
    """Запускает игру и управляет игровым циклом"""
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

    print("Добро пожаловать в Тамагочи-кликер!")
    output = ""

    while True:
        print(output)

        print(f"Сумка с едой: {game.food}")
        print(f"Сумка с лекарствами: {game.medicine}")

        status = game.get_status()
        print(
            f"\nСтатус: голод {status['hunger']}, здоровье {status['hp']}, "
            f"энергия {status['energy']}, монет {status['coins']}\n"
        )
        if game.tamagochi.is_sick():
            print("=======Тамагочи болеет======")
            print("=======Отдых действует менее эффективно=======")
            print("1. Пойти на работу")
            print("2. Купить еду")
            print("3. Купить лекарство")
            print("4. Покормить")
            print("5. Вылечить")
            print("6. Играть")
            print("7. Отдых")
            print("0. Выход")

        match input("Выберите действие: "):
            case "1":
                income = game.work()
                output = f"Вы заработали {income} монет"
                game.tamagochi.update()
            case "2":
                print("Выберите еду для покупки")
                for i, f in enumerate(all_food):
                    print(f"{i}. {f.name} ({f.price} монет)")

                index = int(input("Введите номер еды: "))
                try:
                    game.buy_food(all_food[index])
                    output = f"Вы купили {all_food[index].name}"
                except Exception as e:
                    output = str(e)
            case "3":
                print("Выберите лекарство для покупки:")
                for i, m in enumerate(all_medicine):
                    print(f"{i}. {m.name} ({m.price} монет)")

                index = int(input("Введите номер лекарства: "))
                try:
                    game.buy_medicine(all_medicine[index])
                    output = f"Вы купили {all_medicine[index].name}"
                except Exception as e:
                    output = str(e)
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
