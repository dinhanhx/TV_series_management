import requests
from iso639 import to_iso639_1

def sqr(s):
    """
    Single quote remover
    """
    return s.replace("'", "")

def get_series(i):
    """
    Get tv series then make sql statement to insert into table series
    """
    def get_status(status):
        if status == 'In Development': return 'D'
        if status == 'Ended': return 'E'
        if status == 'Running': return 'R'

        return 'X'

    try:
        r = requests.get(f'http://api.tvmaze.com/shows/{i}')
        data = r.json()
        return f"INSERT INTO series (title, lang, current_status, rating, link) " \
                f"VALUES ('{sqr(data['name'])}', '{to_iso639_1(data['language'])}', " \
                f"'{get_status(data['status'])}', {data['rating']['average']}, '{data['url']}');\n"
    except:
        pass

def get_episodes(i):
    """
    Get tv series' episodes then make sql statement to insert into table episodes
    """
    try:
        r = requests.get(f'http://api.tvmaze.com/shows/{i}/episodes')
        list_data = r.json()
        sql = f""
        for data in list_data:
            sql = sql + f"INSERT INTO episodes (series_id, episode_name, episode_number, " \
            f"season_number, duration, release_date, link) VALUES ({i}, '{sqr(data['name'])}', " \
            f"{data['number']}, {data['season']}, {data['runtime']}, {data['airdate']},  "\
            f"'{data['url']}');\n"

        return sql

    except:
        pass

def to_iso_5218(gender):
    if gender == 'Male': return 1
    if gender == 'Female': return 2
    if gender == 'Not applicable': return 9

    return 0

def to_iso_3166_alpha_3(country):
    from iso3166 import countries
    return countries.get(country)[2]


def get_creators(i):
    """
    Get tv series' creators then make sql statement to insert into table creators
    """
    def get_code(obj):
        if obj is not None: return to_iso_3166_alpha_3(obj['code'])

        return 'N/A'

    try:
        r = requests.get(f'http://api.tvmaze.com/shows/{i}/crew')
        data = r.json()[0]['person']
        return f"INSERT INTO creators (first_name, last_name, nationality, gender, " \
        f"link) VALUES ('{sqr(data['name'].split()[0])}', '{sqr(data['name'].split()[-1])}', " \
        f"'{get_code(data['country'])}', {to_iso_5218(data['gender'])}, " \
        f"'{data['url']}');\n"

    except:
        pass

def get_series_creators(i):
    """
    Make sql statement to insert into table series_creators
    """
    return f"INSERT INTO series_creators (series_id, creator_id) VALUES " \
    f"({i}, {i});\n"

def get_actors_characters(series_list):
    """
    Get tv series' actors and characters
    then make sql statement to insert into table actors and characters
    """
    def get_code(obj):
        if obj is not None: return to_iso_3166_alpha_3(obj['code'])

        return 'N/A'

    counter = 0
    sql = f""
    for i in series_list:
        try:
            r = requests.get(f'http://api.tvmaze.com/shows/{i}/cast')
            list_data = r.json()
            for data in list_data:
                counter = counter + 1
                person = data['person']
                sql = sql + f"INSERT INTO actors (first_name, last_name, nationality, " \
                f"gender, link) VALUES ('{sqr(person['name'].split()[0])}', '{sqr(person['name'].split()[-1])}', " \
                f"'{get_code(person['country'])}', {to_iso_5218(person['gender'])}, '{person['url']}');\n"

                character = data['character']
                sql = sql + f"INSERT INTO characters (character_name, actor_id, series_id, link) " \
                f"VALUES ('{sqr(character['name'])}', {counter}, {i}, '{character['url']}');\n"


        except:
            pass


    return sql

def get_genres():
	return f"INSERT INTO genres(genre_name) VALUES " \
    f"('Action'), ('Adult'), ('Adventure'), ('Anime'), ('Children'), "\
    f"('Comedy'), ('Crime'), ('DIY'), ('Drama'), ('Espisonage'), ('Family'), "\
    f"('Food'), ('History'), ('Horror'), ('Legal'), ('Medical'), ('Music'), ('Mystery'), "\
    f"('Nature'), ('Romance'), ('Science-Fiction'), ('Supernatural'), ('Thriller'), ('Travel'), ('War'), ('Western');\n"

def get_genres_id(i):
	try:
		sql = f""
		r = requests.get(f'http://api.tvmaze.com/shows/{i}')
		data = r.json()
		genre = ['Action', 'Adult', 'Adventure', 'Anime', 'Children', \
                'Comedy', 'Crime', 'DIY', 'Drama', 'Espionage', 'Family', \
                'Food', 'History', 'Horror', 'Legal', 'Medical', 'Music', 'Mystery', \
                'Nature', 'Romance', 'Science-Fiction', 'Supernatural', 'Thriller', 'Travel', 'War', 'Western']

		id_genre = [i for i in range(1, len(genre) + 1)]
		n = data['genres']
		for x in range(len(n)):
			sql = sql + f"INSERT INTO series_genres(series_id,genre_id)" \
			f" VALUES ({i}), ({id_genre[genre.index(n[x])]})\n"

		return sql
	except:
	 	pass

if __name__ == '__main__':
    f = open('insert_into_tables.sql', 'w', encoding = 'utf-8')
    f.write(get_genres())
    series_list = list(range(1,11))
    series_list += [2102, 28946, 26950, 17861, 27436, 41748, 41749, 41750, 495,
                    19268, 32699, 37599, 2503, 351702, 21617, 37681]
    get_list = [get_series, get_episodes, get_creators, get_series_creators, get_genres_id]
    for i in series_list:
        for func in get_list:
            if func(i) is not None:
                f.write(func(i))

    f.write(get_actors_characters(series_list))
    f.close()
