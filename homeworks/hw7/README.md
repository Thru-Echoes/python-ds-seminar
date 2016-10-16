# Flask based Python Web App

Creating a Flask based Python stack for frontend request to backend responses as SQL queries.

## Project Structure

Move into the **ex-server** directory to run this example server using *Bootstrap* (HTML framework) with *Flask* (Python server framework).

* **exApp.py** - Initializes localhost using three core libraries (see below).

```
    # exApp.py core libraries
    #
    # wsgiref : WSGI server, bare bones Python
    # werkzeug : upgrade server with code reloading + interactivity
    # cherrpy : next level server - for production deployment

```

* **exApp.py**, cont. - this file is directly using Flask to run the server and interact / communicate between client (i.e. user in the front = browser) and the server (i.e. backend, routes to each web page). In other words, every web page has a respective function in this file that renders / re-directs the URL to that page's HTML - each HTML page is within the *templates/ directory*

* **static/** - this directory contains utility, mainly non-Python files, *e.g. CSS, Javascript, etc*

* **templates/** - this directory contains each page's HTML file

Note: there is a general layout page, located **templates/layout.html**, that is used to build the other web pages. I.e. other web pages simply augment HTML fields / data to the core layout HTML page.

## To Run

Run this command line by simply executing the **exApp.py** server file and then opening up a browser at the localhost port:

```
    python exApp.py

    # listening on localhost:8888...
```
