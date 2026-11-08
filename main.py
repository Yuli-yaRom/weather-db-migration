# Запуск:  python main.py          (працює з Postgres)
#          python main.py mysql    (працює з MySQL)
import sys

from presentation.console import run_menu

if __name__ == "__main__":
    db_name = sys.argv[1] if len(sys.argv) > 1 else "postgres"
    run_menu(db_name)
