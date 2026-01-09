import re
import string
from datetime import datetime, timezone
from random import choices

from flask import url_for

from . import db
from .constants import (
    ID_DEFAULT_LENGTH,
    RESERVED_SHORT_ID_PREFIXES,
    SHORT_ID_REGEX,
    SHORT_MAX_LEN,
    SHORT_MIN_LEN,
    URL_MAX_LEN,
)


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(URL_MAX_LEN), nullable=False, unique=True)
    short = db.Column(db.String(SHORT_MAX_LEN), nullable=False, unique=True)
    timestamp = db.Column(
        db.DateTime, index=True, default=lambda: datetime.now(timezone.utc)
    )

    def to_dict(self):
        return {
            'url': self.original,
            'short_link': self.get_short_link(self.short),
        }

    @staticmethod
    def get_obj_by_short(short_id):
        return URLMap.query.filter_by(short=short_id).first()

    @staticmethod
    def get_short_link(short_id):
        return url_for('redirect_view', short_id=short_id, _external=True)

    @staticmethod
    def short_id_is_not_unique(short):
        return (
            URLMap.get_obj_by_short(short) is not None
            or short in RESERVED_SHORT_ID_PREFIXES
        )

    @staticmethod
    def get_unique_short_id(length=ID_DEFAULT_LENGTH) -> str:
        symbols = string.ascii_letters + string.digits

        while True:
            short_id = ''.join(choices(symbols, k=length))
            if not URLMap.short_id_is_not_unique(short_id):
                return short_id

    @staticmethod
    def short_id_is_valid(short):
        return (
            SHORT_MIN_LEN < len(short) < SHORT_MAX_LEN
            and re.match(SHORT_ID_REGEX, short)
        )

    @staticmethod
    def original_is_not_unique(original):
        return bool(URLMap.query.filter_by(original=original).first())

    @staticmethod
    def validate_short_and_save_object(original=None, short=None):
        """Валидирует и создает URLMap объект

        Args:
            original: Оригинальный URL
            short: Опциональный кастомный короткий идентификатор

        Returns:
            str: Укороченная ссылка

        Raises:
            ValueError: При некорректных данных или уже существующем custom_id

        """

        if short:
            if URLMap.short_id_is_not_unique(short):
                raise ValueError(
                    'Предложенный вариант короткой ссылки уже существует.'
                )
        else:
            short = URLMap.get_unique_short_id()

        if URLMap.original_is_not_unique(original):
            existing = URLMap.query.filter_by(original=original).first()
            short_link = existing.to_dict()['short_link']
            raise ValueError(f'Такая ссылка уже была укорочена: {short_link}')

        url_map = URLMap(original=original, short=short)
        db.session.add(url_map)
        db.session.commit()

        return url_map
