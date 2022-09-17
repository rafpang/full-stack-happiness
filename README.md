# Full-Stack Happiness
A full stack data analytics project involving AWS, SQL, Python, and Tableau. Involves ingesting OECD data from 2021 of various countries, government trust data, and country abbreviation of countries data.

## IMPORTANT NOTE:
In main.py, there is a reference to config.py (aliased as "c"). This config.py contains details of the AWS instance, such as the name of the server, password, and others. Since I do not want the table or the instance to be altered, I decided to redact them.  The variables are used in the connect_db function in main.py: c.HOST_NAME, c.DBNAME, c.PORT, c.USERNAME, c.PASSWORD. All of them have been changed to "REDACTED" in the config.py file
