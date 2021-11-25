import os
import asyncio
import yaml

from datetime import datetime, timezone, timedelta
from aiofiles import open as async_open
from aiofiles.os import stat as async_stat
from types import SimpleNamespace


class YamlConfigManager:
    def __init__(self, interval):
        self._update_interval = interval
        self._config_file = 'config.yaml'

    async def _update_loop(self, config):
        while True:
            try:
                await self._update(config)
            except Exception as e:
                print(f'Failed to update config!\n{repr(e)}')
            await asyncio.sleep(self._update_interval)

    async def _init(self, config):
        async with async_open(self._config_file, 'r') as f:
            data = yaml.safe_load(await f.read())

            config.VERSION = data['version']

            database = data['database']
            config.DB_CONNECTION_STRING = f"postgresql+asyncpg://{database['user']}:{database['password']}@{database['host']}:{database['port']}/{database['database']}"

    async def _update(self, config):
        conf_stat = await async_stat(self._config_file)
        conf_mod = datetime.fromtimestamp(conf_stat.st_mtime)

        if (datetime.now() > conf_mod + timedelta(seconds=self._update_interval)
            and not config.FIRST_RUN):
            return
        cfg.FIRST_RUN = False

        async with async_open(self._config_file, mode='r') as conf:
            data = yaml.safe_load(await conf.read())

            self._update_interval = data['update_interval']
            config.AUTH_HEADER_PREFIX = data['auth_header_prefix']
            config.AUTH_HEADERS = data['auth_headers']

    async def start(self, config):
        self._update_task = asyncio.ensure_future(self._update_loop(config))
        await self._init(config)


cfg = SimpleNamespace()
cfg.STARTUP_DB_ACTION = False
cfg.FIRST_RUN = True
