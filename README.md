# nbaPostseasonPredictor

To run the application check to see if the data.db is is there. If the tables are not looking correct delete the database and recollect the data. This could also be helpful to do of the season is still going on an the games are still updating. 

1. Check database
1b. if need to delete databse: delete and do python -m app.run to recollect data

2. preprocessing - uncomment out the analyzer.py first few functions above the cutoff and do run python -m app.analyzer make sure to comment the preprocessing functions back out
(Im tinking about just making a seperate file for it called preprocessing)
(I have now seperated the two so instead of doing this second step please move on to step 3)

3. To analyze do python -m app.analyzer