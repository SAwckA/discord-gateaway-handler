import asyncio
import json
import os
import websockets


token = os.environ.get('token')


async def send_json_req(ws, req):
    """Функция отправки запроса"""
    await ws.send(json.dumps(req))


async def recieve_json_resp(ws):
    """Функция обработки ответа"""
    r = await ws.recv()
    return r


async def keep_alive(ws, interval):
    """Цикл поддержания соединения"""
    while True:
        # print('Keep Alive') #Логирование - Поддержания соединения
        await asyncio.sleep(interval)
        await send_json_req(ws, {'op': 1, 'd': 'null'})


async def GateWay():
    url = 'wss://gateway.discord.gg/?v=6&encoding=json'
    async with websockets.connect(url) as ws:

        interval = json.loads(await recieve_json_resp(ws))['d']['heartbeat_interval'] / 1000
        loop.create_task(keep_alive(ws, interval))


        #Запрос на авторизацию op = 2
        authorization = {
            'op': 2,
            'd': {
                'token': token,
                'properties': {
                    '$os': 'windows',
                    '$browser': 'chrome',
                    '$device': 'pc'
                }}}

        await send_json_req(ws, authorization)

        # print('started') #Логирование - начало работы
        while True:
            '''Цикл обработки событий'''
            try:
                resp = json.loads(await recieve_json_resp(ws))
                if resp['op'] == 11:
                    pass
                elif resp['t'] == 'MESSAGE_CREATE':
                    print(f'{resp["d"]["author"]["username"]} > {resp["d"]["content"]} ')

            except Exception as e:
                print(e)


loop = asyncio.get_event_loop()
loop.run_until_complete(GateWay())
