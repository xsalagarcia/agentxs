import json
import os
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from agentxs.models.historical import HistoricalChats
from agentxs.settings.settings import settings

os.environ["IN_MEMORY_DB"] = "Yes"
from agentxs.service import historical as service

class TestHistorical(unittest.TestCase):
    @patch("agentxs.data.historical.create_historical", return_value=1)
    def test_create_historical(self, *args: Mock):
        chat = [
    {
        'content': '\nCan you do some modifications at my code to remove swagger documentation at my project? The code that defines the fastAPI application starts at main.py',
        'role': 'user'
    },
    {
        'arguments': '{"filename":"main.py"}',
        'call_id': 'call_FmlRt7NtJ7ICJsIeKl7AEhtp',
        'name': 'get_paths_from_filename',
        'type': 'function_call',
        'id': 'fc_68171bac9fc081918c106fe0b134d38e09c2f73302e56aed',
        'status': 'completed'
    },
    {
        'call_id': 'call_FmlRt7NtJ7ICJsIeKl7AEhtp',
        'output': "['/home/xevi/Documents/Projectes/clinixs_back/app/main.py', '/home/xevi/Documents/Projectes/clinixs_back/venv/lib/python3.11/site-packages/uvicorn/main.py', '/home/xevi/Documents/Projectes/clinixs_back/venv/lib/python3.11/site-packages/watchfiles/main.py', '/home/xevi/Documents/Projectes/clinixs_back/venv/lib/python3.11/site-packages/markdown_it/main.py', '/home/xevi/Documents/Projectes/clinixs_back/venv/lib/python3.11/site-packages/pip/_internal/main.py', '/home/xevi/Documents/Projectes/clinixs_back/venv/lib/python3.11/site-packages/pip/_internal/cli/main.py', '/home/xevi/Documents/Projectes/clinixs_back/venv/lib/python3.11/site-packages/typer/main.py', '/home/xevi/Documents/Projectes/clinixs_back/venv/lib/python3.11/site-packages/pydantic_settings/main.py', '/home/xevi/Documents/Projectes/clinixs_back/venv/lib/python3.11/site-packages/pydantic/main.py', '/home/xevi/Documents/Projectes/clinixs_back/venv/lib/python3.11/site-packages/pydantic/v1/main.py', '/home/xevi/Documents/Projectes/clinixs_back/venv/lib/python3.11/site-packages/dotenv/main.py', '/home/xevi/Documents/Projectes/clinixs_back/venv/lib/python3.11/site-packages/sqlmodel/main.py']",
        'type': 'function_call_output'
    },
    {
        'arguments': '{"path":"/home/xevi/Documents/Projectes/clinixs_back/app/main.py"}',
        'call_id': 'call_R006XEsIgzdtItp39MonA7Wx',
        'name': 'get_file_content',
        'type': 'function_call',
        'id': 'fc_68171bae173c8191a1b2da6dfd29465309c2f73302e56aed',
        'status': 'completed'
    },
    {
        'call_id': 'call_R006XEsIgzdtItp39MonA7Wx',
        'output': 'import asyncio\nfrom pathlib import PurePath\nfrom urllib.parse import urlencode\n\nfrom fastapi import FastAPI, Request, HTTPException\nfrom starlette.responses import RedirectResponse, JSONResponse\nfrom starlette.staticfiles import StaticFiles\n\nfrom app.settings.settings import settings\nfrom app.service import auth as auth_service\nfrom app.router.api import root\nfrom app.service import middleware as middleware_service\n\napp = FastAPI(  #lifespan=lifespan,\n    title="Clinixs API",\n    version="0.0.1",\n    description="Clinixs API single tenant."\n)\n\n#app.mount("/static", StaticFiles(directory=PurePath(__file__).parent.parent.joinpath("static")), name="static")\n\n\napp.include_router(root.router)\n\n@app.exception_handler(403)\nasync def status_403_exception_handler(request: Request, exception: HTTPException):\n    """\n    All requests that requires the user is identified and is not, will finish here.\n    Called before @app.middleware.\n    :param request:\n    :param exception:\n    :return:\n    """\n    middleware_service.add_login_fail(request.client.host)\n    await asyncio.sleep(2)\n\n    query_params = ({"client_id": settings.org_settings.clinixs_client_id,\n                     "redirect_uri": settings.auth_settings.clinixs_callback_uri} |\n                    auth_service.generate_state_and_code_challenge())\n\n    return RedirectResponse(f"{settings.auth_settings.clinixs_auth_service_url}?{urlencode(query_params)}", status_code=300)\n\n\n@app.middleware("http")\nasync def unauthorized_requests_management(request: Request, call_next):\n    # before processing request.\n    client_ip = request.headers.get("x-forwarded-for", "").split(",")[0]\n    if client_ip == "":\n        client_ip = request.client.host\n    if middleware_service.is_ip_locked(client_ip):\n        return JSONResponse(status_code=403, content="Too many requests.")\n    response = await call_next(request)\n\n    # After processing request.\n    if response.status_code in {401}:  # 403 will never be gotten because of the exception_handler(403). But is login fail, too.\n        middleware_service.add_login_fail(client_ip)\n        await asyncio.sleep(2)\n    return response\n\n\nif __name__ == "__main__":\n    import uvicorn\n\n    uvicorn.run("main:app", reload=True, host="127.0.0.1", port=8001)\n',
        'type': 'function_call_output'
    },
    {
        'id': 'msg_68171baf46708191a3248c13b2438ec209c2f73302e56aed',
        'content': [
            {
                'annotations': [],
                'text': 'To remove the Swagger documentation from your FastAPI application, you can disable the automatic generation of Swagger UI and ReDoc by modifying the `FastAPI` initialization parameters. You need to set `docs_url` and `redoc_url` to `None`.\n\nHere’s the modified section of your `main.py` file:\n\n```python\napp = FastAPI(\n    title="Clinixs API",\n    version="0.0.1",\n    description="Clinixs API single tenant.",\n    docs_url=None,  # Disable Swagger UI\n    redoc_url=None  # Disable ReDoc\n)\n```\n\nThe complete modified `main.py` file would look like this:\n\n```python\nimport asyncio\nfrom pathlib import PurePath\nfrom urllib.parse import urlencode\n\nfrom fastapi import FastAPI, Request, HTTPException\nfrom starlette.responses import RedirectResponse, JSONResponse\n\nfrom app.settings.settings import settings\nfrom app.service import auth as auth_service\nfrom app.router.api import root\nfrom app.service import middleware as middleware_service\n\napp = FastAPI(\n    title="Clinixs API",\n    version="0.0.1",\n    description="Clinixs API single tenant.",\n    docs_url=None,  # Disable Swagger UI\n    redoc_url=None  # Disable ReDoc\n)\n\napp.include_router(root.router)\n\n@app.exception_handler(403)\nasync def status_403_exception_handler(request: Request, exception: HTTPException):\n    middleware_service.add_login_fail(request.client.host)\n    await asyncio.sleep(2)\n\n    query_params = ({"client_id": settings.org_settings.clinixs_client_id,\n                     "redirect_uri": settings.auth_settings.clinixs_callback_uri} |\n                    auth_service.generate_state_and_code_challenge())\n\n    return RedirectResponse(f"{settings.auth_settings.clinixs_auth_service_url}?{urlencode(query_params)}", status_code=300)\n\n@app.middleware("http")\nasync def unauthorized_requests_management(request: Request, call_next):\n    client_ip = request.headers.get("x-forwarded-for", "").split(",")[0]\n    if client_ip == "":\n        client_ip = request.client.host\n    if middleware_service.is_ip_locked(client_ip):\n        return JSONResponse(status_code=403, content="Too many requests.")\n    response = await call_next(request)\n\n    if response.status_code in {401}:  \n        middleware_service.add_login_fail(client_ip)\n        await asyncio.sleep(2)\n    return response\n\nif __name__ == "__main__":\n    import uvicorn\n\n    uvicorn.run("main:app", reload=True, host="127.0.0.1", port=8001)\n```\n\nWould you like me to save these changes to your `main.py` file?',
                'type': 'output_text'
            }],
        'role': 'assistant',
        'status': 'completed',
        'type': 'message'}]
        settings.data_folder = Path(__file__).parent
        service.create_historical(agent_name="python_agent", name="My chat", description="A nice chat.", chat=chat)
        args[0].assert_called_once()
        self.assertEqual(args[0].call_args.kwargs.get("historical").agent_name, "python_agent")
        self.assertEqual(args[0].call_args.kwargs.get("historical").name, "My chat")
        self.assertEqual(args[0].call_args.kwargs.get("historical").description, "A nice chat.")

        self.assertTrue(Path(settings.data_folder).joinpath(f"{args[0].return_value}.json").is_file())
        with open(Path(settings.data_folder).joinpath(f"{args[0].return_value}.json")) as file:
            recovered_chat = json.load(file)
        self.assertEqual(chat, recovered_chat)

        os.remove(Path(settings.data_folder).joinpath(f"{args[0].return_value}.json"))


