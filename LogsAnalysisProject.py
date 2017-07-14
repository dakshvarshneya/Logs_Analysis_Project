#!/usr/bin/env python2.7


import psycopg2


DBNAME = "news"

question1 = """
    SELECT title,count(*)
    As views
    FROM articles,log
    WHERE log.path = CONCAT('/article/', articles.slug)
    GROUP BY title
    ORDER BY views
    Desc lIMIT 3;"""

question2 = """
    SELECT authors.name
    AS author,
    count(articles.author)
    AS views
    FROM articles,authors,log
    WHERE authors.id = articles.author
    AND log.path = CONCAT('/article/', articles.slug)
    GROUP BY authors.name
    ORDER BY views;"""

question3 = """
    SELECT date, ROUND((visits.error * 1.0/logs)*100, 2)
    AS percent
    FROM (SELECT date(time),
    COUNT(CASE WHEN status='404 NOT FOUND' THEN 1 ELSE NULL END)
    AS error, COUNT(*) AS logs FROM log
    GROUP BY date(time)) AS visits
    WHERE ((error * 1.0/ Logs)*100) > 1"""


def popular_article():

    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(question1)
    print "\n" + "3 most popular articles of all time:" + "\n" + "-" * 50
    for content in c:
        print(' ' + content[0] + '- ' + str(content[1]) + " views")
    db.close()


def popular_author():

    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(question2)
    print "\n" + "Most popular article authors of all time:" + "\n" + "-" * 50
    for content in c:
        print(' ' + content[0] + '- ' + str(content[1]) + " views")
    db.close()


def error():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(question3)
    print "\n" + "Days with more than 1% of errors:" + "\n" + "-" * 50
    for content in c:
        print('    ' + str(content[0]) + ' - ' + str(content[1]) + '% ' +
              'errors')
    db.close()


popular_article()
popular_author()
error()
