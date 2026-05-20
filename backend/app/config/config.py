import os


def get_env(name, default=None):
    return os.getenv(name, default)


class Config:
    SECRET_KEY = get_env('SECRET_KEY', 'change-me')
    DEBUG = get_env('DEBUG', 'False').lower() in ('true', '1', 'yes')
    SQLALCHEMY_TRACK_MODIFICATIONS = get_env('SQLALCHEMY_TRACK_MODIFICATIONS', 'False').lower() in ('true', '1', 'yes')

    DB_USER = get_env('DB_USER', 'root')
    DB_PASSWORD = get_env('DB_PASSWORD', '')
    DB_HOST = get_env('DB_HOST', '127.0.0.1')
    DB_PORT = get_env('DB_PORT', '3306')
    DB_NAME = get_env('DB_NAME', 'iluminacion_db')

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
    )
