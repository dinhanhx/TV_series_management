/* Drop tables if exist */
DROP TABLE IF EXISTS series_creators;
DROP TABLE IF EXISTS series_genres;
DROP TABLE IF EXISTS characters;
DROP TABLE IF EXISTS actors;
DROP TABLE IF EXISTS creators;
DROP TABLE IF EXISTS genres;
DROP TABLE IF EXISTS episodes;
DROP TABLE IF EXISTS series;


/* TABLE DEFINITIONS */

CREATE TABLE series (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(50),
    lang CHAR(2),
    current_status CHAR(1),
    rating DECIMAL(2, 1),
    link VARCHAR(2083) -- "url" in the database
);

CREATE TABLE episodes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    series_id INT,
    episode_name VARCHAR(50),
    episode_number INT,
    season_number INT,
    duration INT,
    release_date DATE,
    link VARCHAR(2083)
);

CREATE TABLE genres (
    id INT AUTO_INCREMENT PRIMARY KEY,
    genre_name VARCHAR(20)
);

CREATE TABLE creators (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(20),
    last_name VARCHAR(20),
    nationality CHAR(3),
    gender TINYINT(1),
    link VARCHAR(2083)
);

CREATE TABLE actors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(20),
    last_name VARCHAR(20),
    nationality CHAR(3),
    gender TINYINT(1),
    link VARCHAR(2083)
);

CREATE TABLE characters (
    id INT AUTO_INCREMENT PRIMARY KEY,
    character_name VARCHAR(50),
    actor_id INT NOT NULL,
    series_id INT NOT NULL,
    link VARCHAR(2083)
);

/* Supporting tables for many-many relationships */

CREATE TABLE series_genres (
    series_id INT NOT NULL,
    genre_id INT NOT NULL,
    PRIMARY KEY (series_id, genre_id)
);

CREATE TABLE series_creator (
    series_id INT NOT NULL,
    creator_id INT NOT NULL,
    PRIMARY KEY (series_id, creator_id)
);

ALTER TABLE episodes
ADD CONSTRAINT FK_episodes_series
FOREIGN KEY (series_id) REFERENCES series(id);

ALTER TABLE characters
ADD CONSTRAINT FK_characters_actors
FOREIGN KEY (actor_id) REFERENCES actors(id);

ALTER TABLE characters
ADD CONSTRAINT FK_characters_series
FOREIGN KEY (series_id) REFERENCES series(id);

ALTER TABLE series_genres
ADD CONSTRAINT FK_series_genres_L
FOREIGN KEY (series_id) REFERENCES series(id);

ALTER TABLE series_genres
ADD CONSTRAINT FK_series_genres_R
FOREIGN KEY (genre_id) REFERENCES genres(id);

ALTER TABLE series_creators
ADD CONSTRAINT FK_series_creators_L
FOREIGN KEY (series_id) REFERENCES series(id);

ALTER TABLE series_creators
ADD CONSTRAINT FK_series_creators_R
FOREIGN KEY (creator_id) REFERENCES creators(id);
