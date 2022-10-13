'''
convert.py
Ariana Borlak
To be used with Olympic data from:
    https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results
'''

import csv

def main():
    athletes = []
    games = []
    seasons = []
    events = []
    sports = []
    NOCs = []
    results = []
    athlete_event_results = []
# "C:\Users\arian\Downloads\archive.zip"
# r"C:\Users\arian\Documents\athlete_events.csv"
    with open("athlete_events.csv") as source_file,\
            open('athletes.csv', 'w') as athletes_file,\
            open('games.csv', 'w') as games_file,\
            open('seasons.csv', 'w') as seasons_file,\
            open('events.csv', 'w') as events_file,\
            open('sports.csv', 'w') as sports_file,\
            open('NOCs.csv', 'w') as NOCs_file,\
            open('results.csv', 'w') as results_file,\
            open('athlete_event_results.csv', 'w') as athlete_event_results_file:
        reader = csv.reader(source_file)
        heading_row = next(reader)


        #looked up how to assign multiple variables to the same value here:
        #https://note.nkmk.me/en/python-multi-variables-values/
        athlete_id = game_id = season_id = event_id = sport_id = NOC_id = result_id = 0

        athletes_writer = csv.writer(athletes_file)
        games_writer = csv.writer(games_file)
        seasons_writer = csv.writer(seasons_file)
        events_writer = csv.writer(events_file)
        sports_writer = csv.writer(sports_file)
        NOCs_writer = csv.writer(NOCs_file)
        results_writer = csv.writer(results_file)
        athlete_event_results_writer = csv.writer(athlete_event_results_file)

        results = ["Gold", "Silver", "Bronze", "NA"]
        results_writer.writerow([1, "Gold"])
        results_writer.writerow([2, "Silver"])
        results_writer.writerow([3, "Bronze"])
        results_writer.writerow([4, "NA"])

        for row in reader:
            athlete_name = row[1]
            if athlete_name not in athletes:
                # athlete_name.split()
                # athlete_first_name = athlete_name[1]
                # athlete_surname = athlete_name[2:]

                athletes.append(athlete_name)
                athlete_id = len(athletes)
                athletes_writer.writerow([athlete_id, athlete_name])
                # print(athlete_id, athlete_name)
            else:
                pass

            season_name = row[10]
            if season_name not in seasons:
                seasons.append(season_name)
                season_id = len(seasons)
                seasons_writer.writerow([season_id, season_name])
            else:
                pass

            game_name = row[8]
            if game_name not in games:
                game_year = row[9]
                game_season = seasons.index(row[10]) + 1
                game_city = row[11]

                games.append(game_name)
                game_id = len(games)
                games_writer.writerow([game_id, game_year, game_season, game_city])
            else:
                pass

            sport_name = row[12]
            if sport_name not in sports:
                sports.append(sport_name)
                sport_id = len(sports)
                sports_writer.writerow([sport_id, sport_name])
            else:
                pass

            event_name = row[13]
            if event_name not in events:
                event_sport = sports.index(row[12]) + 1

                events.append(event_name)
                event_id = len(events)
                events_writer.writerow([event_id, event_sport, event_name])
            else:
                pass

            NOC_name = row[6]
            if NOC_name not in NOCs:
                NOC_abbreviation = row[7]

                NOCs.append(NOC_name)
                NOC_id = len(NOCs)
                NOCs_writer.writerow([NOC_id, NOC_abbreviation, NOC_name])
            else:
                pass

            results_name = row[14]
            if results_name not in results:
                results.append(results_name)
                results_id = len(results)
                results_writer.writerow([results_id, results_name])
            else:
                pass

            linking_athlete_id = athletes.index(row[1])
            linking_game_id = games.index(row[8])
            linking_event_id = events.index(row[13])
            linking_NOC_id = NOCs.index(row[6])
            linking_results_id = results.index(row[14])
            athlete_event_results_writer.writerow([linking_athlete_id, linking_game_id, linking_event_id, linking_NOC_id, linking_results_id])


    source_file.close()
    athletes_file.close()
    games_file.close()
    seasons_file.close()
    events_file.close()
    sports_file.close()
    NOCs_file.close()
    results_file.close()
    athlete_event_results_file.close()

if __name__ == "__main__":
    main()

# events = {}
# with open('athlete_events.csv') as original_data_file,\
#         open('events.csv', 'w') as events_file:
#     reader = csv.reader(original_data_file)
#     writer = csv.writer(events_file)
#     heading_row = next(reader) # eat up and ignore the heading row of the data file
#     for row in reader:
#         event_name = row[13]
#         if event_name not in events:
#             event_id = len(events) + 1
#             events[event_name] = event_id
#             writer.writerow([event_id, event_name])