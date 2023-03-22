from connect import *
from datetime import datetime


USER_SYNTAX = ('userId', 'firstName', 'lastName', 'creationDate', 'lastAccessDate', 'email',
               'password', 'username')

COLLECTION_SYNTAX = ('collectionName', 'userId')

MOVIE_SYNTAX=('movieId','mpaa','title''length')

def convert_tuple(tuple, syntax):
    return {syntax[i]: tuple[i] for i, _ in enumerate(tuple)}


def is_a_user(user_email):
    user = execute_query_one('SELECT * FROM "User" WHERE email = %s;', (user_email, ))
    if user == None:
        return False
    return True


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
    query = execute_query_one('SELECT * FROM "Collection" WHERE "collectionName" = %s AND "userId" = %s;', (name, user_id))
    if query == None:
        return False
    return True

def movie_in_collection(name,movie_id, user_id):
    """Checks if a collection of title 'name' exists for a user

    Args:
        name (string): name of collection
        user_id (int): id of user
    """
    query = execute_query_one('SELECT * FROM "CollectionItem" WHERE "collectionName" = %s AND "movieId"=%s AND "userId" = %s;', (name, movie_id,user_id))
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
    collections = execute_query_all('SELECT * FROM "Collection" WHERE "userId"=%s;', (user_id, ))
    collection_list = []
    for collection in collections:
        collection_list.append(convert_tuple(collection, COLLECTION_SYNTAX))
    return collection_list

def display_all_movies():
    """Displays all the movies in the database
     Args:
     """
    movies = execute_query_all('SELECT * FROM "Movie"',(""))
    movie_list = []
    #print(collections)
    for movie in movies:
        new_list=[]
        new_list.append(movie[0])
        new_list.append(movie[2])
        movie_list.append(new_list)
    #print(movie_list)
    return movie_list

def display_one_movies(movie_id):
    """Displays the movie name with the id
     Args:
         movie_id: id of the movie
     """
    collections = execute_query_all('SELECT "title" FROM "Movie" WHERE "movieId"=%s;', (movie_id, ))
    return collections[0]



def display_collection_movies(collection_name,user_id):
    """displays all the movies in a user collection
        Args:
            collection_name(str): name of the collection
            user_id (int): id of user
        """
    collections = execute_query_all('SELECT "movieId" FROM "CollectionItem" WHERE "collectionName"=%s and "userId"=%s;', (collection_name,user_id))



    movie_list=[]
    for movie in collections:
        new_list=[]
        new_list.append(movie[0])
        e=display_one_movies(movie[0])
        new_list.append(e[0])
        movie_list.append(new_list)
    return movie_list


def movie_exists(movie_id):
    """checks to see if a movie exists
        Args:
            movie_id (int): id of the movie
        """
    query = execute_query_one('SELECT * FROM "Movie" WHERE "movieId" = %s;',
                              (movie_id,))
    if query == None:
        return False
    return True

def add_to_collection(collection_name, movie_id,user_id):
    """adds a movie to a user's collection
    Args:
        movie_id (int): id of the movie
        collection_name(str): name of the collection
        user_id (int): id of user
    """
    print("adding")
    insert_or_update('INSERT INTO "CollectionItem" ("collectionName", "movieId","userId") VALUES (%s, %s,%s);',
                     (collection_name,movie_id, user_id))


def remove_from_collection(collection_name, movie_id,user_id):
    """removes a movie to a user's collection
    Args:
        movie_id (int): id of the movie
        collection_name(str): name of the collection
        user_id (int): id of user
    """
    insert_or_update('DELETE FROM "CollectionItem" WHERE "collectionName"=%s and "movieId"=%s and "userId"=%s', (collection_name,movie_id, user_id))



def rename_collection(old_collection_name,new_collection_name, user_id):
    """rename a collection of a user
    Args:
        old_collection_name(str): name of the collection
        new_collection_name(str): name of the new collection
        user_id (int): id of user
    """
    #insert_or_update('UPDATE "CollectionItem" SET "collectionName" = %s WHERE "collectionName" = %s and "userId"=%s;', (new_collection_name, old_collection_name,user_id))

    insert_or_update('UPDATE "Collection" SET "collectionName" = %s WHERE "collectionName" = %s and "userId"=%s;', (new_collection_name, old_collection_name,user_id))


def delete_collection(collection_name,user_id):
    """deletes a collection of a user
     Args:
         collection_name(str): name of the collection
         user_id (int): id of user
    """
    insert_or_update('DELETE FROM "Collection" WHERE "collectionName"=%s and "userId"=%s', (collection_name, user_id))




search_query = None
def search_movies(category=None, term=None):
    """Find a list of movies dependent on the category and search term

    Args:
        category (string): column to search [title | year | cast | studio | genre]
        term (string): term to search for
    """
    if term == None:
        return execute_query_all("""SELECT movieId, mpaa, title, length FROM "Movies"
            LEFT JOIN "Acting" ON movies.movieId = acting.movieId
            LEFT JOIN person ON acting.personId = person.id
            LEFT JOIN directing ON movies.id = directing.movieId
            LEFT JOIN person AS director ON directing.personId = director.id
        """)
    pass


def sort_movies(sort_by, is_asc):
    """Adds a sort clause to the last executed query

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


def rate_movie():
    pass


def watch_movie():
    pass


def watch_collection():
    pass


def search_friends():
    pass


def add_friend():
    pass


def remove_friend():
    pass



