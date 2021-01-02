#! /usr/bin/python
import sys
import time
import datetime
import requests
import json
import subprocess

args = sys.argv

if (len(args) > 1):
  formatted_date = args[1]
else:
  formatted_date = datetime.datetime.now().strftime("%Y-%m-%d")

session = requests.Session()

with open('cookies.json') as f:
  cookie_list: list = json.load(f)
  cookie_jar = requests.cookies.RequestsCookieJar()

  for cookie in cookie_list:
    cookie_jar.set(cookie["name"], cookie["value"], domain=cookie["host"], path=cookie["path"], expires=cookie["expiry"], secure=True)
  session.cookies = cookie_jar

result = session.get(f'https://nyt-games-prd.appspot.com/svc/crosswords/v3/36569100/puzzles.json?publish_type=daily&date_start={formatted_date}&date_end={formatted_date}').text
id = json.loads(result)["results"][0]["puzzle_id"]

puzzle_pdf = session.get(f'https://www.nytimes.com/svc/crosswords/v2/puzzle/{id}.pdf')
puzzle = open(f'{id}.pdf', "wb")
puzzle.write(puzzle_pdf.content)
puzzle.close()

subprocess.run([f'lp {id}.pdf -d brother'], shell=True)