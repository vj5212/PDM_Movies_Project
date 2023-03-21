from connect import *


def is_a_user(user_email):
    user = execute_query_one('SELECT * FROM "User" WHERE email = %s;', (user_email, ))
    if user == None:
        return False
    return True


def login(email, password):
    """Login a user or create a new one if they don't exist

    Users will be able to create new accounts and access via login. The system must record
    the date and time an account is created. It must also store the dates and times users
    access the application

    Args:
        email (string): email of user
        password (string): salted password
    """
    pass

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


def search_movies():
    pass


def sort_movies():
    pass


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





