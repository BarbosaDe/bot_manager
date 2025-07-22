import os
import time
from dataclasses import dataclass
from typing import Optional, Union

from squarecloud import Application, Client, File

from exceptions import UPLOAD_ERRORS_TRANSLATIONS


@dataclass(slots=True, frozen=True)
class ApplicationStatus:
    id: str
    name: str
    cpu: str
    ram: str
    network_total: str
    network_now: str
    running: bool
    storage: str
    lang: str
    uptime: Optional[int]


class SquareManager(Client):
    def __init__(self):
        super().__init__(os.environ["SQUARECLOUD_KEY"])

        self.cache = {"applications": []}
        self.ttl = 30
        self.timestamp = 0

    @property
    async def apps(self) -> list[Application]:
        """
        Retorna uma lista cacheada com aplicacões da SquareCloud
        """

        now = time.time()
        if not self.cache["applications"] or now - self.timestamp > self.ttl:
            self.cache["applications"] = await self.all_apps()
            self.timestamp = now

        return self.cache["applications"]

    async def upload_application(self, bytes) -> Union[str, None]:
        """Faz upload de uma aplicacão para SquareCloud"""
        file = File(bytes)

        try:
            return await square_manager.upload_app(file)

        except Exception as e:
            error = UPLOAD_ERRORS_TRANSLATIONS.get(e.__class__.__name__)

            if not error:
                raise e

            return error

    async def status_application(self, application_id: int):
        """Retorna informacões sobre uma aplicacão da SquareCloud"""
        apps = await self.apps
        app = next((app for app in apps if app.id == application_id), None)

        if not app:
            return

        app_status = await self.app_status(application_id)

        return ApplicationStatus(
            name=app.name,
            id=app.id,
            cpu=app_status.cpu,
            network_total=app_status.network["total"],
            network_now=app_status.network["now"],
            ram=f"{app_status.ram}/{app.ram}",
            running=app_status.running,
            storage=app_status.storage,
            lang=app.lang,
            uptime=app_status.uptime,
        )


square_manager = SquareManager()
