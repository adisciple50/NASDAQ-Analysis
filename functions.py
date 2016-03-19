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
def generate_chart_interval_datetimes(start_datetime,end_datetime,interval_seconds):
    values = []
    marketopen = get_market_opening_time()
    marketclosed = get_market_closing_time()

    start_datetime.combine(time=marketopen)

    market_duration = marketclosed - marketopen
    input_days_difference = end_datetime.days - start_datetime.days
    market_trading_seconds_per_day = market_duration.total_seconds()
    input_trading_day_seconds = input_days_difference * market_trading_seconds_per_day
    input_hours_difference = end_datetime.hours - start_datetime.hours
    input_hours_seconds = input_hours_difference * 3600
    input_minutes_difference = end_datetime.minutes - start_datetime.minutes
    input_minutes_seconds = input_minutes_difference * 60
    input_seconds_difference = end_datetime.seconds - start_datetime.seconds
    total_seconds = input_trading_day_seconds + input_hours_seconds + input_minutes_seconds + input_seconds_difference

    total_intervals = total_seconds // interval_seconds

    for i in range(1,total_intervals):
        amount_to_add = td






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