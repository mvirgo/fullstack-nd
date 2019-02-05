# Logs Analysis Project

In this project, I wrote a python script in Python 3, `analyze_news.py`, 
to connect to a database and query certain information from within it.

The data file used, `newsdata.sql`, is too large for this repository,
but Udacity provides it [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip). 

The database used works with PostgreSQL. If you have created a PostgreSQL
database used the above `.sql` file, you will need `psycopg2` installed for
Python 3 to run the script. You can do this with `pip3 install psycopg2` 
(or just with regular `pip` if Python 3 is your default version.)

The script can be run from a command line where the database is accessible
from the same directory with `python analyze_news.py`. The script answers the
following queries as per the project instructions:

1) What are the most popular three articles of all time?
2) Who are the most popular article authors of all time?
3) On which days did more than 1% of requests lead to errors?

This is done by first connecting to the database, then grabbing the cursor
to interact with the database. Each separate query is defined in a separate
function, where the query is then fed to the `execute_query()` function,
which executes the query with the cursor, then fetches the data from the query.

After each query is fetched, the information is printed back to the terminal
with some additional formatting for ease of reading. The database is closed
after the last query is run and printed to the terminal.

You can see an example of the output in `output.txt`.

### Requirements
Install the following:
Python 3: [download here](https://www.python.org/downloads/)
Virtual Box: [download here](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1)
Vagrant: [download here](https://www.vagrantup.com/downloads.html)

Once you have the above, download the [Udacity Virtual Machine](https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip) for the project.

Next, `cd` into where the VM was downloaded, and then cd into the `vagrant` folder within it.

You'll then run `vagrant up`, which may take awhile to install everything else necessary.
Once it has loaded, run `vagrant ssh` to enter the VM.

Once in the VM, `cd /vagrant` to enter the shared directory with your own computer.
If you already downloaded the `.sql` file further above,
run `psql -d news -f newsdata.sql` to create the database. If you entered the database,
you can exit it with Ctrl+D.

You can then run `python3 analyze_news.py` to run the script.
