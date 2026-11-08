# Робота з базою даних: збереження і пошук записів


def save_all(session, objects):
    session.add_all(objects)
    session.commit()
