class Container():

    def __init__(self):
        self.services = {}

    def register(self, name: str, service):
        if name in self.services:
            raise ValueError(f"Service '{name}' is already registered.")

        self.services[name] = service

    def resolve(self, name: str):
        if name not in self.services:
            raise ValueError(f"Service '{name}' is not registered.")

        return self.services[name]

container = Container()