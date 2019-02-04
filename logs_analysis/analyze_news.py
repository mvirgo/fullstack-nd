#!/usr/bin/python

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
    query = ("SELECT path, count(*) as read_count "
             "FROM log "
             "WHERE path LIKE '%article%' "
             "GROUP BY path "
             "ORDER BY read_count DESC "
             "LIMIT 3;")
    results = execute_query(c, query)
    print("The three most popular articles of all time are:\n")
    print(results)


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
             "ON l.path LIKE CONCAT('%', ar.slug, '%') "
             "GROUP BY au.name "
             "ORDER BY read_count DESC;")
    results = execute_query(c, query)
    print("The most popular authors of all time are:\n")
    print(results)


def high_error_days(c):
    '''
    Query and response to the days with over 1% of requests returning errors.
    Input: Database cursor
    '''
    query = ("SELECT * "
             "FROM authors ")
    results = execute_query(c, query)
    print("Days on which more than 1% of requests returned errors are:\n")
    print(results)


def main():
    # Connect to database
    db = psycopg2.connect("dbname=news")
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
