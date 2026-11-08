# Консольний інтерфейс (меню)
from datetime import date

from business_logic import weather_service
from data_access.database import get_session


def print_weather(w):
    print("-" * 50)
    print(f"{w.location_name}, {w.country}   {w.last_updated:%Y-%m-%d %H:%M}")
    print(f"  Стан:            {w.condition_text}")
    print(f"  Температура:     {w.temperature_celsius} °C")
    print(f"  Схід сонця:      {w.sunrise.strftime('%H:%M') if w.sunrise else '-'}")
    if w.wind:
        direction = w.wind.wind_direction.value if w.wind.wind_direction else "-"
        print(f"  Вітер:           {w.wind.wind_kph} км/год ({w.wind.wind_mph} миль/год)")
        print(f"  Пориви:          {w.wind.gust_kph} км/год ({w.wind.gust_mph} миль/год)")
        print(f"  Напрямок:        {direction} ({w.wind.wind_degree}°)")
        print(f"  Чи варто виходити на вулицю? {'ТАК' if w.wind.should_go_outside else 'НІ'}")


def show_weather(session):
    country = input("Країна: ").strip()
    try:
        day = date.fromisoformat(input("Дата (РРРР-ММ-ДД): ").strip())
    except ValueError:
        print("Неправильний формат дати")
        return
    location = input("Місто (Enter - усі міста): ").strip() or None

    records = weather_service.find_weather(session, country, day, location)
    if not records:
        print("Даних не знайдено")
        return
    for w in records:
        print_weather(w)
    print(f"\nЗнайдено записів: {len(records)}")


def run_menu(db_name):
    session = get_session(db_name)
    while True:
        print(f"\n=== Погодна база ({db_name}) ===")
        print("1 - Завантажити дані з CSV")
        print("2 - Показати погоду за країною та датою")
        print("0 - Вихід")
        choice = input("Ваш вибір: ").strip()

        if choice == "1":
            existing = weather_service.count_records(session)
            if existing > 0:
                answer = input(f"У базі вже є {existing} записів. Завантажити ще раз? (так/ні): ")
                if answer.strip().lower() != "так":
                    continue
            path = input("Шлях до CSV [datasets/GlobalWeatherRepository.csv]: ").strip()
            count = weather_service.import_csv(session, path or "datasets/GlobalWeatherRepository.csv")
            print(f"Додано записів: {count}")
        elif choice == "2":
            show_weather(session)
        elif choice == "0":
            break
        else:
            print("Невідома команда")
    session.close()
