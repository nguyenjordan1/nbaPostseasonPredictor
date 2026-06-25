# nbaPostseasonPredictor

To run the application check to see if the data.db is is there. If the tables are not looking correct delete the database and recollect the data. This could also be helpful to do if the season is still going on an the games are still updating. 

1. Check database
1b. if need to delete database: delete and do python -m app.run to recollect data 

2. To analyze do python -m app.analyzer

For the application I decided to go with modular architecture. I have separated the responsibilities across different components. Data Collection, analytics, metrics tracking, and web routes. These four components should satisfy all of the requirements for the rubric. This separation allows for maintainability and makes the code easier to understand. With modularity I am also able to test different parts of my system without affecting the rest of the system. 

I decided to go with SQLite because the database isn't too large and it doesn't require server setup which makes it easy and the best option for this project. I have 2 tables, one for teams and one for games. This design also allows for efficient querying and supports future expansion if additional statistics or entities need to be stored.

For the data collection I have decided to webscrape ESPN with Requests and BeautifulSoup. I have two collector modules that separately collect teams and a separate that collects games. Separating these two improves maintainability and if there are any changes makes it easy to update independently. Because the team names are represented differently across various ESPN pages, normalization dictionaries are used to standardize team names before storing. For the Analytics the design is to independently calculate operations directly on stored database data. Things such as home vs away win percentage, conference comparisons, team ranking, and average point differential each focus on a single responsibility. 

I use Rest style API endpoints that return JSON data. THis separates the presentation layer from the analytics layer. The frontend uses a simple HtML template combined with JavaScript fetch requests to dynamically load analytics from the API endpoints. 

The last few things that I have are metrics and testing. Metrics are used to track operational statistics like number requests, team loaded, and games loaded. The last thing is unit tests which use Pytest and Flask’s test client to validate application behavior.

