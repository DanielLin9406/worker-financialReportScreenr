import re
import datetime
import time


def getNow():
    """
    @param: None
    @return: datetime object
    """
    return datetime.datetime.now()


def getColumnNameArr(myStockDF):
    """
    @param: DataFrame
    @return: List
    """
    return [ele for ele in myStockDF.columns.values if re.match("Bid/BidDate-*", ele)]


def getBidDate(myStockDF):
    """
    @param: DataFrame
    @return: List
    """
    bidDateCellArr = [myStockDF.get(bid).iloc[1]
                      for bid in getColumnNameArr(myStockDF)]
    return [ele.split("-") for ele in bidDateCellArr]


def getRawBid(myStockDF):
    """
    @param: DataFrame
    @return: List
    """
    return [float(myStockDF.get(bid).iloc[0][1:]) for bid in getColumnNameArr(myStockDF)]


def getDurationInYear(now, bidDate):
    """
    @param: now: datetime
    @param: bidDAte: datetime
    @return: Number
    """
    duration = now - bidDate
    durationInSecond = duration.total_seconds()
    years = divmod(durationInSecond, 31536000)[0]
    return years


def getUnixTimeStamp(firstBidTime):
    year = int(firstBidTime[0][0])
    month = int(firstBidTime[0][1])
    day = int(firstBidTime[0][2])
    d = datetime.date(year, month, day)
    return str(int(time.mktime(d.timetuple())))
