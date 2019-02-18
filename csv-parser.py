#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Name: csv_parser.py
# Description: A python script to parse a CSV file and normalize it using the specs in README.md
# Author: Madhu Joshi (madhu.joshi@gmail.com)
# Updates: Kevin Curry (kmcurry@gmail.com)
#   * Update to Python3
#   * Change file open to a text reader expecting utf-8 and use default replacement error handler
#   * Change total duration to float format for consistency with other duration fields (reuse normalize_duration)
#   * Write output to file
#   * Include column names in output
#   * Use clearer variable names
#
# Date: 02/18/18
# Requirements / Tested on:
#       Python 3.6 on MacOS X
# Additional / non-standard Module(s) used
#       pytz (pip3 install pytz)
#
# Usage:
#        csv_parser.py sample.csv
#
# Normalized CSV file will written to the file sample-fixed.csv

from __future__ import unicode_literals
import datetime
import pytz
import csv
import sys
import re

def convert_to_iso8601(timestamp_str):
    """ This function converts a given timestamp to ISO-8601 format an TZ to US/Eastern"""
    dt = datetime.datetime.strptime(timestamp_str, "%m/%d/%y %H:%M:%S %p")
    us_pacific_tz = pytz.timezone('US/Pacific')
    us_eastern_tz = pytz.timezone('US/Eastern')
    return us_pacific_tz.localize(dt).astimezone(us_eastern_tz).isoformat()

def normalize_zipcode(zip_code):
    """ Normalize / pad zip code to ensure they are 5 digits """
    return '{0:0>5}'.format(zip_code)

def normalize_name(name):
    """ Uppercase name (assuming all caps) """
    return name.upper()

def normalize_addr(addr):
    """ The Address column should be passed through as is, except for Unicode validation. 
        Please note there are commas in the Address field; your CSV parsing will need to 
        take that into account. Commas will only be present inside a quoted string."""
    return addr

def normalize_duration(duration):
    """ Convert duration to floating seconds format """
    # Split duration in %H:%M:%S.%f format into components and convert to int so they
    # can be used as args for timedelta. re.split splits on : as well as .
    h, m, s, ms = map(int, re.split(r'[:\.]', duration))
    td = datetime.timedelta(hours=h, minutes=m, seconds=s, milliseconds=ms)
    secs = td.total_seconds()
    return float(secs)
    
def total_duration(foo_duration, bar_duration):
    """ Totals normalized Foo and Bar duration columns from the sample.csv """
    foo_td = normalize_duration(foo_duration)
    bar_td = normalize_duration(bar_duration)
    return foo_td + bar_td

def normalize_notes(note):
    """ return the notes field w/ no modification except unicode replacement """
    return note 

if __name__ == "__main__":
    """ Open the input file as text, expecting utf-8, and use the Python error default replacement handler"""
    inputFile = open(sys.argv[1], 'rt', encoding="utf-8", errors="replace")
    outputFile = open("sample-fixed.csv", "w+")
    reader = csv.reader(inputFile)
    writer = csv.writer(outputFile)
    writer.writerow(["Timestamp","Address","ZIP","FullName","FooDuration","BarDuration","TotalDuration","Notes"])
    next(reader) # Skip header / first row
    for row in reader:
        nd = convert_to_iso8601(row[0])
        na = normalize_addr(row[1])
        nz = normalize_zipcode(row[2])
        nn = normalize_name(row[3])
        d1 = normalize_duration(row[4])
        d2 = normalize_duration(row[5])
        td = total_duration(row[4], row[5])
        note = normalize_notes(row[7])
        writer.writerow([nd, na, nz, nn, d1, d2, td, note])
    outputFile.close()