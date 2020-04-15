from CreateTables.TableAbstractFactory import TablesFactory, AnalyzeTablesFactory
from Input.InputTemplate import InputTemplate1
from InputPipeline.PipelineHandler import initHandler, leftSpaceStripHandler, transStrToFloatHandler


def createInputFactory(**kwargs):
    factory = InputTemplate1(**kwargs)
    return factory


def createInputPipelineFactory():
    factory = initHandler()
    leftSpaceStrip = leftSpaceStripHandler()
    transStrToFloat = transStrToFloatHandler()
    factory.setNext(
        leftSpaceStrip).setNext(transStrToFloat)
    return factory


def createTablesFactory(**kwargs):
    factory = TablesFactory(**kwargs)
    return factory


def createAnalyzeTablesFactory():
    factory = AnalyzeTablesFactory()
    return factory
