# Консольний інтерфейс (меню)
from business_logic import weather_service
from data_access.database import get_session


def run_menu(db_name):
    session = get_session(db_name)
    while True:
        print(f"\n=== Погодна база ({db_name}) ===")
        print("1 - Завантажити дані з CSV")
        print("0 - Вихід")
        choice = input("Ваш вибір: ").strip()

        if choice == "1":
            path = input("Шлях до CSV [datasets/GlobalWeatherRepository.csv]: ").strip()
            count = weather_service.import_csv(session, path or "datasets/GlobalWeatherRepository.csv")
            print(f"Додано записів: {count}")
        elif choice == "0":
            break
        else:
            print("Невідома команда")
    session.close()
