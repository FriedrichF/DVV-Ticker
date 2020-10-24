import asyncio
import json as JSON

import websockets

matchId = ""


async def hello(websocketServer, path):
    global matchId

    while True:
        try:
            async with websockets.connect('wss://backend.sams-ticker.de/ASSOCIATION/dvv-main',
                                          origin="https://dvv.sams-ticker.de", max_size=1000000000) as websocket:

                while True:
                    try:
                        message = await websocket.recv()
                        messages = JSON.loads(message)
                        if messages['type'] == 'MATCH_UPDATE':
                            if messages['payload']['matchUuid'] == matchId:
                                await websocketServer.send(JSON.dumps(messages['payload']))
                    except websockets.ConnectionClosed:
                        print("Connection closed")
                        break
                    except Exception:
                        print("Exception")
                        break
        except Exception:
            print("Error")

        await asyncio.sleep(5)
        print("try reconnecting")


if __name__ == "__main__":
    matchId = input("Match id: ")
    start_server = websockets.serve(hello, port=8765)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
