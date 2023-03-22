from connect import *
from datetime import datetime

def is_a_user(user_email):
    user = execute_query_one('SELECT * FROM "User" WHERE email = %s;', (user_email, ))
    if user == None:
        return False
    return True

user = None
def login(email, password, exists):
    """Login a user or create a new one if they don't exist

    Users will be able to create new accounts and access via login. The system must record
    the date and time an account is created. It must also store the dates and times users
    access the application

    Args:
        email (string): email of user
        password (string): salted password
    """
    today = datetime.now()
    if not exists:
        first_name = input("What's your first name: ")
        last_name = input("What's your last name: ")
        username = input("Enter a username: ")
        insert_or_update(
            """INSERT INTO "User" ("firstName","lastName","creationDate","lastAccessDate",email,password,username) VALUES (%s,%s,%s,%s,%s,%s,%s);""",
            (first_name, last_name, today, today, email, password, username)
        )
    user = execute_query_one("SELECT * FROM \"User\" WHERE 'email' = %s AND 'password' = %s", (email, password))
    if user != None and exists:
        insert_or_update("UPDATE \"User\" SET lastAccessDate = %s WHERE 'email' = %s", (today, email))
    return user


def create_user_collection():
    pass


def display_collections():
    pass


def display_collection_movies():
    pass


def add_to_collection():
    pass


def remove_from_collection():
    pass


def rename_collection():
    pass


def delete_collection():
    pass


search_query = None
def search_movies(category=None, term=None):
    """Find a list of movies dependent on the category and search term

    Users will be able to search for movies by name, release date, cast members, studio, and
    genre. The resulting list of movies must show the movie’s name, the cast members,
    the director, the length and the ratings (MPAA and user). The list must be sorted
    alphabetically (ascending) by movie’s name and release date.

    Args:
        category (string): column to search [title | year | cast | studio | genre]
        term (string): term to search for
    """
    if term == None:
        search_query = """
            SELECT m.title, m.mpaa, g.genreName, 
                GROUP_CONCAT(DISTINCT p.name SEPARATOR ', ') AS actors, 
                GROUP_CONCAT(DISTINCT pd.name SEPARATOR ', ') AS directors, 
                GROUP_CONCAT(DISTINCT YEAR(r.releaseDate) SEPARATOR ', ') AS releaseYears 
            FROM Movie m 
            LEFT JOIN MovieType mt ON m.movieId = mt.movieId 
            LEFT JOIN Genre g ON mt.genreId = g.genreId 
            LEFT JOIN Acting a ON m.movieId = a.movieId 
            LEFT JOIN Person p ON a.personId = p.personId 
            LEFT JOIN Directing d ON m.movieId = d.movieId 
            LEFT JOIN Person pd ON d.personId = pd.personId 
            LEFT JOIN Released r ON m.movieId = r.movieId 
            GROUP BY m.title, m.mpaa, g.genreName
        """
        return execute_query_all()
    pass


def sort_movies(sort_by, is_asc):
    """Adds a sort clause to the last executed query

    Users can sort by: movie name, studio, genre, and released year. Results can be as-
    cending and descending

    Args:
        sort_by (string): sort by category [title | year | studio | genre]
        is_asc (bool): true if ASC
    """
    direction = 'ASC' if is_asc else 'DESC';
    if search_query != None:
        match sort_by.lower():
            case 'title':
                sort_query = "ORDER BY title {}".format(direction)
            case 'year':
                sort_query = "ORDER BY title {}".format(direction)
            case 'studio':
                sort_query = "ORDER BY title {}".format(direction)
            case 'genre':
                sort_query = "ORDER BY title {}".format(direction)
            case _:
                sort_query = "ORDER BY title ASC"
        final_query = '{} {}'.format(search_query, sort_query)  
        return execute_query_all(final_query)


def rate_movie(movieId, rating):
    """Rate a movie

    Users can rate a movie (star rating)

    Args:
        movieId (string): ID of movie
        rating (number): 1-5 rating
    """
    old_rating = execute_query_one('SELECT "movieId", "userId" FROM "Rating" WHERE movieId = %s AND userId = %s LIMIT 1', (movieId, user.userId))
    if old_rating == None:
        insert_or_update('INSERT INTO "Rating" (rating, "movieId", "userId") VALUES (%s, %s, %s)', (rating, movieId, user.userId))
    else:
        insert_or_update('UPDATE "Rating" SET rating = %s WHERE movieId = %s AND userId = %s', (rating, movieId, user.userId))


def watch_movie(movieId):
    """Watch a movie

    Args:
        movieId (string): ID of movie
    """
    today = datetime.now()
    insert_or_update('INSERT INTO "Watching" ("movieId", "userId", watchtime) VALUES (%s, %s, %s)', (movieId, user.userId, today))


def watch_collection():
    pass


def search_friends(userEmail):
    """Users can search for new friends by email

    Args:
        userEmail (string): email to find
    """
    return execute_query_all('SELECT * FROM "User" WHERE email = %s', (userEmail, ))


def add_friend(userId):
    """Users can follow a friend

    Args:
        userId (string): id of user
    """
    insert_or_update('INSERT INTO "Following" (follower, followee) VALUES (%s, %s)', (user.userId, userId))


def remove_friend(userId):
    """Remove a friend

    The application must also allow an user to unfollow a friend

    Args:
        userId (string): user id
    """
    insert_or_update('DELETE FROM "Following" WHERE follower = %s AND followee = %s)', (user.userId, userId))


