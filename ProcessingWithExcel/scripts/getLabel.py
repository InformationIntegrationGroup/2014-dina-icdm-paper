import time
from pytz import timezone
import datetime
import csv

def getEpochTimestamp(datetimeString):
    india =  timezone('UTC')
    _time_struct = datetime.datetime.strptime(datetimeString, '%Y-%m-%d %H:%M:%S') - datetime.timedelta(hours=5, minutes=30)
    return (_time_struct - datetime.datetime(1970,1,1)).total_seconds()

def getEpoch(datetimeString):
    india =  timezone('UTC')
    _time_struct = datetime.datetime.strptime(datetimeString, '%Y-%m-%d %H:%M:%S') - datetime.timedelta(hours=5, minutes=30)
    time_epoch = (_time_struct - datetime.datetime(1970,1,1)).total_seconds()
    timeDiff = datetime.datetime.fromtimestamp(time_epoch ,india)
    return timeDiff

def generateLabels(ts):
    india =  timezone('UTC')
    data = [{
            "datetimeFrom": "2013-12-24 12:47:00",
            "datetimeTo": "2013-12-24 13:02:00",
            "mode": "walking"
        }, {
            "datetimeFrom": "2013-12-24 13:05:00",
            "datetimeTo": "2013-12-24 13:20:00",
            "mode": "auto"
        }, {
            "datetimeFrom": "2013-12-24 13:22:00",
            "datetimeTo": "2013-12-24 13:37:00",
            "mode": "bus"
        }, {
            "datetimeFrom": "2013-12-24 14:16:00",
            "datetimeTo": "2013-12-24 14:32:00",
            "mode": "stationary"
        }, {
            "datetimeFrom": "2013-12-25 16:31:00",
            "datetimeTo": "2013-12-25 16:46:00",
            "mode": "walking"
        }, {
            "datetimeFrom": "2013-12-25 16:55:00",
            "datetimeTo": "2013-12-25 17:10:00",
            "mode": "auto"
        }, {
            "datetimeFrom": "2013-12-25 17:18:00",
            "datetimeTo": "2013-12-25 17:33:00",
            "mode": "bus"
        }, {
            "datetimeFrom": "2013-12-25 17:49:00",
            "datetimeTo": "2013-12-25 18:05:00",
            "mode": "stationary"
        }, {
            "datetimeFrom": "2013-12-26 16:58:00",
            "datetimeTo": "2013-12-26 17:13:00",
            "mode": "walking"
        }, {
            "datetimeFrom": "2013-12-26 17:22:00",
            "datetimeTo": "2013-12-26 17:37:00",
            "mode": "auto"
        }, {
            "datetimeFrom": "2013-12-26 17:47:00",
            "datetimeTo": "2013-12-26 18:02:00",
            "mode": "bus"
        }, {
            "datetimeFrom": "2013-12-26 18:33:00",
            "datetimeTo": "2013-12-26 18:48:00",
            "mode": "stationary"
        }]

    ip = int(float(ts))
    label = 'NA'
    for i in data:
        mid_time = datetime.datetime.fromtimestamp(ip ,india)

        start_time = getEpoch(i['datetimeFrom'])
        end_time = getEpoch(i['datetimeTo'])
        # print start_time.strftime('%Y-%m-%d %H:%M:%S %Z%z'),'\t',mid_time.strftime('%Y-%m-%d %H:%M:%S %Z%z'),'\t',end_time.strftime('%Y-%m-%d %H:%M:%S %Z%z')


        if mid_time >= start_time and mid_time <= end_time:
            label = i['mode']
            print start_time.strftime('%Y-%m-%d %H:%M:%S %Z%z'),'\t',mid_time.strftime('%Y-%m-%d %H:%M:%S %Z%z'),'\t',end_time.strftime('%Y-%m-%d %H:%M:%S %Z%z')
        # else:
        #     print ip - getEpochTimestamp(i['datetimeFrom'])
        #     print getEpochTimestamp(i['datetimeTo']) - ip

            #break        
    return label

ts_index = 0
fName = 'forLabeling.csv'
# fName = '/Users/shri/devel/huawei/karma-svm-service/invoking_the_mode_of_transport/RawData/Day1/AccelerometerSensorProbe.csv'
# fName = '/Users/shri/devel/huawei/karma-svm-service/invoking_the_mode_of_transport/RawData/page1.csv'
fOut = 'ExtractedAccDFTwithLabels.csv'
f1 = open(fName)
f2 = open(fOut, 'w+')

contents = csv.reader(f1, delimiter=',')
first = True
headers = []
results = []
for row in contents:
    if first:  
        items = len(row)        
        print row      
        for i in range(0,items):
            if row[i].strip() == 'timestamp':
                print 'timestamp index is : ',ts_index
                break
            else:
                ts_index = ts_index + 1

        first = False
        headers = row
        headers.append('mode')
        # print headers
        f2.write(','.join(headers) + '\n')
        continue

    lbl = generateLabels(row[ts_index])
    row.append(lbl)
    # print row
    f2.write(','.join(row) + '\n')

f2.close()