CREATE TABLE athletes (
  id SERIAL
  name text
);

CREATE TABLE games (
  id SERIAL
  year integer
  season_id integer
  city text
);

CREATE TABLE seasons (
  id SERIAL
  season text
);

CREATE TABLE events (
  id SERIAL
  sport_id integer
  name text
);

CREATE TABLE sports (
  id SERIAL
  name text
);

CREATE TABLE NOCs (
  id SERIAL
  abbreviation text
  country text
);

CREATE TABLE results (
  id SERIAL
  medal text
);

CREATE TABLE athlete_event_results (
  athlete_id integer
  game_id integer
  event_id integer
  NOC_id integer
  results_id integer
);
