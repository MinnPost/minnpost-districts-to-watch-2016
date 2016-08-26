# MinnPost’s Legislative races to watch 2016
In 2016, all 201 seats in the Minnesota Legislature are up for election. To help
readers understand the dynamics in the election this application focuses on 10
Senate races and 15 House races that are likely to be the hardest fought and
potentially the closest this election.

For each race, we display the candidates, information about the district
and past election results.

The live story is here: [The 25 legislative races to watch in Minnesota in 2016](https://www.minnpost.com/politics-policy/2016/07/25-legislative-races-watch-minnesota-2016).

This application was based on [MinnPost’s Who’s running for the Minnesota Legislature 2016](https://github.com/MinnPost/minnpost-whos-running-2016).

##Data sources
All data used for this application comes from csvs in the `/data` directory:
 - `CF_FedStateCounty.csv`: all candidates for office, from the MN sos
 - `demographics-HDs.csv` and `demographics-SDs.csv`: Median income, median age and percent of the population that is white for each legislative district. From the U.S. Census.
 - `house-incumbents.csv` and `senate-incumbents.csv`: The name and party of current legislative incumbents
 - Past election results files:
   - `2012_statesenateresults.csv`: 2012 state Senate results
   - `2014_houseelectionresults.csv`: 2014 state House results
   - `2012-pres-by-HD.csv` and `2012-pres-by-SD`: 2012 presidential results by legislative district
 - `2016-primary-state-senate.csv` and `2016-primary-state-representative.csv`: Primary election results. Used to eliminate candidates who lost primaries from the list of candidates (primary results are not displayed)
 - `district-blurbs.csv`: Short blurbs written by Briana Bierschbach describing the races in the 25 districts to watch

##Development
It's recommended that you use a virtualenv. Additionally, the app was written in Python 3. Use something like:

`virtualenv -p python3 venv`

Activate it:

`source venv/bin/activate`

Then install the requirements:

`pip install -r requirements.txt`

This is a flask application. To run it locally, run:

`python app.py`

And point a browser toward the URL specified in the terminal output.

Generally, data processing takes place in `app.py` and layout is in
`templates/index.html`

##Deploying

This application uses Frozen Flask to save an html file that can be copied into a CMS or hosted somewhere. To build it, run:

`python deploy.py`

The file is `build/index.html`.
