# Распишите пример(ы) unit тестов на эту фнкцию:

# async def logs(cont, name):
#     conn = aiohttp.UnixConnector(path="/var/run/docker.sock")
#     async with aiohttp.ClientSession(connector=conn) as session:
#         async with session.get(f"http://xx/containers/{cont}/logs?follow=1&stdout=1") as resp:
#             async for line in resp.content:
#                 print(name, line)


import aiohttp
import pytest


async def test_logs():
    cont = "container_id"
    name = "container_name"

    # Создаем фейковый ответ от сервера
    class FakeResponse:
        def __init__(self):
            self.content = [b"Log line 1\n", b"Log line 2\n", b"Log line 3\n"]

    # Создаем фейковую сессию и заменяем метод get на возвращение фейкового ответа
    class FakeSession:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass

        async def get(self, url):
            return FakeResponse()

    # Заменяем оригинальный ClientSession на фейковую сессию
    aiohttp.ClientSession = FakeSession

    # Запускаем функцию logs и собираем все логи в список
    logs = []
    await logs(cont, name, logs.append)

    # Проверяем, что все логи были получены и записаны в список
    assert logs == ["Log line 1\n", "Log line 2\n", "Log line 3\n"]

# Запускаем тест
pytest.main()
