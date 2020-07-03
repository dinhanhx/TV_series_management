import requests
from iso639 import to_iso639_1

def get_series(i):
    """
    Get tv series then make sql statement to insert into table series
    """
    try:
        r = requests.get(f'http://api.tvmaze.com/shows/{i}')
        data = r.json()
        return f"INSERT INTO series (title, lang, current_status, rating, link) " \
                f"VALUES ('{data['name']}', '{to_iso639_1(data['language'])}', " \
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
            f"season_number, duration, release_date, link) VALUES ({i}, '{data['name']}', " \
            f"{data['number']}, {data['season']}, {data['runtime']}, {data['airdate']},  "\
            f"'{data['url']}');\n"

        return sql

    except:
        pass


if __name__ == '__main__':
    f = open('insert_into_tables.sql', 'w', encoding = 'utf-8')
    for i in range(1, 11):
        f.write(get_series(i))
        f.write(get_episodes(i))

    f.close()
