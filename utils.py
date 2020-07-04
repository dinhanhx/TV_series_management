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
    try:
        r = requests.get(f'http://api.tvmaze.com/shows/{i}')
        data = r.json()
        return f"INSERT INTO series (title, lang, current_status, rating, link) " \
                f"VALUES ('{sqr(data['name'])}', '{to_iso639_1(data['language'])}', " \
                f"'{data['status']}', {data['rating']['average']}, '{data['url']}');\n"
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

def get_creators(i):
    """
    Get tv series' creators then make sql statement to insert into table creators
    """
    def get_code(obj):
        if obj is not None: return obj['code']

        return None

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

def get_actors_characters(i_start, ii_end):
    """
    Get tv series' actors and characters
    then make sql statement to insert into table actors and characters
    """
    def get_code(obj):
        if obj is not None: return obj['code']

        return None

    counter = 0
    sql = f""
    for i in range(i_start, ii_end):
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

if __name__ == '__main__':
    f = open('insert_into_tables.sql', 'w', encoding = 'utf-8')
    for i in range(1, 11):
        f.write(get_series(i))
        f.write(get_episodes(i))
        f.write(get_creators(i))
        f.write(get_series_creators(i))

    f.write(get_actors_characters(1, 11))
    f.close()
