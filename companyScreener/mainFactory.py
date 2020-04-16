from Input.InputTemplate import InputTemplate1
from InputPipeline.PipelineHandler import initHandler, leftSpaceStripHandler, transStrToFloatHandler
from CreateTables.TableAbstractFactory import TablesFactory, AnalyzeTablesFactory
from Output.OutputObserver import GoogleSheetObserver, PostgreSqlObserver
from Output.OutputSubject import OutputSubject


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


def createOutputFactory(**kwargs):
    factory = OutputSubject()
    factory.attach(GoogleSheetObserver(**kwargs))
    factory.attach(PostgreSqlObserver(**kwargs))
    return factory
