from connect import *
from datetime import datetime

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
    user = execute_query_one("SELECT * FROM \"User\" WHERE 'email' = %s AND 'password' = %s", (email, password))
    if user != None and exists:
        insert_or_update("UPDATE \"User\" SET lastAccessDate = %s WHERE 'email' = %s", (today, email))
    return user

def is_a_collection(name, user_id):
    """Checks if a collection of title 'name' exists for a user

    Args:
        name (string): name of collection
        user_id (int): id of user
    """
    query = 'SELECT collectionName FROM COLLECTION WHERE collectionName=' + name + ' AND userId=' + str(user_id)
    return execute_query(query)

def create_user_collection(name, user_id):
    """Creates a new collection with title 'name' for a user

    Args:
        name (string): name of collection
        user_id (int): id of user
    """
    query = 'INSERT INTO COLLECTION (collectionName, userId) VALUES (' + name + ',' + str(user_id) + ')'
    return execute_query(query)


def display_collections(user_id):
    """Displays list of collections for a user
    Args:
        user_id (int): id of user
    """
    query = 'SELECT * FROM COLLECTION WHERE userId=' + str(user_id)
    return execute_query(query)

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



