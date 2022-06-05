
from pathlib import Path
import fastapi
import fastapi_chameleon
import uvicorn
from starlette.staticfiles import StaticFiles

from data import db_session

from views import account, home, play, today, api, admin_views

app = fastapi.FastAPI()


def main():
    configure()
    uvicorn.run(app, host="127.0.01", port=8000, log_level="info")


def configure():
    configure_templates()
    configure_routes()
    configure_db(dev_mode=True)


def configure_db(dev_mode: bool):
    file = (Path(__file__).parent / 'db' / 'saucerdb.sqlite').absolute()
    db_session.global_init(file.as_posix())


def configure_templates():
    fastapi_chameleon.global_init("templates")


def configure_routes():
    app.mount("/static", StaticFiles(directory="static"), name="static")
    app.include_router(home.router)
    app.include_router(play.router)
    app.include_router(today.router)
    app.include_router(account.router)
    app.include_router(api.router)
    app.include_router(admin_views.router)


if __name__ == "__main__":
    main()
    uvicorn.run(app, port=8000, host="127.0.0.1")
else:
    configure()
