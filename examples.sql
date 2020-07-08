SELECT character_name
FROM characters
WHERE characters.series_id = 1;

SELECT series.title, COUNT(episodes.id) AS num_episodes
FROM episodes, series
WHERE episodes.series_id = series.id
GROUP BY series.title;

SELECT series.lang AS `language`, COUNT(series.id) AS num_series
FROM series
GROUP BY series.lang;

SELECT genres.genre_name, COUNT(series.id) AS num_series
FROM series, genres, series_genres
WHERE series_genres.series_id = series.id
    AND series_genres.genre_id = genres.id
GROUP BY genre_name;
