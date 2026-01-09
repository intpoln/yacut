from flask import flash, render_template, redirect

from . import app
from .forms import URLForm, FileForm
from .constants import FILES_PREFIX
from .models import URLMap
from .yandex_disk import upload_files_and_get_urls


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """Обработка главной страницы и создание которких ссылок.

    При GET запросе отображает форму для создания короткой ссылки.
    При POST запросе обрабатывает форму, создает короткую ссылку
    и отображает результат пользователю.
    """

    form = URLForm()

    if not form.validate_on_submit():
        return render_template('create_url.html', form=form)

    original = form.original_link.data
    short = form.custom_id.data

    try:
        url_map = URLMap.validate_short_and_save_object(
            original=original, short=short
        )
    except ValueError as error:
        flash(str(error))
        return render_template('create_url.html', form=form)

    short_link = url_map.to_dict()['short_link']
    flash(f'Ваша новая ссылка готова: <a href="{short_link}">{short_link}</a>')

    return render_template('create_url.html', form=form)


@app.route(f'/{FILES_PREFIX}', methods=['GET', 'POST'])
async def files_view():
    """Обработка страницы загрузки файлов и создания коротких ссылок.

    При GET запросе отображает форму для загрузки файлов.
    При POST запросе загружает файлы на Yandex Disk, создает короткие
    ссылки для каждого файла и отображает результаты.
    """

    form = FileForm()

    if not form.validate_on_submit():
        return render_template('upload_file.html', form=form)

    filenames_urls = await upload_files_and_get_urls(form.files.data)
    filenames_shorts = {}
    for filename, original in filenames_urls:
        try:
            url_map = URLMap.validate_short_and_save_object(original=original)
            filenames_shorts[filename] = url_map.to_dict()['short_link']
        except ValueError as error:
            flash(str(error))
            return render_template('upload_file.html', form=form)
    return render_template(
        'upload_file.html', form=form, files=filenames_shorts
    )


@app.route('/<string:short_id>')
def redirect_view(short_id):
    """Перенаправление на оригинальный URL по короткому идентификатору.

    Args:
        short_id: Короткий идентификатор ссылки.

    Returns:
        Редирект на оригинальный URL или 404 если ссылка не найдена.
    """

    original = URLMap.query.filter_by(short=short_id).first_or_404().original
    return redirect(original)
