import os
from alembic import command
from alembic.config import Config

from database import DATABASE_URL


def run():
    script_dir = os.path.dirname(__file__)
    cfg = Config()
    cfg.set_main_option('script_location', os.path.join(script_dir, 'alembic'))
    cfg.set_main_option('sqlalchemy.url', DATABASE_URL)
    command.upgrade(cfg, 'head')


if __name__ == '__main__':
    run()
