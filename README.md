## Book2Playlist

The goal of this project was to create a custom playlist for each book so that a user can listen to a playlist that reflects the changes of the book and provides a proxy soundtrack. The flow from book text to songs playlist is displayed below:
- Book Text Topics -> matched to -> Song Lyrics topics -> Song Lyrics Topic Average Spotify Audio Features -> matched to -> new Spotify Public songs
### Terms above explained:
- Book Text Topics: I went about this using 300 books from Project Gutenberg and topic modeling on this large corpus. I ended with 100 topics
- Song Lyrics Topics: I was able to get the lyrics for 10,000 songs on Metro Lyrics and topic modeled on this corpus as well. I ended with 100 topics for the song lyrics as well
- Average Spotify Audio Features: Spotify provides the audio features to all the songs in their massive library (i.e. acousticness, energy, loudness, etc...). Using these features I was able to find the average audio features of the songs in my song lyric topics. Then using that average audio feature I was able to match back to a larger spotify library to find new songs.
- New Spotify Public songs: Using the spotify public API I was able to find 100,000 songs from their public playlists.

The pickle files for the books, lyrics and new spotify public songs are listed in the link below.  

## Google download for the pickle files https://drive.google.com/open?id=1FFql_HnsOARiGjOuhLJvwlfWkC5hOsD1
