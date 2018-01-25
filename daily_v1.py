#!/usr/bin/env python

import cgi
import cgitb
import json


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
      google.load("visualization", "1", {packages:["corechart"]});
      google.setOnLoadCallback(drawChart);
      function drawChart() {
        var data = google.visualization.arrayToDataTable([
    ['Time', 'EMS', 'Fire'],
    %s
        ]);

        var options = {
          title: 'Incidents in the past 24 hours',
          curveType: 'function',
          hAxis: {title: 'Hour of day', titleTextStyle: {color: 'blue'}},
          vAxis: {title: 'Number of Incidents', titleTextStyle: {color: 'blue'}}
        };

        var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
        chart.draw(data, options);
      }
    </script>
    <div id="chart_div"></div>

    </body>
    """ % print_table('../hour/24HrHistory.txt', ';')

    # serve the page with the data table embedded in it
    print page_str

if __name__=="__main__":
    main()
