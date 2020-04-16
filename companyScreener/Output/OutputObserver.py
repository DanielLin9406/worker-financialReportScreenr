from __future__ import annotations
from abc import ABC, abstractmethod, abstractproperty
from Output.OutputSubject import Subject
from Output.GoogleSheetObserver import OutPutToGoogleSheet


class Observer(ABC):
    @abstractmethod
    def upload(self, subject: Subject) -> None:
        pass


class GoogleSheetObserver(Observer):
    def __init__(self, **kwargs):
        self._kwargs = kwargs
        self._company = self._kwargs.get('company')
        self._idNum = self._kwargs.get('idNum')

    def upload(self, subject: Subject) -> None:
        for key, value in self._kwargs["tables"].items():
            OutPutToGoogleSheet(**dict(
                df=value,
                sheetTabName=key,
                idNum=self._idNum,
                company=self._company
            )).uploadData()


class PostgreSqlObserver(Observer):
    def __init__(self, **kwargs):
        print('init')

    def upload(self, subject: Subject) -> None:
        print('Not Yet')
