from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField, FileRequired
from wtforms import StringField, URLField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, URL, Regexp

from .constants import (
    URL_MIN_LEN,
    URL_MAX_LEN,
    SHORT_MAX_LEN,
    SHORT_ID_REGEX,
)


class URLForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[
            Length(
                URL_MIN_LEN,
                URL_MAX_LEN,
                message='Длина поля не должна быть меньше'
                f'{URL_MIN_LEN} и больше {URL_MAX_LEN} символов.',
            ),
            DataRequired('Обязательное поле'),
            URL(require_tld=True, message='Введите корректный URL'),
        ],
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Length(max=SHORT_MAX_LEN),
            Optional(),
            Regexp(SHORT_ID_REGEX, message='Только латинские буквы и цифры'),
        ],
    )
    submit = SubmitField('Создать')


class FileForm(FlaskForm):
    files = MultipleFileField('Файлы', validators=[FileRequired()])
    submit = SubmitField('Загрузить')
