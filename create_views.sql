CREATE VIEW seasons AS
(SELECT CONCAT(series.title, ' season ', episodes.season_number) AS season_title, 
	COUNT(episodes.id) AS number_of_episodes
FROM series, episodes
WHERE series_id = series.id
GROUP BY season_title);

CREATE VIEW readable_characters AS
(SELECT characters.character_name, CONCAT(actors.first_name, ' ', actors.last_name) AS played_by, series.title AS appears_in
FROM characters, actors, series
WHERE characters.series_id = series.id AND characters.actor_id = actors.id);