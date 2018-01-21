import time

def code2int(s):
    s=int(s)
    return s

def code2double(s):
    s=float(s)
    return s
    
def getcode(s):
    a=s.split(',')
    return a[0]
   
def getdate(s):
    a=s.split(',')
    return a[1]

def getmonth1(s):
    a=s.split(',')
    datenew=time.strptime(a[1], "%Y-%m-%d")
    return datenew.tm_mon

def getmonth2(s):
    datenew=time.strptime(s, "%Y/%m/%d")
    return datenew.tm_mon

def getyear1(s):
    a=s.split(',')
    datenew=time.strptime(a[1], "%Y-%m-%d")
    return datenew.tm_year

def getyear2(s):
    datenew=time.strptime(s, "%Y/%m/%d")
    return datenew.tm_year

def getequity(s):
    a=s.split(',')
    return a[5]

def changeyear(s):
    datenew=time.strptime(s, "%Y/%m/%d")
    if datenew.tm_mon>4:
        return datenew.tm_year
    else:
        return datenew.tm_year-1
    
def getday(s):
    datenew=time.strptime(s, "%Y/%m/%d")
    return datenew.tm_mday
