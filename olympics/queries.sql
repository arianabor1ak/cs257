SELECT DISTINCT abbreviation
FROM NOCs
ORDER BY NOCS.abbreviation;

SELECT name
FROM athletes
WHERE NOCs.abbreviation = 'JAM';

-- athletes.id = athlete_event_results.athlete_id

SELECT name, medal, name, year
FROM athletes, results, events, games
WHERE athletes.name = 'Greg Louganis'
AND (results.medal = 'Gold'
OR results.medal = 'Silver'
OR results.medal = 'Bronze')
ORDER BY games.year;

SELECT NOCs.name, COUNT(results.medal)
FROM results, NOCS
WHERE results.medal = 'Gold'
ORDER BY COUNT(results.medal)