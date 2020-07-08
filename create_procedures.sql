DELIMITER //
CREATE PROCEDURE get_serie_by_year(year INT)
BEGIN
    SELECT title, series_id 
    FROM series JOIN episodes
    WHERE episode_number = 1 AND release_date = year;
END//

CREATE PROCEDURE get_top_rating_series(threshold INT)
BEGIN
    SELECT title AS TopRatingSeries
    FROM series
    WHERE rating >= threshold;
    ORDER BY rating DESC
END//

CREATE PROCEDURE get_series_by_genres(genre char(50))
BEGIN 
    SELECT series_id, title
    FROM series JOIN series_genres
    ON series.id = series_genres.series_id
    JOIN genre ON series_genres.genre_id = genres.id
    WHERE genres.genre_name = @genre;
END//

CREATE PROCEDURE get_rating_sorted
BEGIN
    SELECT title AS SortRating
    FROM series
    ORDER BY rating DESC;
END//

CREATE PROCEDURE get_series_by_status(_status char(1)) --'In Development': 'D','Ended':'E','Running':'R'
BEGIN
    SELECT title, series_id
    FROM series
    WHERE _status = current_status;
END//

DELIMITER ;