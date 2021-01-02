#! /usr/local/bin/python3
import sqlite3
import json

cookie_db = "/Users/andy/Library/Application Support/Firefox/Profiles/9ypnuirw.default/cookies2.sqlite"

conn = sqlite3.connect(cookie_db)
conn.row_factory = sqlite3.Row
c = conn.cursor()
c.execute("select * from moz_cookies where host = '.nytimes.com'")
result = [dict(row) for row in c.fetchall()]

open("cookies.json", "w").write(json.dumps(result))