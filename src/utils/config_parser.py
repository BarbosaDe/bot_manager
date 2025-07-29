import io
import zipfile
from contextlib import ExitStack

from squarecloud.utils import ConfigFile


def get_squarecloud_config(zip_bytes: bytes):
    with ExitStack() as stack:
        zip_memory = stack.enter_context(io.BytesIO(zip_bytes))
        zip = stack.enter_context(zipfile.ZipFile(zip_memory))

        files = zip.namelist()

        config_file = next(
            (a for a in files if a in {"squarecloud.config", "squarecloud.app"}), None
        )

        if not config_file:
            return None

        config_content = zip.read(config_file).decode().splitlines()

        config = {}
        for line in config_content:
            k, v = line.split("=", 1)

            config[k.strip()] = v

        return ConfigFile(
            display_name=config["DISPLAY_NAME"],
            main=config["MAIN"],
            memory=int(config["MEMORY"]),
            version=config["VERSION"],
            description=config.get("DESCRIPTION"),
            subdomain=config.get("SUBDOMAIN"),
            start=config.get("START"),
            auto_restart=config.get("AUTORESTART", False),
        )


def insert_squarecloud_config(zip_bytes: bytes, filename: str, content: bytes) -> bytes:
    """
    Insere um novo arquivo (ou substitui, se já existir) dentro de um ZIP.

    :param zip_bytes: bytes do arquivo ZIP original
    :param filename: nome do novo arquivo a ser inserido (ex: "config.txt")
    :param content: conteúdo do novo arquivo em bytes
    :return: bytes do novo arquivo ZIP
    """
    original_zip = zipfile.ZipFile(io.BytesIO(zip_bytes), "r")
    new_zip_buffer = io.BytesIO()
    with zipfile.ZipFile(
        new_zip_buffer, "w", compression=zipfile.ZIP_DEFLATED
    ) as new_zip:
        for item in original_zip.infolist():
            if item.filename != filename:
                new_zip.writestr(item.filename, original_zip.read(item.filename))

        new_zip.writestr(filename, content)

    original_zip.close()
    new_zip_buffer.seek(0)
    return new_zip_buffer.read()
