#!usr/bin/python

import requests
import argparse
import datetime
import json

parser = argparse.ArgumentParser()
time = datetime.datetime.now()

parser.add_argument("-c", "--commit", help="Search commit in github", action='store_true')
parser.add_argument("-n", "--name", help="Choose username in github", action='store', type=str)
parser.add_argument("-r", "--repository", help="Choose repository in github", action='store',type=str)

args = parser.parse_args()
if args.name:
    if args.repository:
        if args.commit:
            name = args.name
            repository = args.repository
                
            req = requests.get("https://api.github.com/repos/{0}/{1}/commits".format(name, repository))

            if not req.status_code == 404:
                f = open("content.json","r+")
                f.write(str(req.text))
                f.truncate()
                f.close()

                with open("content.json") as json_data:
                    data = json.load(json_data)

                print("You can find this repository on github:\nhttps://github.com/{0}/{1}.git\n\nAll commits:".format(name, repository))

                i=0
                for commit in data:
                    i+=1

                    committers = commit["commit"]["author"]["name"]
                    message = commit["commit"]["message"]
                    date_get = commit["commit"]["author"]["date"][:-1]
                    date = date_get.split('T')
                    convert = date[0].split('-')
                    year = int(convert[0])
                    actual_year = int(time.year)
                    year_send = actual_year - year
                    month = int(convert[1])
                    actual_month = int(time.month)
                    month_send = actual_month - month

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

                    print("{0}.".format(i), message, "- published", res_date, "by", committers)

                print("\nWe found {0} commits in {1} repository of {2}".format(i, repository, name))

            else:
                print('You must used an username and a repository valid')
