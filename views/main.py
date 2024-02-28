from flask import Flask, render_template, request

from data import DataFetcher

app = Flask(__name__, template_folder='../templates', static_folder='../static')

def get_artist_info(fetcher, artist, artist_similar):
    first_genre = artist_similar['artist']['tags']['tag'][0]['name']
    similar_artists = [similar_artist['name'] for similar_artist in artist_similar['artist']['similar']['artist']]
    return {
        "top_artist": artist,
        "genre": first_genre,
        "similar_artists": similar_artists
    }

def get_top_artists_and_similars(fetcher, data_artists):
    result = []
    for artist in data_artists['topartists']['artist'][:5]:
        top_artist = artist['name']
        artist_similar = fetcher.get_similar_artist(top_artist)
        result.append(get_artist_info(fetcher, top_artist, artist_similar))
    return result

def get_top_artists_and_genres(fetcher, data_artists):
    result = []
    for artist in data_artists['topartists']['artist']:
        top_artist = artist['name']
        artist_similar = fetcher.get_similar_artist(top_artist)
        if 'artist' in artist_similar and 'tags' in artist_similar['artist'] and 'tag' in artist_similar['artist']['tags'] and len(artist_similar['artist']['tags']['tag']) > 0:
            result.append(get_artist_info(fetcher, top_artist, artist_similar))
    return result

def get_recent_artists_and_similars(fetcher, data_recent_track):
    result = []
    processed_artists = set()
    for artist in data_recent_track['recenttracks']['track'][:5]:
        top_artist = artist['artist']['#text']
        if top_artist not in processed_artists:
            processed_artists.add(top_artist)
            artist_similar = fetcher.get_similar_artist(top_artist)
            result.append(get_artist_info(fetcher, top_artist, artist_similar))
    return result

def count_genre_frequency(results):
    genre_count = {}
    for item in results:
        genre = item['genre']
        genre_count[genre] = genre_count.get(genre, 0) + 1

    genre_count = dict(sorted(genre_count.items(), key=lambda item: item[1], reverse=True)[:7])

    return genre_count


def get_user_input():
    user = request.form.get('user')
    period = request.form.get('period')
    return user, period


def get_data(fetcher):
    data_artists = fetcher.get_json_data("user.gettopartists")
    data_user = fetcher.get_user_info()
    return data_artists, data_user

def process_data(fetcher, data_artists):
    top_artists_and_similars = get_top_artists_and_similars(fetcher, data_artists)
    top_artists_and_genres = get_top_artists_and_genres(fetcher, data_artists)
    genre_frequency = count_genre_frequency(top_artists_and_genres)
    sorted_genres = sorted(genre_frequency.items(), key=lambda x: x[1], reverse=True)
    return sorted_genres, top_artists_and_similars

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user, period = get_user_input()
        fetcher = DataFetcher(user, period)
        data_artists, data_user= get_data(fetcher)
        sorted_genres, top_artists_and_similars = process_data(fetcher, data_artists)
        return render_template('index.html', data_user=data_user)
    else: 
        user, period = get_user_input()
        fetcher = DataFetcher(user, period)
        data_artists, data_user= get_data(fetcher)
        sorted_genres, top_artists_and_similars = process_data(fetcher, data_artists)
        return render_template('index.html', data_user=data_user)
        

if __name__ == '__main__':
    app.run(debug=True, port=3333)
