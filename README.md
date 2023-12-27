# sqlalchemy-challenge

In this two-part challenge, we used Python and SQLAlchemy to explore and analyze climate data. Then we created an app using Flask to return the climate data. 

To prepare the database, we created an engine to connect to the hawaii.sqlite database, reflected the tables into classes, then created a SQLAlchemy session to connect Python to the database. From there we were able to create queries, convert the returned data into Pandas dataframes, and make plots.

For the second part of the challenge, we used the queries we created in the first part to create an app using Flask. First we listed the available api routes on the 'Welcome' page. Then for each route we performed a query, converted the returned data into dictionaries, and lastly jsonified them. In addition to the queries that were already created, we created two new queries to return the min, max, and avg temperature for a specified start date or start/end date. 
