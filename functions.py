from yahoo_finance import Share
from datetime import date
import operator

import pandas as pd
import numpy as np
import urllib3
import datetime as dt
import matplotlib.pyplot as plt


class EST(dt.tzinfo):
    def utcoffset(self, dt):
        return dt.timedelta(hours=-5)

    def dst(self, dt):
        return dt.timedelta(0)

# date_start and date_end are type datetime.date
def get_days_from_daterange(date_start,date_end):
    days = date_end - date_start
    return days

def get_datetime_from_past(seconds_to_subtract,datetime_start_date=False):
    seconds = dt.timedelta(seconds=seconds_to_subtract)
    #seconds.seconds = seconds_to_subtract
    if not datetime_start_date:
        now = dt.datetime.now(tz=EST())
    return now - seconds

def get_google_data(symbol, period_in_seconds, number_of_days_behind_today):
    url_root = 'http://www.google.com/finance/getprices?i='
    url_root += str(period_in_seconds) + '&p=' + str(number_of_days_behind_today)
    url_root += 'd&f=d,o,h,l,c,v&df=cpct&q=' + symbol
    print(url_root)
    #response = urllib3.urlopen(url_root)
    http = urllib3.PoolManager()
    response = http.request(method='GET',url=url_root)

    #data = response.read().split('\n')
    data = str(response.data).split('\\')

    for i,entry in enumerate(data[8:len(data)]):
        data[i+7] = str(entry).split(',')
        # data[i+7][1] = str(get_datetime_from_past(len(data[7:])*period_in_seconds))
    return data

def get_market_opening_time(google_finance_data):
    openingminutes = google_finance_data[1][str(google_finance_data[2]).find("="):]
    tdelta = dt.timedelta(minutes=int(openingminutes))
    # print(openingminutes[1:]) # debug
    #openingtime = dt.time() + tdelta
    openingtime = dt.datetime.combine(dt.date(1,1,1),dt.time()) + tdelta # http://stackoverflow.com/a/12448721/2394499
    return openingtime.time()

def get_market_closing_time(google_finance_data):
    closingminutes = google_finance_data[2][str(google_finance_data[2]).find("="):]
    tdelta = dt.timedelta(minutes=int(closingminutes[1:]))
    # print(closingminutes[1:]) # debug
    #closingtime = dt.time() + tdelta
    closingtime = dt.datetime.combine(dt.date(1,1,1),dt.time()) + tdelta # http://stackoverflow.com/a/12448721/2394499
    return closingtime.time()

#this includes market times!
def generate_chart_interval_datetimes(start_datetime:dt.datetime,end_datetime:dt.datetime,interval_seconds:int):
    values = []
    marketopen = get_market_opening_time(get_google_data('ZVZZT',interval_seconds,1))
    marketclosed = get_market_closing_time(get_google_data('ZVZZT',interval_seconds,1))

    start_datetime.combine(date=start_datetime.date(),time=marketopen)

    market_duration = dt.datetime.combine(dt.datetime.today(),marketclosed) - dt.datetime.combine(dt.datetime.today(),marketopen)
    input_days_difference = end_datetime.day - start_datetime.day
    market_trading_seconds_per_day = market_duration.total_seconds()
    input_trading_day_seconds = input_days_difference * market_trading_seconds_per_day
    input_hours_difference = end_datetime.hour - start_datetime.hour
    input_hours_seconds = input_hours_difference * 3600
    input_minutes_difference = end_datetime.minute - start_datetime.minute
    input_minutes_seconds = input_minutes_difference * 60
    input_seconds_difference = end_datetime.second - start_datetime.second
    total_seconds = input_trading_day_seconds + input_hours_seconds + input_minutes_seconds + input_seconds_difference

    total_intervals = total_seconds // interval_seconds
    print(total_intervals)
    for i in range(0,int(total_intervals)):

        amount_to_add = dt.timedelta(hours=marketopen.hour,minutes=marketopen.minute) + dt.timedelta(seconds=interval_seconds)*i
        basevalue = start_datetime + amount_to_add
        value = basevalue
        print(value.time())
        print(marketclosed)
        print(value.time() > marketclosed)
        print(value.date())
        print(value.date().weekday())
        if value.time() > marketclosed:  # advance to next day
            value + dt.timedelta(days=1)
            value.combine(value.date(),marketopen)
        if value.weekday() == 6: # in case its a sunday
            value + dt.timedelta(days=2)
            value.combine(value.date(),marketopen)
        if value.weekday() == 7: # in case its a saturday
            value + dt.timedelta(days=1)
            value.combine(value.date(),marketopen)
        values.append(value)

    print(marketclosed)
    return values






def modes(list_of_numbers):
    sample = list_of_numbers
    modes_dict = {}
    for item in sample:
        if item in modes_dict.keys():
            modes_dict[item] += 1
        else:
            modes_dict.item = 0
    return modes_dict

def sort_dict(a_dictionary):
    sort = sorted(a_dictionary.values())
    return sort

date_start = dt.date(2016,3,12)
date_end = dt.date.today()

 #print(get_days_from_daterange(date_start,date_end))

print(get_google_data('AMD',300,7))

print(get_market_opening_time(get_google_data('AMD',300,7)))

print(get_market_closing_time(get_google_data('AMD',300,7)))

print(generate_chart_interval_datetimes(dt.datetime(2016,3,12),dt.datetime(2016,3,19),300))

print(dt.datetime.now().isoweekday())