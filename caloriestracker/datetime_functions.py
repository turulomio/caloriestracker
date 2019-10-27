## THIS IS FILE IS FROM https://github.com/turulomio/reusingcode IF YOU NEED TO UPDATE IT PLEASE MAKE A PULL REQUEST IN THAT PROJECT
## DO NOT UPDATE IT IN YOUR CODE IT WILL BE REPLACED USING FUNCTION IN README

## If a function only can be used by dtaware or naive it will have its prefix dtaware_ or dtnaive_
## If a function can use both of them its prefix will be dt_


from datetime import timedelta, datetime, date, time
from pytz import timezone
from logging import error
from .decorators import deprecated #To use main remove dot from decorators

## Types for dt strings. Used in dtaware2string function
class eDtStrings:
    ## Parsed for ui
    QTableWidgetItem=1
    
    ## 20190909 0909
    Filename=2
    
    ## 201909090909
    String=3

## Returns if a datetime is aware
def is_aware(dt):
    if dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None:
        return False
    return True

## Returns if a datetime is naive
def is_naive(dt):
    return not is_aware(dt)


## Function to create a datetime aware object
## @param date datetime.date object
## @param hour hour object
## @param tz_name String with datetime tz_name name. For example "Europe/Madrid"
## @return datetime aware
def dtaware(date, hour, tz_name):
    z=timezone(tz_name)
    a=dtnaive(date, hour)
    a=z.localize(a)
    return a

def dtaware_now(tzname='UTC'):
    return timezone(tzname).localize(dtnaive_now())

def dtnaive_now():
    return datetime.now()


## Function to create a datetime aware object
## @param date datetime.date object
## @param hour hour object
## @return datetime naive
def dtnaive(date, hour):
    return datetime(date.year,  date.month,  date.day,  hour.hour,  hour.minute,  hour.second, hour.microsecond)

## Function that converts a number of days to a string showing years, months and days
## @param days Integer with the number of days
## @return String like " 0 years, 1 month and 3 days"
def days2string(days):
    from PyQt5.QtWidgets import QApplication
    years=days//365
    months=(days-years*365)//30
    days=int(days -years*365 -months*30)
    if years==1:
        stryears=QApplication.translate("Core", "year")
    else:
        stryears=QApplication.translate("Core", "years")
    if months==1:
        strmonths=QApplication.translate("Core", "month")
    else:
        strmonths=QApplication.translate("Core", "months")
    if days==1:
        strdays=QApplication.translate("Core", "day")
    else:
        strdays=QApplication.translate("Core", "days")
    return QApplication.translate("Core", "{} {}, {} {} and {} {}").format(years, stryears,  months,  strmonths, days,  strdays)

## Returns a date with the first date of the month
## @param year Year to search fist day
## @param month Month to search first day
def date_first_of_the_month(year, month):
    return date(year, month, 1)

## Returns a date with the last date of the month
## @param year Year to search last day
## @param month Month to search last day
def date_last_of_the_month(year, month):
    if month==12:
        return date(year, month, 31)
    return date(year, month+1, 1)-timedelta(days=1)
    
## Returns a date with the first date of the month after x months
## @param year Year to search  day
## @param month Month to search day
## @param x Number of months after parameters. Must be positive
def date_first_of_the_next_x_months(year, month, x):
    last=date(year, month, 1)
    for i in range(x):
        last=date_last_of_the_month(last.year, last.month)
        last=last+timedelta(days=1)
    return last    

## Returns a date with the last date of the month after x months
## @param year Year to search  day
## @param month Month to search day
## @param x Number of months after parameters. Must be positive
def date_last_of_the_next_x_months(year, month, x):
    first=date_first_of_the_next_x_months(year, month, x)
    return date_last_of_the_month(first.year, first.month)

def dtaware_month_end(year, month, tz_name):
    return dtaware_day_end_from_date(date_last_of_the_month(year, month), tz_name)
    
## Returns an aware datetime with the start of year
def dtaware_year_start(year, tz_name):
    return dtaware_day_start_from_date(date(year, 1, 1), tz_name)
    
## Returns an aware datetime with the last of year
def dtaware_year_end(year, tz_name):
    return dtaware_day_end_from_date(date(year, 12, 31), tz_name)
    
## Returns a dtnaive or dtawre (as parameter) with the end of the day
def dt_day_end(dt):
    return dt.replace(hour=23, minute=59, second=59, microsecond=999999)

## Returns the end of the day dtnaive from a date
def dtnaive_day_end_from_date(dat):
    dt=datetime(dat.year, dat.month, dat.day)
    return dt_day_end(dt)

## Returns the end of the day dtaware of the tz_name timezone from a date
def dtaware_day_end_from_date(date, tz_name):
    dt=dtaware(date, time(0, 0), tz_name)
    return dt_day_end(dt)    
    
## Returns a dtnaive or dtawre (as parameter) with the end of the day
def dt_day_start(dt):
    return dt.replace(hour=0, minute=0, second=0, microsecond=0)

## Returns the end of the day dtnaive from a date
def dtnaive_day_start_from_date(dat):
    dt=datetime(dat.year, dat.month, dat.day)
    return dt_day_start(dt)

## Returns the end of the day dtaware of the tz_name timezone from a date
def dtaware_day_start_from_date(date, tz_name):
    dt=dtaware(date, time(0, 0), tz_name)
    return dt_day_start(dt)

## Returns the start of a month
def dtaware_month_start(year, month, tz_name):
    return dtaware_day_start_from_date(date(year, month, 1), tz_name)
    
def month2int(s):
    """
        Converts a month string to a int
    """
    if s in ["Jan", "Ene", "Enero", "January", "enero", "january"]:
        return 1
    if s in ["Feb", "Febrero", "February", "febrero", "february"]:
        return 2
    if s in ["Mar", "Marzo", "March", "marzo", "march"]:
        return 3
    if s in ["Apr", "Abr", "April", "Abril", "abril", "april"]:
        return 4
    if s in ["May", "Mayo", "mayo", "may"]:
        return 5
    if s in ["Jun", "June", "Junio", "junio", "june"]:
        return 6
    if s in ["Jul", "July", "Julio", "julio", "july"]:
        return 7
    if s in ["Aug", "Ago", "August", "Agosto", "agosto", "august"]:
        return 8
    if s in ["Sep", "Septiembre", "September", "septiembre", "september"]:
        return 9
    if s in ["Oct", "October", "Octubre", "octubre", "october"]:
        return 10
    if s in ["Nov", "Noviembre", "November", "noviembre", "november"]:
        return 11
    if s in ["Dic", "Dec", "Diciembre", "December", "diciembre", "december"]:
        return 12

def string2time(s, format="HH:MM"):
    allowed=["HH:MM", "HH:MM:SS","HH:MMxx"]
    if format in allowed:
        if format=="HH:MM":#12:12
            a=s.split(":")
            return time(int(a[0]), int(a[1]))
        elif format=="HH:MM:SS":#12:12:12
            a=s.split(":")
            return time(int(a[0]), int(a[1]), int(a[2]))
        elif format=="HH:MMxx": #5:12am o pm
            s=s.upper()
            s=s.replace("AM", "")
            if s.find("PM"):
                s=s.replace("PM", "")
                points=s.split(":")
                return time(int(points[0])+12, int(points[1]))
            else:#AM
                points=s.split(":")
                return time(int(points[0]), int(points[1]))
    else:
        error("I can't convert this format '{}'. I only support this {}".format(format, allowed))

## Converts a time to a string
def time2string(ti, format="HH:MM" ):
    allowed=["HH:MM", "HH:MM:SS","Xulpymoney"]
    if format in allowed:
        if ti==None:
            return None
        if format=="Xulpymoney":
            if ti.microsecond in (4, 5):
                return str(ti)[11:-13]
            else:
                return str(ti)[11:-6]
        elif format=="HH:MM":
            return ("{}:{}".format(str(ti.hour).zfill(2), str(ti.minute).zfill(2)))
        elif format=="HH:MM:SS":
            return ("{}:{}:{}".format(str(ti.hour).zfill(2), str(ti.minute).zfill(2), str(ti.second).zfill(2)))


def string2date(iso, format="YYYY-MM-DD"):
    allowed=["YYYY-MM-DD", "DD/MM/YYYY", "DD.MM.YYYY", "DD/MM"]
    if format in allowed:
        if format=="YYYY-MM-DD": #YYYY-MM-DD
            d=iso.split("-")
            return date(int(d[0]), int(d[1]),  int(d[2]))
        if format=="DD/MM/YYYY": #DD/MM/YYYY
            d=iso.split("/")
            return date(int(d[2]), int(d[1]),  int(d[0]))
        if format=="DD.MM.YYYY": #DD.MM.YYYY
            d=iso.split(".")
            return date(int(d[2]), int(d[1]),  int(d[0]))
        if format=="DD/MM": #DD/MM
            d=iso.split("/")
            return date(date.today().year, int(d[1]),  int(d[0]))
    else:
        error("I can't convert this format '{}'. I only support this {}".format(format, allowed))

        
## Function to generate a datetime aware from a string
## @param s String
## @param type Integer
## @param tz_name Name of the tz_name. By default "Europe Madrid" only in type 3and 4
## @return Datetime
@deprecated
def string2dtaware_old(s, type, tz_name="Europe/Madrid"):
    if type==1:#2017-11-20 23:00:00+00:00  ==> Aware
        s=s[:-3]+s[-2:]
        dat=datetime.strptime( s, "%Y-%m-%d %H:%M:%S%z" )
        return dat
    if type==3:#20/11/2017 23:00 ==> Aware, using zone parameter
        dat=datetime.strptime( s, "%d/%m/%Y %H:%M" )
        z=timezone(tz_name)
        return z.localize(dat)
    if type==4:#27 1 16:54 2017==> Aware, using zone parameter . 1 es el mes convertido con month2int
        dat=datetime.strptime( s, "%d %m %H:%M %Y")
        z=timezone(tz_name)
        return z.localize(dat)
    if type==5:#2017-11-20 23:00:00.000000+00:00  ==> Aware with microsecond
        s=s[:-3]+s[-2:]#quita el :
        arrPunto=s.split(".")
        s=arrPunto[0]+s[-5:]
        micro=int(arrPunto[1][:-5])
        dat=datetime.strptime( s, "%Y-%m-%d %H:%M:%S%z" )
        dat=dat+timedelta(microseconds=micro)
        return dat
    if type==6:#201907210725 ==> Aware
        dat=datetime.strptime( s, "%Y%m%d%H%M" )
        z=timezone(tz_name)
        return z.localize(dat)
    if type==7:#01:02:03 ==> Aware
        tod=date.today()
        a=s.split(":")
        dat=datetime(tod.year, tod.month, tod.day, int(a[0]), int(a[1]), int(a[2]))
        z=timezone(tz_name)
        return z.localize(dat)

@deprecated
def string2dtnaive_old(s, type):
    if type==2:#20/11/2017 23:00 ==> Naive
        dat=datetime.strptime( s, "%d/%m/%Y %H:%M" )
        return dat
    if type==6:#201907210725 ==> Naive
        dat=datetime.strptime( s, "%Y%m%d%H%M" )
        return dat

def string2dtnaive(s, format):
    allowed=["%Y%m%d%H%M","%Y-%m-%d %H:%M:%S","%d/%m/%Y %H:%M","%d %m %H:%M %Y","%Y-%m-%d %H:%M:%S.","%H:%M:%S"]
    if format in allowed:
        if format=="%Y%m%d%H%M":
            dat=datetime.strptime( s, format )
            return dat
        if format=="%Y-%m-%d %H:%M:%S":#2017-11-20 23:00:00
            return datetime.strptime( s, format )
        if format=="%d/%m/%Y %H:%M":#20/11/2017 23:00
            return datetime.strptime( s, format )
        if format=="%d %m %H:%M %Y":#27 1 16:54 2017. 1 es el mes convertido con month2int
            return datetime.strptime( s, format)
        if format=="%Y-%m-%d %H:%M:%S.":#2017-11-20 23:00:00.000000  ==>  microsecond. Notice the point in format
            arrPunto=s.split(".")
            s=arrPunto[0]
            micro=int(arrPunto[1])
            dt=datetime.strptime( s, "%Y-%m-%d %H:%M:%S" )
            dt=dt+timedelta(microseconds=micro)
            return dt
        if format=="%H:%M:%S": 
            tod=date.today()
            a=s.split(":")
            return datetime(tod.year, tod.month, tod.day, int(a[0]), int(a[1]), int(a[2]))
    else:
        error("I can't convert this format '{}'. I only support this {}".format(format, allowed))

def string2dtaware(s, format, tz_name='UTC'):
    allowed=["%Y-%m-%d %H:%M:%S%z","%Y-%m-%d %H:%M:%S.%z"]
    if format in allowed:
        if format=="%Y-%m-%d %H:%M:%S%z":#2017-11-20 23:00:00+00:00
            s=s[:-3]+s[-2:]
            dt=datetime.strptime( s, format )
            return dtaware_changes_tz(dt, tz_name)
        if format=="%Y-%m-%d %H:%M:%S.%z":#2017-11-20 23:00:00.000000+00:00  ==>  microsecond. Notice the point in format
            s=s[:-3]+s[-2:]#quita el :
            arrPunto=s.split(".")
            s=arrPunto[0]+s[-5:]
            micro=int(arrPunto[1][:-5])
            dt=datetime.strptime( s, "%Y-%m-%d %H:%M:%S%z" )
            dt=dt+timedelta(microseconds=micro)
            return dtaware_changes_tz(dt, tz_name)
    else:
        return timezone(tz_name).localize(string2dtnaive(s,format))

## epoch is the time from 1,1,1970 in UTC
## return now(timezone(self.name))
def dtaware2epochms(d):
    return d.timestamp()*1000
    
## Return a UTC datetime aware
def epochms2dtaware(n, tz="UTC"):
    utc_unaware=datetime.utcfromtimestamp(n/1000)
    utc_aware=utc_unaware.replace(tzinfo=timezone('UTC'))#Due to epoch is in UTC
    return dtaware_changes_tz(utc_aware, tz)


## Returns a formated string of a dtaware string formatting with a zone name
## @param dt datetime aware object
## @return String
def dtaware2string(dt, type=eDtStrings.QTableWidgetItem):
    if dt==None:
        return "None"
    elif dt.tzname()==None:
        return "Naive date and time"
    else:
        return dtnaive2string(dt, type)

## Returns a formated string of a dtaware string formatting with a zone name
## @param dt datetime aware object
## @return String
def dtnaive2string(dt, type=eDtStrings.QTableWidgetItem):
    if dt==None:
        resultado="None"
    elif type==eDtStrings.QTableWidgetItem:
        if dt.microsecond==4 :
            resultado="{}-{}-{}".format(dt.year, str(dt.month).zfill(2), str(dt.day).zfill(2))
        else:
            resultado="{}-{}-{} {}:{}:{}".format(dt.year, str(dt.month).zfill(2), str(dt.day).zfill(2), str(dt.hour).zfill(2), str(dt.minute).zfill(2),  str(dt.second).zfill(2))
    elif type==eDtStrings.Filename:
            resultado="{}{}{} {}{}".format(dt.year, str(dt.month).zfill(2), str(dt.day).zfill(2), str(dt.hour).zfill(2), str(dt.minute).zfill(2))
    elif type==eDtStrings.String:
        resultado="{}{}{}{}{}".format(dt.year, str(dt.month).zfill(2), str(dt.day).zfill(2), str(dt.hour).zfill(2), str(dt.minute).zfill(2))
    return resultado
    
## Changes zoneinfo from a dtaware object
## For example:
## - datetime.datetime(2018, 5, 18, 8, 12, tzinfo=<DstTzInfo 'Europe/Madrid' CEST+2:00:00 DST>)
## - libcaloriestrackerfunctions.dtaware_changes_tz(a,"Europe/London")
## - datetime.datetime(2018, 5, 18, 7, 12, tzinfo=<DstTzInfo 'Europe/London' BST+1:00:00 DST>)
## @param dt datetime aware object
## @tzname String with datetime zone. For example: "Europe/Madrid"
## @return datetime aware object
def dtaware_changes_tz(dt,  tzname):
    if dt==None:
        return None
    tzt=timezone(tzname)
    tarjet=tzt.normalize(dt.astimezone(tzt))
    return tarjet


if __name__ == "__main__":
    tz="Europe/Madrid"
    now=datetime.now()
    print("Current localzone is", tz)
    print ("DtNaive:",  now)
    now_aware=dtaware(now.date(), now.time(), tz)
    print("DtAware:", now_aware)
    epochms=dtaware2epochms(now_aware)
    print("Epoch in miliseconds:", epochms)
    print("Dtaware reconverting epoch {}".format(epochms2dtaware(epochms, tz)) )
    print("This is a dataware string wight eDtStrings.QTableWidgetItem:", dtaware2string(now_aware, eDtStrings.QTableWidgetItem))
    print("This is a dataware string wight eDtStrings.Filename:", dtaware2string(now_aware, eDtStrings.Filename))
    print("This is a dataware string wight eDtStrings.String:", dtaware2string(now_aware, eDtStrings.String))
    now_aware_in_utc=dtaware_changes_tz(now_aware, 'UTC')
    print("Datetime '{}' changes to UTC '{}'".format(now_aware, now_aware_in_utc))
    print()
    print("dt_day_end")
    print("  - Today will end at '{}' as naive".format(dt_day_end(now)))
    print("  - Today will end at '{}' as aware in this timezone '{}'".format( dt_day_end(now_aware), tz))
    print()    
    print("time2string")
    print("  - This is the current hour '{}' with format HH:MM".format(time2string(now.time(), "HH:MM")))
    print("  - This is the current hour '{}' with format HH:MM:SS".format(time2string(now.time(), "HH:MM:SS")))

    print("string2dtnaive and string2dtaware")
    a="201910022209"
    format="%Y%m%d%H%M"
    print("  - {}: {} and {}".format(a,string2dtnaive(a,format),string2dtaware(a,format)))
    a="2019-10-03 2:22:09"
    format="%Y-%m-%d %H:%M:%S"
    print("  - {}: {} and {}".format(a,string2dtnaive(a,format),string2dtaware(a,format)))
    a="2019-10-03 2:22:09+05:00"
    format="%Y-%m-%d %H:%M:%S%z"
    print("  - {}: UTC: {}. Madrid: {}".format(a,string2dtaware(a,format),string2dtaware(a,format,"Europe/Madrid")))
    a="2019-10-03 2:22:09.267+05:00"
    format="%Y-%m-%d %H:%M:%S.%z"
    print("  - {}: UTC: {}. Madrid: {}".format(a,string2dtaware(a,format),string2dtaware(a,format,"Europe/Madrid")))
    a="2019-10-03 2:22:09"
    format="%Y-%m-%d %H:%M:%S"
    print("  - {}: {} and {}".format(a,string2dtnaive(a,format),string2dtaware(a,format)))
    a="2019-10-03 2:22:09.267"
    format="%Y-%m-%d %H:%M:%S."
    print("  - {}: {} and {}".format(a,string2dtnaive(a,format),string2dtaware(a,format)))
