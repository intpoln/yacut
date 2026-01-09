from http import HTTPStatus

from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap


@app.route('/api/id/', methods=['POST'])
def create_short():
    """Создание короткой ссылки через API.

    Принимает JSON с полями 'url' (обязательно) и 'custom_id' (опционально).
    Возвращает созданную короткую ссылку или информацию о существующей.

    Returns:
        JSON ответ с короткой ссылкой (201).

    Raises:
        InvalidAPIUsage: При некорректных входных данных или валидации.
    """

    data = request.get_json(silent=True)
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')

    original, short = data.get('url'), data.get('custom_id')

    if short and not URLMap.short_id_is_valid(short):
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')

    try:
        url_map = URLMap.validate_short_and_save_object(
            original=original, short=short
        )
    except ValueError as error:
        raise InvalidAPIUsage(str(error))

    return jsonify(url_map.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_original_link(short_id):
    """Получение оригинального URL по короткому идентификатору через API.

    Args:
        short_id: Короткий идентификатор ссылки.

    Returns:
        JSON ответ с оригинальным URL.

    Raises:
        InvalidAPIUsage: Если ссылка с указанным идентификатором не найдена.
    """

    obj = URLMap.get_obj_by_short(short_id)

    if not obj:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)

    original = obj.original

    return jsonify({'url': original}), HTTPStatus.OK
