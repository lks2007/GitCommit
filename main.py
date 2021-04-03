#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
import argparse
import datetime
import json
import sys

def arg_management():
    """
    argument management
    
    """
    
    desc = '''github commit helper'''
    parser = argparse.ArgumentParser(description=desc)
    group = parser.add_mutually_exclusive_group()

    parser.add_argument("-c", "--commit", help="Search commit in github", action='store_true', dest='commit')
    parser.add_argument("-n", "--name", help="Choose username in github", action='store', dest='name', type=str)
    parser.add_argument("-r", "--repository", help="Choose repository in github", action='store', dest='repository', type=str)
    
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)
    
    return  parser.parse_args()

def time_management(date):
    """
    function to find when the commits done

    """
    convert = date[0].split('-')
    convert_time = date[1].split(':')
    year = int(convert[0])
    actual_year = int(time.year)
    year_send = actual_year - year
    month = int(convert[1])
    actual_month = int(time.month)
    month_send = actual_month - month
    day = int(convert[2])
    actual_day = int(time.day)
    day_send = actual_day - day
    hours = int(convert_time[0])+2
    actual_hour = int(time.hour)
    hours_send = actual_hour - hours
    minute = int(convert_time[1])
    actual_minute = int(time.minute)
    minute_send = actual_minute - minute
    
    res_date = ""
    if year_send > 0:
        if year_send > 1:
            res_date = '{} years ago'.format(year_send)  
        else:
            res_date = '{} year ago'.format(year_send)  
    elif month_send > 0:
        if month_send > 1:
            res_date = '{} months ago'.format(month_send)  
        else:
            res_date = '{} month ago'.format(month_send)           
    elif day_send > 0:
        if day_send > 1:
            res_date = '{} days ago'.format(day_send)  
        else:
            res_date = '{} day ago'.format(day_send)     
    elif hours_send > 0:
        if hours_send > 1:
            res_date = '{} hours ago'.format(hours_send)  
        else:
            res_date = '{} hour ago'.format(hours_send) 
    else:
        if minute_send > 5:
            res_date = '{} minutes ago'.format(minute_send)  
        else:
            res_date = 'just now'
    return res_date

def main():
    """
    main function
    """

    args = arg_management()
    

    if args.name and args.repository and args.commit:
        name = args.name
        repository = args.repository

        req = requests.get("https://api.github.com/repos/{0}/{1}/commits".format(name, repository))

        if not req.status_code == 404:
            data = json.loads(req.text)

            print("You can find this repository on github:\nhttps://github.com/{0}/{1}.git\n\nAll commits:".format(name, repository))

            i=0
            for commit in data:
                committers = commit["commit"]["author"]["name"]
                message = commit["commit"]["message"]
                date_get = commit["commit"]["author"]["date"][:-1]
                date = date_get.split('T')
                res_date=time_management(date)

                i+=1
                print("{0}.".format(i), message, "- published", res_date, "by", committers)


            print("\nWe found {0} commits in {1} repository of {2}".format(i, repository, name))
            sys.exit(0)
        else:
            print('You must used an username and a repository valid')
            sys.exit(1)
        
if __name__ == "__main__":
    time = datetime.datetime.now()
    main()