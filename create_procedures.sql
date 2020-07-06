CREATE PROCEDURE get_serie_by_year(@year INT(4))
AS
SELECT title, series_id 
FROM series JOIN episodes
WHERE episode_number = 1 AND release_date = @year
GO;

CREATE PROCEDURE get_top_rating_series
AS
SELECT title AS TopRatingSeries
FROM series
WHERE rating >= 8
GO;

CREATE PROCEDURE get_series_by_genres(@genre char(50))
AS 
SELECT series_id, title
FROM series JOIN series_genres
ON series.id = series_genres.series_id
JOIN genre ON series_genres.genre_id = genres.id
WHERE genres.genre_name = @genre;
