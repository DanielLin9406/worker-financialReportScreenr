from Input.InputTemplate import InputTemplate


def createInputFactory(**kwargs):
    factory = InputTemplate(**kwargs)
    return factory
