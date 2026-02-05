"""GCP Cloud Functions Entry Point for FastAPI.

Este arquivo converte requisições Flask (usadas pelo Cloud Functions)
para o formato ASGI que o FastAPI espera.
"""

import asyncio
from io import BytesIO

import functions_framework
from flask import Response

from app.main import app
from app.infrastructure.db.database import Database

# Event loop persistente para reutilização entre requisições
_loop = None
_db_connected = False


def get_or_create_loop():
    """Get existing event loop or create a new one."""
    global _loop
    if _loop is None or _loop.is_closed():
        _loop = asyncio.new_event_loop()
        asyncio.set_event_loop(_loop)
    return _loop


def run_async(coro):
    """Run async coroutine using persistent event loop."""
    loop = get_or_create_loop()
    return loop.run_until_complete(coro)


async def ensure_db_connected():
    """Ensure database is connected (called once per instance)."""
    global _db_connected
    if not _db_connected:
        await Database.connect()
        _db_connected = True


async def handle_request(request):
    """Convert Flask request to ASGI and process with FastAPI."""
    # Ensure database is connected
    await ensure_db_connected()
    
    # Build ASGI scope
    scope = {
        "type": "http",
        "asgi": {"version": "3.0"},
        "http_version": "1.1",
        "method": request.method,
        "path": request.path,
        "query_string": request.query_string,
        "root_path": "",
        "headers": [(k.lower().encode(), v.encode()) for k, v in request.headers],
        "server": (request.host.split(":")[0], 443),
    }

    # Get request body
    body = request.get_data()

    # Response containers
    response_status = 200
    response_headers = []
    response_body = BytesIO()

    async def receive():
        return {"type": "http.request", "body": body, "more_body": False}

    async def send(message):
        nonlocal response_status, response_headers

        if message["type"] == "http.response.start":
            response_status = message["status"]
            response_headers = [
                (k.decode() if isinstance(k, bytes) else k,
                 v.decode() if isinstance(v, bytes) else v)
                for k, v in message.get("headers", [])
            ]
        elif message["type"] == "http.response.body":
            body_content = message.get("body", b"")
            if body_content:
                response_body.write(body_content)

    # Call FastAPI app
    await app(scope, receive, send)

    # Build Flask response
    flask_response = Response(
        response_body.getvalue(),
        status=response_status,
    )
    for key, value in response_headers:
        flask_response.headers[key] = value

    return flask_response


@functions_framework.http
def starwars_api(request):
    """GCP Cloud Function entry point."""
    return run_async(handle_request(request))
