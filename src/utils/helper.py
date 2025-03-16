def extendContainers(containers: list):
    class AppContainer(*containers):
        pass

    return AppContainer()
