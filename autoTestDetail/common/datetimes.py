# -*- coding:utf8 -*-

from time import strftime, localtime
from datetime import timedelta, date,datetime
import calendar

year = strftime("%Y", localtime())
mon = strftime("%m", localtime())
day = strftime("%d", localtime())
hour = strftime("%H", localtime())
min = strftime("%M", localtime())
sec = strftime("%S", localtime())


def today():
    """返回当天的str类型YYYY-MM-DD"""
    return str(date.today())

def nowTime():
    """返回当前时间的str类型YYYY-MM-DD HH:MM:SS"""
    return strftime("%Y-%m-%d %H:%M:%S", localtime())

def addDays(days=0,date=None):
    """在当前的前提下加减天数，返回date类型YYYY-MM-DD"""
    if days < 0:
        if date:
            time = datetime.strptime(date,'%Y-%m-%d') - timedelta(days=abs(days))
            return time.strftime('%Y-%m-%d')
        else:
            return str(date.today() - timedelta(days=abs(days)))
    else:
        if date:
            time = datetime.strptime(date,'%Y-%m-%d') + timedelta(days=(days))
            return time.strftime('%Y-%m-%d')
        else:
            return str(date.today() + timedelta(days=days))

def addMonths(months=0,date=None):
    """在当前的前提下加减月数，返回date类型YYYY-MM-DD"""
    (y, m, d) = getyearandmonth(months) if not date else getyearandmonth(months,date)
    arr = (y, m, d)
    if (int(d) > get_days_of_date(int(y),int(m))):
        arr = (y, m, get_days_of_date(int(y),int(m)))
    return "-".join("%s" % i for i in arr)

def get_days_of_date(year, mon):
    """"返回指定月份的天数"""
    return calendar.monthrange(year, mon)[1]

def getyearandmonth(n=0,date=None):
    '''''
    get the year,month,days from today
    befor or after n months
    '''
    if date:
        time = date.split('-')
        thisyear,thismon = int(time[0]),int(time[1])
        totalmon = thismon+n
    else:
        thisyear, thismon = int(year),int(mon)
        totalmon = thismon + n
    if (n >= 0):
        if (totalmon <= 12):
            days = str(get_days_of_date(thisyear, totalmon))
            totalmon = addzero(totalmon)
            return (year, totalmon, days) if not date else (time[0],totalmon,time[2])
        else:
            i = totalmon / 12
            j = totalmon % 12
            if (j == 0):
                i -= 1
                j = 12
            thisyear += i
            days = str(get_days_of_date(thisyear, j))
            j = addzero(j)
            return (str(thisyear), str(j), days if not date else time[2])
    else:
        if ((totalmon > 0) and (totalmon < 12)):
            days = str(get_days_of_date(thisyear, totalmon))
            totalmon = addzero(totalmon)
            return (year, totalmon, days) if not date else (time[0],totalmon,time[2])
        else:
            i = totalmon / 12
            j = totalmon % 12
            if (j == 0):
                i -= 1
                j = 12
            thisyear += i
            days = str(get_days_of_date(thisyear, j))
            j = addzero(j)
            return (str(thisyear), str(j), days if not date else time[2])

def addzero(n):
    '''''
    add 0 before 0-9
    return 01-09
    '''
    nabs = abs(int(n))
    if (nabs < 10):
        return "0" + str(nabs)
    else:
        return nabs


if __name__ == "__main__":
    a = addMonths(1,'2016-10-31')
    print a