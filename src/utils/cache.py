class Cache:
    zip_bytes = {}

    @classmethod
    def get(cls, key):
        return cls.zip_bytes.get(key)

    @classmethod
    def insert(cls, key, value):
        cls.zip_bytes[key] = value

    @classmethod
    def delete(cls, key):
        cls.zip_bytes.pop(key)
