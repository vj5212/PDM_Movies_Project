from connect import *
from datetime import datetime

USER_SYNTAX = ('userId', 'firstName', 'lastName', 'creationDate', 'lastAccessDate', 'email',
               'password', 'username')

COLLECTION_SYNTAX = ('collectionName', 'userId')

MOVIE_SYNTAX = ('movieId', 'mpaa', 'title', 'length')

WATCHING_SYNTAX = ('watchtime', 'userId', 'movieId')


SELECT_CLAUSE = """
    SELECT
        m."movieId",
        m.title,
        m.mpaa,
        m.length,
        STRING_AGG(DISTINCT p.name, ', ') AS actors,
        STRING_AGG(DISTINCT pd.name, ', ') AS directors,
        STRING_AGG(DISTINCT EXTRACT(YEAR FROM r."releaseDate")::text, ', ') AS releaseYears,
        STRING_AGG(rating.rating::text, ', ') AS ratings
    FROM "Movie" m
    LEFT JOIN "Acting" a ON m."movieId" = a."movieId"
    LEFT JOIN "Person" p ON a."personId" = p.personId
    LEFT JOIN "Directing" d ON m."movieId" = d."movieId"
    LEFT JOIN "Person" pd ON d."personId" = pd.personId
    LEFT JOIN "Released" r ON m."movieId" = r."movieId"
    LEFT JOIN "Rating" rating on m."movieId" = rating."movieId"
"""

SORT_BY_GENRE = """
    SELECT
        m."movieId",
        m.title,
        m.mpaa,
        m.length,
        STRING_AGG(DISTINCT p.name, ', ') AS actors,
        STRING_AGG(DISTINCT pd.name, ', ') AS directors,
        STRING_AGG(DISTINCT EXTRACT(YEAR FROM r."releaseDate")::text, ', ') AS releaseYears,
        STRING_AGG(rating.rating::text, ', ') AS ratings,
        STRING_AGG(DISTINCT g."genreName", ', ') AS genres,
    FROM "Movie" m
    LEFT JOIN "Acting" a ON m."movieId" = a."movieId"
    LEFT JOIN "Person" p ON a."personId" = p.personId
    LEFT JOIN "Directing" d ON m."movieId" = d."movieId"
    LEFT JOIN "Person" pd ON d."personId" = pd.personId
    LEFT JOIN "Released" r ON m."movieId" = r."movieId"
    LEFT JOIN "Rating" rating on m."movieId" = rating."movieId"
    LEFT JOIN "MovieType" mt ON m."movieId" = mt."movieId"
    LEFT JOIN "Genre" g ON mt."genreId" = g."genreId"
"""

SORT_BY_STUDIO = """
    SELECT
        m."movieId",
        m.title,
        m.mpaa,
        m.length,
        STRING_AGG(DISTINCT p.name, ', ') AS actors,
        STRING_AGG(DISTINCT pd.name, ', ') AS directors,
        STRING_AGG(DISTINCT EXTRACT(YEAR FROM r."releaseDate")::text, ', ') AS releaseYears,
        STRING_AGG(rating.rating::text, ', ') AS ratings,
        STRING_AGG(DISTINCT s."studioName", ', ') AS producers,
    FROM "Movie" m
    LEFT JOIN "Acting" a ON m."movieId" = a."movieId"
    LEFT JOIN "Person" p ON a."personId" = p.personId
    LEFT JOIN "Directing" d ON m."movieId" = d."movieId"
    LEFT JOIN "Person" pd ON d."personId" = pd.personId
    LEFT JOIN "Released" r ON m."movieId" = r."movieId"
    LEFT JOIN "Rating" rating on m."movieId" = rating."movieId"
    LEFT JOIN "Producing" producing ON m."movieId" = producing."movieId"
    LEFT JOIN "Studio" s ON producing."studioId" = s."studioId"
"""

def convert_tuple(tuple, syntax):
    return {syntax[i]: tuple[i] for i, _ in enumerate(tuple)}


def is_a_user(user_email):
    user = execute_query_one('SELECT * FROM "User" WHERE email = %s;', (user_email,))
    if user == None:
        return False
    return True

# user = None

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
    user = execute_query_one('SELECT * FROM "User" WHERE email = %s AND password = %s;', (email, password))
    if user != None and exists:
        insert_or_update('UPDATE "User" SET "lastAccessDate" = %s WHERE email = %s;', (today, email))
    return convert_tuple(user, USER_SYNTAX)


def is_a_collection(name, user_id):
    """Checks if a collection of title 'name' exists for a user

    Args:
        name (string): name of collection
        user_id (int): id of user
    """
    query = execute_query_one('SELECT * FROM "Collection" WHERE "collectionName" = %s AND "userId" = %s;',
                              (name, user_id))
    if query == None:
        return False
    return True


def movie_in_collection(name, movie_id, user_id):
    """Checks if a collection of title 'name' exists for a user

    Args:
        name (string): name of collection
        user_id (int): id of user
    """
    query = execute_query_one(
        'SELECT * FROM "CollectionItem" WHERE "collectionName" = %s AND "movieId"=%s AND "userId" = %s;',
        (name, movie_id, user_id))
    if query == None:
        return False
    return True


def create_user_collection(name, user_id):
    """Creates a new collection with title 'name' for a user

    Args:
        name (string): name of collection
        user_id (int): id of user
    """

    insert_or_update(
        'INSERT INTO "Collection" ("collectionName", "userId") VALUES (%s, %s);', (name, user_id))


def display_collections(user_id):
    """Displays list of collections for a user
    Args:
        user_id (int): id of user
    """
    collections = execute_query_all(
        'SELECT c."collectionName", COUNT(m."movieId"), SUM(m."length") FROM "CollectionItem" as '
        'c INNER JOIN "Movie" m on c."movieId" = m."movieId" WHERE "userId" = %s '
        'GROUP BY c."collectionName";', (user_id,))
    return collections


def count_movies_collection(collection_name, user_id):
    num_movies = execute_query_one('SELECT COUNT("movieId") FROM "CollectionItem" WHERE "userId" = %s AND '
                                   '"collectionName" = %s;', (user_id, collection_name))
    return num_movies[0]


def list_collections(Collection_Name, user_id):
    collections = execute_query_all(
        'SELECT * FROM "CollectionItem" ORDER BY ASC WHERE "CollectionName"=%s AND  "userId"=%s; ',
        (Collection_Name, user_id,))
    print(collections)


def display_all_movies():
    """Displays all the movies in the database
     Args:
     """
    movies = execute_query_all('SELECT * FROM "Movie"', (""))
    movie_list = []
    # print(collections)
    for movie in movies:
        new_list = []
        new_list.append(movie[0])
        new_list.append(movie[2])
        movie_list.append(new_list)
    # print(movie_list)
    return movie_list


def display_one_movies(movie_id):
    """Displays the movie name with the id
     Args:
         movie_id: id of the movie
     """
    movie = execute_query_all('SELECT * FROM "Movie" WHERE "movieId"=%s;', (movie_id,))
    return convert_tuple(movie[0], MOVIE_SYNTAX)


def display_collection_movies(collection_name, user_id):
    """displays all the movies in a user collection
        Args:
            collection_name(str): name of the collection
            user_id (int): id of user
        """
    movie_id_list = execute_query_all(
        'SELECT "movieId" FROM "CollectionItem" WHERE "collectionName"=%s and "userId"=%s;', (collection_name, user_id))
    movie_id_tuple = tuple([movie[0] for movie in movie_id_list])
    return search_movies(movie_id_tuple)



def movie_exists(movie_id):
    """checks to see if a movie exists
        Args:
            movie_id (string): id of the movie
        """
    query = execute_query_one('SELECT * FROM "Movie" WHERE "movieId" = %s;',
                              (movie_id,))
    if query == None:
        return False
    return True


def add_to_collection(collection_name, movie_id, user_id):
    """adds a movie to a user's collection
    Args:
        movie_id (int): id of the movie
        collection_name(str): name of the collection
        user_id (int): id of user
    """
    print("adding")
    insert_or_update('INSERT INTO "CollectionItem" ("collectionName", "movieId","userId") VALUES (%s, %s,%s);',
                     (collection_name, movie_id, user_id))


def remove_from_collection(collection_name, movie_id, user_id):
    """removes a movie to a user's collection
    Args:
        movie_id (int): id of the movie
        collection_name(str): name of the collection
        user_id (int): id of user
    """
    insert_or_update('DELETE FROM "CollectionItem" WHERE "collectionName"=%s and "movieId"=%s and "userId"=%s',
                     (collection_name, movie_id, user_id))


def rename_collection(old_collection_name, new_collection_name, user_id):
    """rename a collection of a user
    Args:
        old_collection_name(str): name of the collection
        new_collection_name(str): name of the new collection
        user_id (int): id of user
    """
    # insert_or_update('UPDATE "CollectionItem" SET "collectionName" = %s WHERE "collectionName" = %s and "userId"=%s;', (new_collection_name, old_collection_name,user_id))

    insert_or_update('UPDATE "Collection" SET "collectionName" = %s WHERE "collectionName" = %s and "userId"=%s;',
                     (new_collection_name, old_collection_name, user_id))


def delete_collection(collection_name, user_id):
    """deletes a collection of a user
     Args:
         collection_name(str): name of the collection
         user_id (int): id of user
    """
    insert_or_update('DELETE FROM "Collection" WHERE "collectionName"=%s and "userId"=%s', (collection_name, user_id))


search_query = None


def search_movies(movieIds = (), sort_clause = ''):

    """Find a list of movies dependent on the category and search term

    Users will be able to search for movies by name, release date, cast members, studio, and
    genre. The resulting list of movies must show the movie’s name, the cast members,
    the director, the length and the ratings (MPAA and user). The list must be sorted
    alphabetically (ascending) by movie’s name and release date.

    Args:
       movieIds (list[ids]): list of movie ids to search for
    """
    if sort_clause != '' and sort_clause[0] == 'genre':
        select_clause = SORT_BY_GENRE
    elif sort_clause != '' and sort_clause[0] == 'studio':
        select_clause = SORT_BY_STUDIO
    else:
        select_clause = SELECT_CLAUSE

    group_clause = 'GROUP BY m.title, m.mpaa, m.length, m."movieId"'
    where_clause = 'WHERE m."movieId" IN %s' if movieIds else None
    order_by = 'ORDER BY m.title, releaseYears' if sort_clause == '' else sort_clause[1]
    if where_clause == None:
        search_query = '{} {} {}'.format(select_clause, group_clause, order_by)
        return execute_query_all(search_query)
    else:
        search_query = '{} {} {} {}'.format(select_clause, where_clause, group_clause, order_by)
        return execute_query_all(search_query, (movieIds, ))


def search_movies_by_term(category, term):
    """Search for movies by term. Returns list of movieIds
    
        Args:
            category (string): category to search on
            term (string): term to search for
    """
    match category.lower():
        case 'title':
            query = 'SELECT "movieId" FROM "Movie" m WHERE m.title ILIKE %s'
        case 'year':
            query = """
                SELECT
                    m."movieId"
                FROM "Movie" m
                LEFT JOIN "Released" r ON m."movieId" = r."movieId"
                WHERE EXTRACT(YEAR FROM r."releaseDate")::text ILIKE %s
            """
        case 'cast':
            query = """
                SELECT
                    m."movieId"
                FROM "Movie" m
                LEFT JOIN "Acting" a ON m."movieId" = a."movieId"
                LEFT JOIN "Person" p ON a."personId" = p.personId
                WHERE p.name ILIKE %s
            """
        case 'studio':
            query = """
                SELECT
                    m."movieId"
                FROM "Movie" m
                LEFT JOIN "Producing" producing ON m."movieId" = producing."movieId"
                LEFT JOIN "Studio" s ON producing."studioId" = s."studioId"
                WHERE s."studioName" ILIKE %s
            """
        case 'genre':
            query = """
                SELECT
                    m."movieId"
                FROM "Movie" m
                LEFT JOIN "MovieType" mt ON m."movieId" = mt."movieId"
                LEFT JOIN "Genre" g ON mt."genreId" = g."genreId"
                WHERE g."genreName" ILIKE %s
            """
        case _:
            print('Invalid category to search on. Try again')
            return None
    data = ('%{}%'.format(term), )
    results = execute_query_all(query, data)
    movieIds = tuple([movie[0] for movie in results])
    return movieIds



def get_sort_movies_clause(sort_by, is_asc):
    """Adds a sort clause to the last executed query

    Users can sort by: movie name, studio, genre, and released year. Results can be as-
    cending and descending

    Args:
        sort_by (string): sort by category [title | year | studio | genre]
        is_asc (bool): true if ASC
    """
    direction = 'ASC' if is_asc else 'DESC';
    match sort_by.lower():
        case 'title':
            sort_query = "ORDER BY m.title {}".format(direction)
        case 'year':
            sort_query = "ORDER BY releaseYears {}".format(direction)
        case 'studio':
            sort_query = "ORDER BY producers {}".format(direction)
        case 'genre':
            sort_query = "ORDER BY genres {}".format(direction)
        case _:
            print('Invalid sort by option. Try again!')
            return None
    return (sort_by.lower(), sort_query)

def rate_movie(movieId, rating, user_id):
    """Rate a movie

    Users can rate a movie (star rating)

    Args:
        movieId (string): ID of movie
        rating (number): 1-5 rating
    """
    old_rating = execute_query_one('SELECT "movieId", "userId" FROM "Rating" WHERE "movieId" = %s AND "userId" = %s LIMIT 1', (movieId, user_id))
    if old_rating == None:
        insert_or_update('INSERT INTO "Rating" (rating, "movieId", "userId") VALUES (%s, %s, %s)',
                         (rating, movieId, user_id))
    else:
        insert_or_update('UPDATE "Rating" SET rating = %s WHERE movieId = %s AND userId = %s',
                         (rating, movieId, user_id))


def watch_movie(movieId, user_id):
    """Watch a movie

    Args:
        movieId (string): ID of movie
    """
    today = datetime.now()
    insert_or_update('INSERT INTO "Watching" ("movieId", "userId", watchtime) VALUES (%s, %s, %s)',
                     (movieId, user_id, today))


def watch_collection(collection_name, user_id):
    movies = execute_query_all('SELECT "movieId" FROM "CollectionItem" WHERE "collectionName"=%s and "userId"=%s;',
                               (collection_name, user_id))
    for movie in movies:
        watch_movie(movie[0], user_id)


def search_friends(userEmail):
    """Users can search for new friends by email

    Args:
        userEmail (string): email to find
    """

    if userEmail == None:
            return execute_query_all('SELECT * FROM "User"')
    return execute_query_all('SELECT * FROM "User" WHERE email = %s;', (userEmail, ))


def add_friend(friend_user_id, userId):
    """Users can follow a friend

    Args:
        userId (string): id of user
    """
    insert_or_update(
        'INSERT INTO "Following" (follower, followee) VALUES (%s, %s);', (userId, friend_user_id))


def remove_friend(friend_user_id, userId):
    """Remove a friend

    The application must also allow an user to unfollow a friend

    Args:
        userId (string): user id
    """
    insert_or_update(
        'DELETE FROM "Following" WHERE follower = %s AND followee = %s;', (userId, friend_user_id))

