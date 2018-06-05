import flask
import pandas as pd
import numpy as np
from spotipy import util
import spotipy
from pprint import pprint

from flask import Flask, render_template, url_for, request
app = Flask(__name__) # create instance of Flask class

books_df = pd.read_pickle('/Users/ngawangtsetan/ds/Fletcher/books_df.pkl')
topic_lookup = pd.read_pickle('/Users/ngawangtsetan/ds/Fletcher/topic_lookup.pkl')
shewas = pd.read_pickle('/Users/ngawangtsetan/ds/Fletcher/songlist_master.pkl')
cos_matrix= pd.read_pickle('/Users/ngawangtsetan/ds/Fletcher/cos_matrix.pkl')
manh_matrix = pd.read_pickle('/Users/ngawangtsetan/ds/Fletcher/manh_matrix.pkl')
euc_matrix = pd.read_pickle('/Users/ngawangtsetan/ds/Fletcher/euc_matrix.pkl')
inst_cos_matrix = pd.read_pickle('/Users/ngawangtsetan/ds/Fletcher/inst_cos_matrix.pkl')
inst_manh_matrix = pd.read_pickle('/Users/ngawangtsetan/ds/Fletcher/inst_manh_matrix.pkl')
inst_euc_matrix = pd.read_pickle('/Users/ngawangtsetan/ds/Fletcher/inst_euc_matrix.pkl')

unm = "spotify:user:1243463812"
user = '1243463812'
scope = "playlist-modify-private"

token = util.prompt_for_user_token(
    unm,
    scope,
    client_id='1bfe1674111049e3ab2bbc1bf4a7640d',
    client_secret='82b9cc64a23f4956bf2dbbeae6895b35',
    redirect_uri='http://localhost/')
sp = spotipy.Spotify(auth=token)

def book2topic(doc_name):
    topics = []
    book_topic = books_df[books_df['title'] == doc_name]['dom_top']
    for num in book_topic:
        hopo = topic_lookup[topic_lookup['book_topic'] == num]['song_topic']
        topics.append(int(hopo))
    return topics

def topic2song(topics, n_songs, mat):
    songs = []
    old_rows = []
    while len(songs) < n_songs:
        for i in topics:
            scores = list(mat.sort_values(by=i,ascending=False).iloc[0:20].index)
            song_row = scores[int(np.random.choice(20,1))]
#             print(f"cur row: {song_row} {shewas.iloc[song_row]['song_name']}" )
#             print(f"old rows: {old_rows}")
            while shewas.iloc[song_row]['song_name'] in old_rows:
                song_row = scores[int(np.random.choice(20,1))]
            songs.append(shewas.iloc[song_row])
            old_rows.append(shewas.iloc[song_row]['song_name'])
    ans_playlist = pd.DataFrame(songs)
#             print('song appended')
    return ans_playlist

def book2playlist(doc_name, n_songs, mat,playlist_name):
    topics = book2topic(doc_name)
    ans = topic2song(topics,n_songs,mat)
    for i in range(len(sp.user_playlists(user)['items'])):
        if sp.user_playlists(user)['items'][i]['name'] == playlist_name:
            playlist_name += '_1'
    plylist = sp.user_playlist_create(user,playlist_name,public=False)
    sp.user_playlist_add_tracks(user,plylist['id'], list(ans['id']))
    print("Playlist Created")
    return plylist['uri']

@app.route('/home') # the site to route to, index/main in this case
def hello():
    return 'At least this page works'
@app.route('/app', methods=["POST", "GET"])
def home():
    # print(pprint(sp.user(user)))
    nome = " "
    if request.method == 'GET':
        name = request.args.get('bookname')
        music = request.args.get('music')
        print('music: ' + str(music))
        print("this is the bookname: " + str(name))
        if name is None:
            print('name is none')
            pass
        else:
            if music == 0:
                uri = book2playlist(name,10,manh_matrix,name)
            else:
                uri = book2playlist(name, 10, inst_manh_matrix, name)
            nome = "https://open.spotify.com/embed?uri=" + uri
            print(nome)
        # print(pprint(sp.user_playlists(user)))
    if nome == ' ':
        send_var = "https://open.spotify.com/embed?uri=spotify:user:1243463812:playlist:1mydyJ2yx1lNwCFfPTRwKM"
    else:
        send_var = nome
    print("send var: " + send_var)
    print("still working")

    return render_template('home.html', title='home', spot = send_var)
@app.route('/demo') # the site to route to, index/main in this case
def demo():
    # print(pprint(sp.user(user)))
    nome = " "
    if request.method == 'GET':
        name = request.args.get('bookname')
        music = request.args.get('music')
        print('music: ' + str(type(music)))
        print("this is the demo bookname: " + str(name))
        if name is None:
            print('name is none')
            playlist = "Spotify Public" + " Playlist"
            pass
        else:
            musik = int(music)
            playlist = str(name) + " Playlist"
            if musik % 10 == 0:
                if musik < 19:
                    uri = book2playlist(name, 10, manh_matrix, name)
                    print('manhattan matrix')
                elif musik < 29:
                    uri = book2playlist(name, 10, euc_matrix, name)
                    print('euclidean matrix')
                else:
                    uri = book2playlist(name, 10, cos_matrix, name)
                    print('cosine matrix')
            else:
                if musik < 19:
                    uri = book2playlist(name, 10, inst_manh_matrix, name)
                    print('inst_manhattan matrix')
                elif musik < 29:
                    uri = book2playlist(name, 10, inst_euc_matrix, name)
                    print('inst_euclidean matrix')
                else:
                    uri = book2playlist(name, 10, inst_cos_matrix, name)
                    print('inst_cosine matrix')
            pass
            nome = "https://open.spotify.com/embed?uri=" + uri
            print(nome)
        # print(pprint(sp.user_playlists(user)))
    if nome == ' ':
        send_var = "https://open.spotify.com/embed?uri=spotify:user:spotify:playlist:37i9dQZF1DXcBWIGoYBM5M"
    else:
        send_var = nome
    print("send var: " + send_var)
    print("still working")

    return render_template('demo.html', title='demos', spot = send_var, playlist = playlist)

if __name__ == '__main__':
    app.run(debug=True)
