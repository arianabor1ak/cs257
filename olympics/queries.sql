SELECT NOCs.abbreviation
FROM NOCs
ORDER BY NOCS.abbreviation;

SELECT athletes.names, NOCs.country
FROM athletes, NOCs, athlete_event_results
WHERE athletes.id = athlete_event_results.athlete_id
AND NOCs.id = athlete_event_results.NOC_id