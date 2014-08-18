csv-server
==========

A small Python web app (using Flask) that serves a CSV file for
simple querying (using Pandas and pandas.DataFrame.query()). The
app consists of a single web page with a query input field, query
button and the query results (# rows returned and the data in a
table).

Usage:

./csv_server.py [--debug] <csv_file>

Notes:

This is a very rough implementation that, while meeting the
requirements, could be improved dramatically in a number of
areas:

1) Memory Utilization

The application loads the entire data set into memory. While
this isn't a problem when there are only 1,000 records, it
could easily be a problem if we were working with large data
sets (especially if the application is running on a server
with multiple processes/threads). Depending on the size of
the file, a buffering strategy where query result frames and
counts are combined and summed respectively.

2) UX

Right now, the only useful message generated for bad queries
is "Column X doesn't exist in the dataset". Otherwise, the
user only gets a message that the query syntax is invalid.
For a complex query with a small typo, it would be useful
to provide more helpful feedback.

There's also no indication of what values are extant for
the respective columns (e.g. there may be a small set of 
values for personal status like "female div/dep/mar"), but
the user wouldn't know what they are without performing an
entirely separate analysis of the data. Other fields have
such a large range of values that identifying a common set
of values wouldn't make sense. The ability to enumerate
fields and delineate which ones have common values would
make the application more useful.

We also see cases where there are ranges (e.g. "1<=X<4").
If a single numeric value is supplied in the querystring
for that particular column, we might be able to modify the
query such that the correct set of records are return.

There's also the issue of the layout. There's currently
no functionality in place to select the subset of columns
a user actually cares about. Nor is there a limit to the
number of rows (or a facility for the user to select the
number of rows) that could be used in conjunction with
pagination. The result is a potentially massive table
table that bleads way out to the right of the page.

An export utility would be nice too.

3) Performance

For large data sets, indices would make searching the
dataframe much more efficient. This is challenging
because we don't know what queries a user wants to run
until they actually submit them. If a large number of
queries are run with the same columns, there may be
an opportunity to generate indices dynamically.
