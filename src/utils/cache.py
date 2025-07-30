import datetime


class Cache:
    zip_bytes = {}

    @classmethod
    def get(cls, key):
        value = cls.zip_bytes.get(key)

        return value["value"] if value else value

    @classmethod
    def insert(cls, key, value):
        cls.zip_bytes[key] = {
            "value": value,
            "created_at": datetime.datetime.now(datetime.UTC),
        }

    @classmethod
    def delete(cls, key):
        cls.zip_bytes.pop(key)

    @classmethod
    def purge_cache(cls):
        now = datetime.datetime.now(datetime.UTC)
        keys_to_delete = []

        for key, data in cls.zip_bytes.items():
            created_at = data.get("created_at")
            if not created_at:
                continue

            diff = now - created_at
            if diff > datetime.timedelta(minutes=2):
                keys_to_delete.append(key)

        for key in keys_to_delete:
            cls.delete(key)
