from flask import Flask, render_template, request

from data import DataFetcher
from plot import Plotter

app = Flask(__name__, template_folder='../templates', static_folder='../static')

def get_artist_info(fetcher, artist, artist_similar, playcount_artist):
    first_genre = artist_similar['artist']['tags']['tag'][0]['name']
    similar_artists = [similar_artist['name'] for similar_artist in artist_similar['artist']['similar']['artist']]
    return {
        "top_artist": artist,
        "genre": first_genre,
        "similar_artists": similar_artists,
        "playcount_artist": playcount_artist
    }

def get_top_artists_and_similars(fetcher, data_artists):
    result = []
    for artist in data_artists['topartists']['artist'][:5]:
        playcount_artist = artist['playcount']
        top_artist = artist['name']
        artist_similar = fetcher.get_artist_info(top_artist)
        result.append(get_artist_info(fetcher, top_artist, artist_similar, playcount_artist))
    
    return result

def get_user_input():
    user = request.form.get('user')
    period = request.form.get('period')
    return user, period

def get_data(fetcher):
    data_artists = fetcher.get_json_data("user.gettopartists")
    data_tracks = fetcher.get_json_data("user.gettoptracks")
    data_albums = fetcher.get_json_data("user.gettopalbums")
    data_user = fetcher.get_user_info()
    return data_artists, data_user, data_tracks, data_albums

def get_top_track(data_track):
    for track in data_track['toptracks']['track'][:1]:
        top_track = track['name']
        print(top_track)
    return top_track

def get_top_album(data_album):
    top_album = ''
    for album in data_album['topalbums']['album'][:1]:
        top_album = album['name']
        print(top_album)
    return top_album

def process_data(fetcher, data_artists):
    top_artists_and_similars= get_top_artists_and_similars(fetcher, data_artists)
    return top_artists_and_similars

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user, period = get_user_input()
        fetcher = DataFetcher(user, period)
        data_artists, data_user, data_tracks, data_albums = get_data(fetcher)
        top_artists_and_similars = process_data(fetcher, data_artists)
        top_track = get_top_track(data_tracks)
        top_album = get_top_album(data_albums)
        plotter = Plotter()
        data_pie_top_track = plotter.plot_data_pie(data_tracks, "track", user, period)
        data_pie_top_album = plotter.plot_data_pie(data_albums, "album", user, period)

        return render_template('index.html', period=period, top_track=top_track, top_album=top_album, top_artists_and_similars=top_artists_and_similars, data_user=data_user, data_pie_top_album=data_pie_top_album, data_pie_top_track=data_pie_top_track)
    else: 
        user, period = get_user_input()
        fetcher = DataFetcher(user, period)
        data_artists, data_user, data_tracks, data_albums = get_data(fetcher)
        top_artists_and_similars = process_data(fetcher, data_artists)
        top_track = get_top_track(data_tracks)
        top_album = get_top_album(data_albums)
        plotter = Plotter()
        data_pie_top_track = plotter.plot_data_pie(data_tracks, "track", user, period)
        data_pie_top_album = plotter.plot_data_pie(data_albums, "album", user, period)
        return render_template('index.html', period=period, top_track=top_track, top_album=top_album, top_artists_and_similars=top_artists_and_similars, data_user=data_user, data_pie_top_album=data_pie_top_album, data_pie_top_track=data_pie_top_track)
        

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)