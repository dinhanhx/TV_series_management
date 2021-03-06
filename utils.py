import requests
from numba import njit
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

    def get_rating(rating):
        if rating is not None:
            return rating
        else:
            return 0.0

    try:
        r = requests.get(f'http://api.tvmaze.com/shows/{i}')
        data = r.json()
        return f"INSERT INTO series (id, title, lang, current_status, rating, link) " \
                f"VALUES ({data['id']}, '{sqr(data['name'])}', '{to_iso639_1(data['language'])}', " \
                f"'{get_status(data['status'])}', {get_rating(data['rating']['average'])}, '{data['url']}');\n"
    except:
        pass

@njit
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
            f"{data['number']}, {data['season']}, {data['runtime']}, \'{data['airdate']}\',  "\
            f"'{data['url']}');\n"

        return sql

    except:
        pass

def to_iso_5218(gender):
    if gender == 'Male': return 1
    if gender == 'Female': return 2
    if gender == 'Unknown' or gender is None: return 0

    return 9

def to_iso_3166_alpha_3(country):
    from iso3166 import countries
    return countries.get(country)[2]


@njit
def get_creators(i):
    """
    Get tv series' creators then make sql statement to insert into table creators
    """
    def get_code(obj):
        if obj is not None: return to_iso_3166_alpha_3(obj['code'])

        return 'N/A'

    try:
        r = requests.get(f'http://api.tvmaze.com/shows/{i}/crew')
        data = r.json()
        data = list(filter(lambda person: person['type'] == 'Creator', data))
        sql = ''
        for person in data:
            p = person['person']
            sql += f"INSERT INTO creators (id, first_name, last_name, nationality, gender, " \
            f"link) VALUES ({p['id']}, '{sqr(p['name'].split()[0])}', '{sqr(p['name'].split()[-1])}', " \
            f"'{get_code(p['country'])}', {to_iso_5218(p['gender'])}, " \
            f"'{p['url']}');\n"
            sql += f"INSERT INTO series_creators (series_id, creator_id) VALUES ({i}, {p['id']});\n"
        return sql

    except:
        pass


@njit
def get_actors_characters(series_list):
    """
    Get tv series' actors and characters
    then make sql statement to insert into table actors and characters
    """
    def get_code(obj):
        if obj is not None: return to_iso_3166_alpha_3(obj['code'])

        return 'N/A'

    sql = f""
    for i in series_list:
        try:
            r = requests.get(f'http://api.tvmaze.com/shows/{i}/cast')
            list_data = r.json()
            for data in list_data:
                person = data['person']
                sql = sql + f"INSERT INTO actors (id, first_name, last_name, nationality, " \
                f"gender, link) VALUES ({person['id']}, '{sqr(person['name'].split()[0])}', '{sqr(person['name'].split()[-1])}', " \
                f"'{get_code(person['country'])}', {to_iso_5218(person['gender'])}, '{person['url']}');\n"

                character = data['character']
                sql = sql + f"INSERT INTO characters (character_name, actor_id, series_id, link) " \
                f"VALUES ('{sqr(character['name'])}', {person['id']}, {i}, '{character['url']}');\n"


        except:
            pass


    return sql

def get_genres():
	return f"INSERT INTO genres(genre_name) VALUES " \
    f"('Action'), ('Adult'), ('Adventure'), ('Anime'), ('Children'), ('Fantasy'),"\
    f"('Comedy'), ('Crime'), ('DIY'), ('Drama'), ('Espisonage'), ('Family'), "\
    f"('Food'), ('History'), ('Horror'), ('Legal'), ('Medical'), ('Music'), ('Mystery'), "\
    f"('Nature'), ('Romance'), ('Science-Fiction'), ('Supernatural'), ('Thriller'), ('Travel'), ('War'), ('Western');\n"

@njit
def get_genres_id(i):
	try:
		sql = f""
		r = requests.get(f'http://api.tvmaze.com/shows/{i}')
		data = r.json()
		genre = ['Action', 'Adult', 'Adventure', 'Anime', 'Children', 'Fantasy',\
                'Comedy', 'Crime', 'DIY', 'Drama', 'Espionage', 'Family', \
                'Food', 'History', 'Horror', 'Legal', 'Medical', 'Music', 'Mystery', \
                'Nature', 'Romance', 'Science-Fiction', 'Supernatural', 'Thriller', 'Travel', 'War', 'Western']

		# id_genre = [i for i in range(1, len(genre) + 1)]
		genres = data['genres']
		for g in genres:
			sql = sql + f"INSERT INTO series_genres(series_id,genre_id) VALUES ({i}, {1 + genre.index(g)});\n"

		return sql
	except:
	 	pass

@njit
def main():
    f = open('insert_into_tables.sql', 'w', encoding = 'utf-8')
    f.write(get_genres())
    series_list = list(range(1,11))
    series_list += [2102, 24665, 26950, 17861, 27436, 41748, 41749, 41750, 495,
                    19268, 32699, 2503, 21617, 37681, 555, 216, 31989]
    get_list = [get_series, get_episodes, get_creators, get_genres_id]
    for i in series_list:
        for func in get_list:
            if func(i) is not None:
                f.write(func(i))

    f.write(get_actors_characters(series_list))
    f.close()

if __name__ == '__main__':
    main()
