import asyncio
import urllib

import aiohttp

from . import app

AUTH_HEADERS = {'Authorization': f'OAuth {app.config["DISK_TOKEN"]}'}

API_HOST = 'https://cloud-api.yandex.net/'
API_VERSION = 'v1'

DISK_INFO_URL = f'{API_HOST}{API_VERSION}/disk/'
REQUEST_UPLOAD_URL = f'{API_HOST}{API_VERSION}/disk/resources/upload'
DOWNLOAD_LINK_URL = f'{API_HOST}{API_VERSION}/disk/resources/download'


async def get_upload_url(filename: str):
    async with aiohttp.ClientSession(headers=AUTH_HEADERS) as session:
        async with session.get(
            url=REQUEST_UPLOAD_URL,
            params={
                'path': f'app:/{filename}',
                'overwrite': 'True',
                'fields': 'href',
            },
        ) as response:
            data = await response.json()
            upload_url = data.get('href')
            return upload_url


async def get_download_url(location):
    async with aiohttp.ClientSession(headers=AUTH_HEADERS) as session:
        async with session.get(
            url=DOWNLOAD_LINK_URL,
            params={
                'path': location,
                'fields': 'href',
            },
        ) as response:
            data = await response.json()
            return data.get('href')


async def upload_file(session, file, upload_url):
    async with session.put(
        url=upload_url,
        data=file.read(),
    ) as response:
        if response.status != 201:
            error_text = await response.text()
            raise ValueError(
                f'Ошибка загрузки файла. Статус: {response.status}, '
                f'Ответ: {error_text}'
            )

        location = response.headers.get('location')
        location = urllib.parse.unquote(location)
        location = location.replace('/disk', '')
        download_url = await get_download_url(location)
        return file.filename, download_url


async def upload_files_and_get_urls(files):
    tasks = []
    filenames_urls = []
    async with aiohttp.ClientSession() as session:
        for file in files:
            upload_url = await get_upload_url(file.filename)
            tasks.append(
                asyncio.ensure_future(upload_file(session, file, upload_url))
            )
        filenames_urls.extend(await asyncio.gather(*tasks))
    return filenames_urls
