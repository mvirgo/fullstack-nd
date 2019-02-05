#!/usr/bin/env python3

'''
Connects to a database made from newsdata.sql, and returns:
1) What are the most popular three articles of all time?
2) Who are the most popular article authors of all time?
3) On which days did more than 1% of requests lead to errors?
'''

import psycopg2


def execute_query(c, query):
    '''
    Executes the given SQL query, and returns the output.
    Input: Database cursor, SQL query
    Output: Query results
    '''
    c.execute(query)
    data = c.fetchall()

    return data


def top_three_articles(c):
    '''
    Query and response to the most popular three articles of all time.
    Input: Database cursor
    '''
    query = ("SELECT a.title, count(l.*) as read_count "
             "FROM log l "
             "JOIN articles a "
             "ON l.path = CONCAT('/article/', a.slug) "
             "GROUP BY a.title "
             "ORDER BY read_count DESC "
             "LIMIT 3;")
    print("Executing query for top three all-time articles...\n")
    results = execute_query(c, query)
    print("The three most popular articles of all time are:")
    for i in range(len(results)):
        print(results[i][0], '--', results[i][1], 'views')
    print('\n')


def popular_authors(c):
    '''
    Query and response to the most popular authors of all time.
    Input: Database cursor
    '''
    query = ("SELECT au.name, COUNT(l.path) as read_count "
             "FROM authors au "
             "JOIN articles ar "
             "ON au.id = ar.author "
             "JOIN log l "
             "ON l.path = CONCAT('/article/', ar.slug) "
             "GROUP BY au.name "
             "ORDER BY read_count DESC;")
    print("Executing query for most popular authors...\n")
    results = execute_query(c, query)
    print("The most popular authors of all time are:")
    for i in range(len(results)):
        print(results[i][0], '--', results[i][1], 'views')
    print('\n')


def high_error_days(c):
    '''
    Query and response to the days with over 1% of requests returning errors.
    Input: Database cursor
    '''
    query = ("WITH failure AS (SELECT time::date as day, "
             "COUNT(status) AS fails "
             "FROM log "
             "WHERE status = '404 NOT FOUND' "
             "GROUP BY day), "
             "request AS (SELECT time::date as day, "
             "COUNT(status) AS requests "
             "FROM log "
             "GROUP BY day) "
             "SELECT f.day, f.fails / r.requests::float AS fail_rate "
             "FROM failure f "
             "JOIN request r "
             "ON f.day = r.day "
             "WHERE f.fails / r.requests::float > 0.01; ")
    print("Executing query for days with >1% failures on requests...\n")
    results = execute_query(c, query)
    print("Days on which more than 1% of requests returned errors are:")
    for i in range(len(results)):
        print(results[i][0], '--', '%.2f%%' % results[i][1], 'errors')
    print('\n')


def main():
    # Connect to database
    try:
        db = psycopg2.connect("dbname=news")
    except psycopg2.Error:
        print("Unable to connect to the database.")
    # Grab cursor
    c = db.cursor()
    # Run each query and print results
    top_three_articles(c)
    popular_authors(c)
    high_error_days(c)
    # Close database
    db.close()

if __name__ == "__main__":
    main()
