# Full-Stack Happiness
A near-full stack data analytics project involving AWS, SQL, Python, and Tableau. Involves ingesting OECD data from 2021 of various countries, government trust data, and country abbreviation of countries data.

## IMPORTANT NOTE:
In `main.py`, there is a reference to `config.py` (aliased as "c"). This `config.py` contains details of the AWS instance: the name of the server, password, and others. Since I do not want the table or the instance to be altered, I decided to redact them.  

The variables are used in the `connect_db` function in `main.py`: `c.HOST_NAME`,`c.DBNAME`, `c.PORT`, `c.USERNAME`, `c.PASSWORD`. 
All of them have been changed to a series of hashtags (#) in the `config.py` file

## Tableau Link
Check out the Tableau viz here: https://public.tableau.com/views/country_happiness_16652571153560/Main?:language=en-US&:display_couant=n&:origin=viz_share_link

# Original datasets

https://stats.oecd.org/index.aspx?DataSetCode=BLI
