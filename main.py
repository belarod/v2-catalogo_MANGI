from app.app import App
from database.db import DB
from utils.utils import Utils

if __name__ == '__main__':
    Utils.clear_screen()

    my_db = DB('example.db')

    app = App(my_db)
    app.start_app()