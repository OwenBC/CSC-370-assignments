#!/bin/python3

import sys
import re

def strToDate(dateString):
    return re.split("-", dateString)

def beforeOrOn(date1, date2):
    (y1,m1,d1)=strToDate(date1)
    (y2,m2,d2)=strToDate(date2)
    y1=int(y1)
    y2=int(y2)
    m1=int(m1)
    m2=int(m2)
    d1=int(d1)
    d2=int(d2)
    if y1 < y2:
        return True
    elif y1 == y2:
        if m1 < m2:
            return True
        elif m1 == m2:
            if d1 <= d2:
                return True
    return False

weights = (("2022-01-21", 5),("2022-01-28", 20),("2022-02-11", 5),("2022-02-18", 20),("2022-03-11", 5),("2022-03-18", 20),("2022-04-01", 5),("2022-04-08", 20))

date = sys.argv[1]
if date == 'dropdate100':
    date = '2022-01-30'
elif date == 'dropdate50':
    date = '2022-02-13'
elif date == 'dropdate0':
    date = '2022-02-28'

grade = 0
for deadline in weights:
    if beforeOrOn(deadline[0], date):
        grade += deadline[1]
print(str(grade)+"%")
