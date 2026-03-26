from django.apps import AppConfig

"""
Конфигурация Django приложения `content`.

`default_auto_field` задает тип PK по умолчанию для новых моделей.
"""


class ContentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'content'
