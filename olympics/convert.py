# Hannah Moran
# CS 257

import csv

def main():

    with open('athletes_events.csv') as csvfile:
        athlete_events_text = csv.reader(csvfile)

        athlete_id_checker = []
        id_counter = 0
        olympic_games_checker = []
        olympic_games_id = 0
        olympic_events_checker = []
        olympic_events_id = 0

        for row in athlete_events_text: 
            # add id, name, sex to athletes table
            with open('athletes.csv', 'a') as csvfile:

                athletes = csv.writer(csvfile)
                
                if row[0] in athlete_id_checker:
                    repeated_athlete = True
                else:
                    data = [row[0], row[1], row[2]]
                    athlete_id_checker.append(row[0])
                    repeated_athlete = False
                    athletes.writerow(data)

            # add id (new), age, height, weight, team, year to player_attributes table
            with open('player_attributes.csv', 'a') as csvfile:

                player_attributes = csv.writer(csvfile)

                if repeated_athlete == False:
                    data = [id_counter, row[3], row[4], row[5], row[6], row[9]]
                    id_counter += 1
                    player_attributes.writerow(data)
                else:
                    pass
    
            # add id (new), season, year, city, games to olympic_games
            with open('olympic_games.csv', 'a') as csvfile:
                olympic_games = csv.writer(csvfile)

                if row[8] in olympic_games_checker:
                    pass
                else:
                    data = [olympic_games_id, row[10], row[9], row[11], row[8]]
                    olympic_games_id += 1
                    olympic_games_checker.append(row[8])
                    olympic_games.writerow(data)
            
            # add id, sports, event 
            with open('olympic_events.csv', 'a') as csvfile:
                olympic_events = csv.writer(csvfile)

                if row[13] in olympic_events_checker:
                    pass
                else:
                    olympic_events_checker.append(row[13])
                    data = [olympic_events_id, row[12], row[13]]
                    olympic_events_id += 1
                    olympic_events.writerow(data)

    with open('medals.csv', 'w') as csvfile:
        medals = csv.writer(csvfile)
        medals.writerow("Gold")
        medals.writerow("Silver")
        medals.writerow("Bronze")
        medals.writerow("NA")

# add nocs
    with open('noc_regions.csv', 'r') as csvfile:
        noc_regions_text = csv.reader(csvfile)
        nocs_id = 0
        for row in noc_regions_text:
            with open('nocs', 'w') as csvfile:
                nocs = csv.writer(csvfile)
                
                data = [nocs_id, row[1]]
                nocs_id += 1

                nocs.writerow(data)
                print(data)    

    

if __name__ == '__main__':
    main()