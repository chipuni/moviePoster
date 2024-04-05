How do I set up for this project?

The create_database.py program gets its images from themoviedb.org. In order
to download the movie posters, you must get an account with API privileges
on https://www.themoviedb.org/.

1. Visit https://www.themoviedb.org/signup
2. Create a normal account and sign in.
3. Visit https://www.themoviedb.org/settings/api
4. Request an API key.
5. Fill out the form.
6. The system seems automated. In my case, it immediately approved me.
7. Copy the API read access token to the TMDB_READ_ACCESS_TOKEN environment variable. For example,
   since my read access token is "ey...0s" (with many characters removed), I would type:

export TMDB_READ_ACCESS_TOKEN=ey...0s

Then python/create_database.py should create and download many files to a "database"
directory.