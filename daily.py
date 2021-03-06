#!/usr/bin/env python

import cgi
import cgitb
import json

from os import listdir
from os.path import isfile, join

#from dateutil import parser
#from datetime import timedelta
from datetime import date
from datetime import datetime

# enable tracebacks of exceptions
cgitb.enable()

# print data from a file formatted as a javascript array
# return a string containing the table
#
def print_table(filename,delimiter):
    data_lines=[]
    result=""
    timesFire = {}
    timesEms = {}
    for  x in range(0,24):
        timesFire[x] = 0
        timesEms[x] = 0
    with open(filename, "r+") as myfile:
        ids = json.load(myfile)
        for k, v in ids.items():
            #print(k)
            dt = datetime.strptime(v,"%Y-%m-%d %H:%M:%S")
            if k.startswith('E'):
                timesEms[dt.hour] = timesEms[dt.hour] + 1
            else:
                timesFire[dt.hour] = timesFire[dt.hour] + 1

        for x in range(0,23):
            result += "['"+str(x)+"', "+str(timesEms[x])+ ", " + str(timesFire[x])+"],\n"
            #result += "['"+str(x)+"', "+str(timesFire[x])+ "],\n"

        result += "['"+str(23)+"', "+str(timesEms[23])+ ", " + str(timesFire[23])+"]"
        #result += "['"+str(23)+"', "+str(timesFire[23])+ "]"



        # for line in data_lines[:-1]:
        #     x, y=line.strip('\n').split(delimiter)
        #     result += "['"+x+"', "+y+"],\n"
        # else:
        #     x, y=data_lines[-1].strip('\n').split(delimiter)
        #     result += "['"+x+"', "+y+"]"

    return result

def print_histTable():
    #get files (oldest to newest}
    onlyfiles = [f for f in listdir('../daily') if isfile(join('../daily', f))]
    #print(onlyfiles)
    result = ""

    count = 0
    for i in sorted(onlyfiles):
        with open('../daily/' + i, "r+") as myfile:
            # read dict
            dict = json.load(myfile)
            result += "['" + i[:-4] + "', " + str(dict['ems']) + ", " + str(dict['fire']) + "],\n"
        count = count + 1
        if count >= 7:
            break

    #print(result)
    result = result[:-2]
    #print(result)
        # result += "['0', 130, 30],\n"
        # result += "['1', 135, 34],\n"
        # result += "['2', 128, 29]"
    return result
# print an HTTP header
#
def printHTTPheader():
    print "Content-type: text/html"
    print ""
    print ""


def main():

    printHTTPheader()

    # this string contains the web page that will be served
    page_str="""
    <h1>Montomgery County Incident Stats</h1>

    <script type="text/javascript" src="https://www.google.com/jsapi">
</script>
    <script type="text/javascript">
      google.load("visualization", "1", {{packages:["corechart"]}});
      google.setOnLoadCallback(drawChart);
      google.setOnLoadCallback(drawDailyHistoryChart);
      function drawChart() {{
        var data = google.visualization.arrayToDataTable([
    ['Time', 'EMS', 'Fire'],
    {0}
        ]);

        var options = {{
          title: 'Incidents in the past 24 hours',
          curveType: 'function',
          hAxis: {{title: 'Hour of day', titleTextStyle: {{color: 'blue'}}}},
          vAxis: {{title: 'Number of Incidents', titleTextStyle: {{color: 'blue'}}}}
        }};

        var lineChart = new google.visualization.LineChart(document.getElementById('chart_div'));
        lineChart.draw(data, options);
      }}
      
       function drawDailyHistoryChart() {{
        var data = google.visualization.arrayToDataTable([
    ['Day', 'EMS', 'Fire'],
    {1}
        ]);

        var options = {{
          title: 'Incidents in the past several days',
          hAxis: {{title: 'Day', titleTextStyle: {{color: 'blue'}}}},
          vAxis: {{title: 'Number of Incidents', titleTextStyle: {{color: 'blue'}}}}
        }};

        var dailyCounts = new google.visualization.ColumnChart(document.getElementById('daily_hist_div'));
        dailyCounts.draw(data, options);
      }}
      
    </script>
    <div id="chart_div"></div>
    <div id="daily_hist_div"></div>

    </body>
    """.format(print_table('../hour/24HrHistory.txt', ';'), print_histTable())

    # serve the page with the data table embedded in it
    print page_str

if __name__=="__main__":
    main()
