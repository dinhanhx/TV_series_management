CREATE TABLE series (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(50),
    lang CHAR(2),
    current_status CHAR(1),
    rating DECIMAL(2, 1)
);

CREATE TABLE episodes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    seriesid INT,
    episode_name VARCHAR(50),
    episode_number INT,
    duration INT,
    release_date DATE
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
    gender TINYINT(1)
);

CREATE TABLE actors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(20),
    last_name VARCHAR(20),
    nationality CHAR(3),
    gender TINYINT(1)
);

CREATE TABLE characters (
    id INT AUTO_INCREMENT PRIMARY KEY,
    character_name VARCHAR(50),
    actor_id CHAR(3),
    series_id TINYINT(1)
);
