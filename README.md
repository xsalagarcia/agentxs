
# agentxs

Is a simple agent wrapper for playing with openai-agents library. Contains
an example that creates an agent to help with python projects. The path to the
project can be set to allow the agent access the code through custom tools.

# CLI agents: cli_python_agent.py and cli_postgres_agent.py

Brings OpenAI Agents API to the CLI using agentxs package. A CLI tool for playing
with the agent.

If run cli_postgres_app.py or cli_python_agent.py without activating virtual environment is wanted, with
the virtual environment activated install the package in dev mode (`pip install -e .`)
and edit shebang line.

Setting the path which the python agent can access the files and file extensions is necessary.
You can set it using flags when run the script or options when script is running (just type
"help" to see the options). The main purpose is to read the files, not modifying the content or
perform changes actively.

The postgres allows to interact with tables definitions. For this, it's necessary to create the connection
with credentials, database, host, url and port. Credentials are managed locally and never processed
by the llm. When all the credentials are set, a sqlalchemy engine is created. With the custom tools,
available tables, their columns and other properties are available for the llm model. But the database
data (the rows of the tables) are never sent to the llm. The main purpose of this model is to help in 
SQL sentences elaboration: selects, views, triggers, alters... but not accessing to data or modifying 
the database.

## LLM Models

If you want to use more models, just add them to enum. Other from OpenAI can be added using
[LiteLLM](https://openai.github.io/openai-agents-python/models/litellm/)

## About the run context

The [run context](https://openai.github.io/openai-agents-python/ref/run_context/) is set into the AgentWrapper object,
and can be modified anytime. This can be, as openai agents docs says, any dependency or data that never is sent to
the LLM, is only passed to functions, callbacks, hooks. 

When a function tool is called and the first argument is `ctx: RunContextWrapper[Any]` the context is passed. The
context object can be retrieved referencing the context attribute (`ctx.context`).

## Setting the APY key

You need a `.env` file in the root of the project with the API key. See the content of
`.env_sample` file.


```python
[
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
```