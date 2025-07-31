import datetime


class Cache:
    _data = {}

    @classmethod
    def get(cls, key):
        value = cls._data.get(key)

        return value["value"] if value else value

    @classmethod
    def insert(cls, key, value):
        cls._data[key] = {
            "value": value,
            "created_at": datetime.datetime.now(datetime.UTC),
        }

    @classmethod
    def delete(cls, key):
        cls._data.pop(key)

    @classmethod
    def purge_cache(cls):
        now = datetime.datetime.now(datetime.UTC)
        keys_to_delete = []

        for key, data in cls._data.items():
            created_at = data.get("created_at")
            if not created_at:
                continue

            diff = now - created_at
            if diff > datetime.timedelta(minutes=2):
                keys_to_delete.append(key)

        for key in keys_to_delete:
            cls.delete(key)
