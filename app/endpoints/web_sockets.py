import time

from fastapi import APIRouter, WebSocket, Cookie, Depends, Query, WebSocketException, status, WebSocketDisconnect
from fastapi.responses import HTMLResponse

router = APIRouter()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var client_id = "user_" + Math.floor(Math.random() * 100) + 1;
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://localhost:80/api/v1/websocket/forum/${client_id}`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
        self.connections: dict = {}

    async def connection_available(self, websocket: WebSocket, client_id: str):
        # sourcery skip: assign-if-exp, boolean-if-exp-identity, reintroduce-else, remove-unnecessary-cast
        """
        Check if there is a websocket matching with another in the same dict key.
        In false case, a new dictionary with websocket will be created.
        """
        connection_available = await self.assign_partner(websocket, client_id, client_id)
        if not connection_available:
            return False
        return connection_available
        # return True
        # if client_id not in self.connections:
        #     if websocket in self.connections.values():
        #         return True
        #     return False

    async def assign_partner(self, websocket: WebSocket, client_id1: str, client_id2: str):
        if any(client_id1 not in connection for connection in self.connections.values()):
            free_space = next(
                (key for key, value in self.connections.items() if len(value) < 2),
                None
            )
            if free_space:
                self.connections[free_space].append(websocket)
                new_key = f"{free_space} {client_id1}"
                self.connections[new_key] = self.connections.pop(free_space)
                return new_key
        return None
        # print("before host")
        # if host := next(
        #         filter(lambda x: len(self.connections[x]) < 2, self.connections), False
        # ):
        #     # self.connections[host].append(websocket)
        #     self.connections[host][client_id1] = {client_id1: websocket}
        #     if websocket in self.connections[host]:
        #         return self.connections[host]
        #     return self.connections[host]
        # return False

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        sockets = await self.connection_available(websocket, client_id)
        if not sockets:
            self.connections[client_id] = [websocket]
            return self.connections
            # await self.assign_partner(websocket, client_id, client_id)
        self.active_connections.append(websocket)  # esto equivale a self.connections[client_id]
        return next(
            (value for key, value in self.connections.items() if client_id in key),
            None,
        )

    def disconnect(self, websocket: WebSocket, client_id: str):
        self.active_connections.remove(websocket)
        if websocket in self.connections:
            del self.connections[websocket]
        if websocket in self.connections.values():
            self.connections = {key: val for key,
            val in self.connections.items() if val == websocket}

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


# async def get_cookie_or_token(
#         websocket: WebSocket,
#         session: Annotated[str | None, Cookie()] = None,
#         token: Annotated[str | None,  Query()] = None
# ):
#     if session is None and token is None:
#         raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
#     return session or token


@router.get("/")
async def web_socket():
    return HTMLResponse(html)


@router.websocket("/forum/{client_id}")
async def websocket_endpoint(websocket: WebSocket,
                             client_id: str,
                             # cookie_or_token: Annotated[str, Depends(get_cookie_or_token)],
                             q: int | None = None):
    # await websocket.accept()
    # while True:
    #     connections = await manager.connect(websocket, client_id)
    #     if type(connections) is bool:
    #         continue
    # print("SALI DEL PRIMER WHILE")
    # s1, s2 = await manager.connection_available(websocket, client_id)
    # print(s1)
    connections = await manager.connect(websocket, client_id)
    free_space = next(
        (key for key, value in manager.connections.items() if len(value) < 2),
        None
    )

    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")

            # Solo enviar el mensaje al otro websocket en la misma conexión
            # other_websocket = next(
            #     (conn for conn in manager.connections[connections] if conn != websocket),
            #     None
            # )
            # if other_websocket:
            #     await manager.send_personal_message(f"User #{client_id} send: {data}", other_websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket, client_id)
        await manager.broadcast(f"User {client_id} left the chat")

    # await websocket.accept()
    # while True:
    #     data = await websocket.receive_text()
    #     await websocket.send_text(
    #         f"Session cookie or token value is: {cookie_or_token}"
    #
    #     if not q:
    #         await websocket.send_text(f"Query parameter q is: {q}")
    #     await websocket.send_text(f"Message text was: {data}, for ITEM ID: {item_id}")


websocket_router = router
