from flask import Flask, render_template
import csv
from collections import OrderedDict

app = Flask(__name__)

metro_districts = ["State Representative District 30A", "State Representative District 31A", "State Representative District 31B", "State Representative District 32B", "State Representative District 29B", "State Representative District 30B", "State Representative District 35A", "State Representative District 35B", "State Representative District 39A", "State Representative District 34A", "State Representative District 29A", "State Representative District 36A", "State Representative District 37A", "State Representative District 37B", "State Representative District 38A", "State Representative District 33A", "State Representative District 44A", "State Representative District 34B", "State Representative District 45A", "State Representative District 40A", "State Representative District 36B", "State Representative District 40B", "State Representative District 41A", "State Representative District 41B", "State Representative District 42A", "State Representative District 38B", "State Representative District 42B", "State Representative District 39B", "State Representative District 43B", "State Representative District 59A", "State Representative District 59B", "State Representative District 45B", "State Representative District 60A", "State Representative District 61A", "State Representative District 60B", "State Representative District 62A", "State Representative District 62B", "State Representative District 63A", "State Representative District 61B", "State Representative District 49A", "State Representative District 49B", "State Representative District 44B", "State Representative District 48A", "State Representative District 33B", "State Representative District 63B", "State Representative District 50A", "State Representative District 50B", "State Representative District 48B", "State Representative District 47B", "State Representative District 51A", "State Representative District 51B", "State Representative District 52A", "State Representative District 52B", "State Representative District 64B", "State Representative District 65B", "State Representative District 65A", "State Representative District 64A", "State Representative District 66B", "State Representative District 66A", "State Representative District 43A", "State Representative District 67A", "State Representative District 67B", "State Representative District 53A", "State Representative District 53B", "State Representative District 54A", "State Representative District 54B", "State Representative District 46A", "State Representative District 46B", "State Representative District 15B", "State Representative District 58A", "State Representative District 58B", "State Representative District 47A", "State Representative District 55A", "State Representative District 55B", "State Representative District 57A", "State Representative District 57B", "State Representative District 56A", "State Representative District 56B", "State Representative District 32A", "State Senator District 15", "State Senator District 29", "State Senator District 30", "State Senator District 31", "State Senator District 32", "State Senator District 33", "State Senator District 34", "State Senator District 35", "State Senator District 36", "State Senator District 37", "State Senator District 38", "State Senator District 39", "State Senator District 40", "State Senator District 41", "State Senator District 42", "State Senator District 43", "State Senator District 44", "State Senator District 45", "State Senator District 46", "State Senator District 47", "State Senator District 48", "State Senator District 49", "State Senator District 50", "State Senator District 51", "State Senator District 52", "State Senator District 53", "State Senator District 54", "State Senator District 55", "State Senator District 56", "State Senator District 57", "State Senator District 58", "State Senator District 59", "State Senator District 60", "State Senator District 61", "State Senator District 62", "State Senator District 63", "State Senator District 64", "State Senator District 65", "State Senator District 66", "State Senator District 67"]

def incumbent_data():
    incumbents = {}
    #senate
    with open("data/senate-incumbents.csv", "r") as f:
        reader = csv.reader(f, delimiter=",")
        for row in reader:
            district = "State Senator District " + row[0]
            name = row[1]
            year_elected = row[3]
            party = row[2][0]

            incumbents[district] = {"name": name, "year_elected": year_elected, "party": party}

    #house
    with open("data/house-incumbents.csv", "r") as f:
        reader = csv.reader(f, delimiter=",")
        for row in reader:
            district = "State Representative District " + row[0]
            name = row[1]
            year_elected = row[3]
            party = row[2][0]

            incumbents[district] = {"name": name, "year_elected": year_elected, "party": party}

    return incumbents

def prev_election_data():

    election_results = {}

    #senate results
    with open('data/2012_statesenateresults.csv', 'r') as f:
        reader = csv.reader(f, delimiter=";")
        for row in reader:
            district = row[4]
            name = row[7].title()
            party = row[10]
            percentage = row[14]

            inserted = False

            if district in election_results:
                for i in range(0, len(election_results[district])):
                    if float(percentage) > float(election_results[district][i]["percentage"]):
                        election_results[district].insert(i, {"name": name, "party": party, "percentage": percentage})
                        inserted = True
                        break
                if not inserted:
                    election_results[district].append({
                                                        "name": name,
                                                        "party": party,
                                                        "percentage": percentage
                                                    })
            else:
                election_results[district] = [{
                                                "name": name,
                                                "party": party,
                                                "percentage": percentage
                                              }]

    #house results
    with open('data/2014_houseelectionresults.csv', 'r') as f:
        reader = csv.reader(f, delimiter=";")
        for row in reader:
            district = row[4]
            name = row[7].title()
            party = row[10]
            percentage = row[14]

            inserted = False

            if district in election_results:
                for i in range(0, len(election_results[district])):
                    if float(percentage) > float(election_results[district][i]["percentage"]):
                        election_results[district].insert(i, {"name": name, "party": party, "percentage": percentage})
                        inserted = True
                        break
                if not inserted:
                    election_results[district].append({
                                                        "name": name,
                                                        "party": party,
                                                        "percentage": percentage
                                                    })
            else:
                election_results[district] = [{
                                                "name": name,
                                                "party": party,
                                                "percentage": percentage
                                             }]

    #2012 pres results
    election_results['prez'] = {}
    with open('data/2012-pres-by-HD.csv','r') as f:
        reader = csv.reader(f)
        next(reader) #skip header
        for row in reader:
            district = row[0]
            if district[0] == "0": #leading 0s are bad
                district = district[1:]
            title = "State Representative District " + district
            election_results['prez'][title] = {
                                                'romney': int(float(row[4])*10000)/100,
                                                'obama': int(float(row[5])*10000)/100
                                                }
    with open('data/2012-pres-by-SD.csv','r') as f:
        reader = csv.reader(f)
        next(reader) #skip header
        for row in reader:
            district = row[0]
            if district[0] == "0": #leading 0s are bad
                district = district[1:]
            title = "State Senator District " + district
            election_results['prez'][title] = {
                                                'romney': int(float(row[4])*10000)/100,
                                                'obama': int(float(row[5])*10000)/100
                                                }

    return election_results

def primary_results():
    primary_winners = {}
    #House winners
    with open('data/2016-primary-state-representative.csv','r') as f:
        results = csv.reader(f, delimiter=";")

        for row in results:
            title = row[4]
            party = row[10]
            candidate = row[7]
            percent = row[14]

            if title in primary_winners:
                if party in primary_winners[title]:
                    if float(percent) > float(primary_winners[title][party]['percent']):
                        primary_winners[title][party] = {'candidate': candidate, 'percent': percent}
                else:
                    primary_winners[title][party] = {'candidate': candidate, 'percent': percent}
            else:
                primary_winners[title] = {party: {'candidate': candidate, 'percent': percent}}

    #senate winners
    with open('data/2016-primary-state-senate.csv','r') as f:
        results = csv.reader(f, delimiter=";")

        for row in results:
            title = row[4]
            party = row[10]
            candidate = row[7]
            percent = row[14]

            if title in primary_winners:
                if party in primary_winners[title]:
                    if float(percent) > float(primary_winners[title][party]['percent']):
                        primary_winners[title][party] = {'candidate': candidate, 'percent': percent}
                else:
                    primary_winners[title][party] = {'candidate': candidate, 'percent': percent}
            else:
                primary_winners[title] = {party: {'candidate': candidate, 'percent': percent}}

    simple_winners = {}

    for race in primary_winners:
        simple_winners[race] = []
        for party in primary_winners[race]:
            simple_winners[race].append(primary_winners[race][party]['candidate'])

    return simple_winners

def candidate_data():

    elections = OrderedDict()

    with open('data/CF_FedStateCounty.csv', 'r') as f:
        reader = csv.reader(f, delimiter=";", quotechar='"')

        for row in reader:
            district = row[3]
            candidate = row[1]
            candidate_party = row[5]

            if district in elections:
                first_party = elections[district][0][1]
                if candidate_party == first_party:
                    elections[district].insert(0, [candidate, candidate_party])
                else:
                    elections[district].append([candidate, candidate_party])
            else:
                elections[district] = [[candidate, candidate_party]]

    return elections

def map_url(election_title):
    if "State Representative" in election_title:
        district = election_title[30:]
        if len(district) == 2:
            district = "0" + district
        url = "http://www.gis.leg.mn/redist2010/Legislative/L2012/maps/house/" + district + ".pdf"
    else:
        district = election_title[23:]
        if len(district) == 1:
            district = "0" + district
        url = "http://www.gis.leg.mn/redist2010/Legislative/L2012/maps/senate/" + district + ".pdf"

    return url

def demographic_data():
    district_demographics = {}

    with open('data/demographic-SDs.csv','r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            district = row['DISTRICT']
            title = "State Senator District " + district

            district_demographics[title] = {
                                                "med_age": row['med_age'],
                                                "med_inc": '{:,}'.format(int(row['med_income'])),
                                                "pct_wht": int(float(row['pct_white'])*100)
                                             }

    with open('data/demographic-HDs.csv','r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            district = row['DISTRICT']
            if district[0] == "0":
                district = district[1:]
            title = "State Representative District " + district

            district_demographics[title] = {
                                                "med_age": row['med_age'],
                                                "med_inc": '{:,}'.format(int(row['med_income'])),
                                                "pct_wht": int(float(row['pct_white'])*100)
                                            }
    return district_demographics

def featured_blurbs():
    blurbs = {}
    with open('data/district-blurbs.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            blurbs[row[0]] = row[1]
    return blurbs

def formatted_elections(elections):

    f_elections = []

    election_data = prev_election_data()
    demo_data = demographic_data()
    blurbs = featured_blurbs()
    incumbents = incumbent_data()
    primary_winners = primary_results()

    for election in elections:
        title = election
        candidates = elections[election]

        #look for primary winners IF there was a primary
        if title in primary_winners:
            final_candidates = []
            for candidate in candidates:
                if candidate[0] in primary_winners[title]:
                    final_candidates.append(candidate)
            candidates = final_candidates

        classes = ""

        if len(candidates) == 1:
            classes += " uncontested"

        parties = [candidate[1] for candidate in candidates]
        dflers = parties.count("DFL")
        if dflers > 1:
            classes += " dfl-primary"
        gopers = parties.count("R")
        if gopers > 1:
            classes += " gop-primary"

        if title in metro_districts:
            classes += " metro"
        else:
            classes += " greatermn"

        if "State Senator" in title:
            classes += " senate"
        if "State Representative" in title:
            classes += " house"

        if title in blurbs:
            classes += " featured"

        #incumbent handling
        if title in incumbents:
            incumbent_name = incumbents[title]["name"]
            incumbent_year_elected = incumbents[title]["year_elected"]

            if incumbents[title]["party"] == "D":
                classes += " dfl-control"
            if incumbents[title]["party"] == "R":
                classes += " gop-control"

            incumbent_running = False

            for i in range(0, len(candidates)):
                if candidates[i][0] == incumbent_name:
                    incumbent_candidate = candidates.pop(i)
                    incumbent_candidate.append(incumbent_year_elected)
                    incumbent_running = True
                    break

            if not incumbent_running:
                incumbent_candidate = ["Open seat","",""]
                classes += " open-seat"



        #previous elections
        if "State Senator" in title:
            last_election_year = "2012"
        else:
            last_election_year = "2014"

        last_election_results = election_data.get(title) #for this election

        related_election_results = [] #for 2 HDs in SD or 1 SD in HD
        if "State Senator" in title:
            district = title[23:]
            for letter in ["A","B"]:
                related_district_title = "State Representative District " + district +letter
                related_district_result = election_data.get(related_district_title)
                related_election_results.append({'title':related_district_title.replace('Representative', 'House'),
                                                 'year': '2014',
                                                 'result': related_district_result})
        if "State Representative" in title:
            district = title[29:].lower()
            related_district_title = "State Senator District" + district[0:-1]
            related_district_result = election_data.get(related_district_title)
            related_election_results.append({'title':related_district_title.replace('Senator', 'Senate'),
                                             'year': '2012',
                                             'result': related_district_result})


        prez_results = election_data['prez'].get(title) #2012 presidential result
        if prez_results:
            if float(prez_results['romney']) > (prez_results['obama']):
                classes += " romney-won"
            if float(prez_results['obama']) > (prez_results['romney']):
                classes += " obama-won"

        #filtering to Lege elections
        if "State Senator" in title or "State Representative" in title:
            f_elections.append({
                                    "title": title.replace('Representative', 'House').replace('Senator', 'Senate'),
                                    "district": district.strip(),
                                    "map_url": map_url(title),
                                    "incumbent": incumbent_candidate,
                                    "candidates": candidates,
                                    "classes": classes,
                                    "blurb": blurbs.get(title),
                                    "demographics": demo_data.get(title),
                                    "last_election_year": last_election_year,
                                    "last_election_results": last_election_results,
                                    "related_election_results": related_election_results,
                                    "prez_results": prez_results
                                })


    return f_elections

@app.route("/")
def main_view():
    template = "index.html"
    return render_template(template, contests = formatted_elections(candidate_data()))

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
