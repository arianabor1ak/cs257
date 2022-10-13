SELECT NOCs.abbreviation
FROM NOCs
ORDER BY NOCS.abbreviation;

SELECT athletes.names, NOCs.country
FROM athletes, NOCs, athlete_event_results
WHERE athletes.id = athlete_event_results.athlete_id
AND NOCs.id = athlete_event_results.NOC_id;

SELECT athletes.name, results.medal, events.name, games.year
FROM athletes, results, events, games
WHERE athletes.name = 'Greg Louganis'
AND results.medal = 'Gold'
AND results.medal = 'Silver'
AND results.medal = 'Bronze'
ORDER BY games.year;

SELECT NOCs.name, COUNT(results.medal)
FROM results, NOCS
WHERE results.medal = 'Gold'
ORDER BY COUNT(results.medal)