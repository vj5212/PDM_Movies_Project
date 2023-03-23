# Main executable for program. Command line based
from services import *
import math


def main():
    global user
    user = welcome()

    # print('Welcome {} to NotNetflix! Type a category below or sign out!\n'.format(user.firstName + ' ' + user.lastName))
    print('Welcome {} to NotNetflix!\n'.format(user['firstName']))
    while True:
        print('## [MENU] ## COLLECTIONS ## MOVIES ## FRIENDS ##\n')
        print('COLLECTIONS')
        print('MOVIES')
        print('FRIENDS')
        print('QUIT')
        category = input()

        match category.upper():
            case 'COLLECTIONS':
                collection_commands()
            case 'MOVIES':
                movie_commands()
            case 'FRIENDS':
                friend_commands()
            case 'QUIT':
                print('Thank you for using NotNetflix!')
                break
            case _:
                print('Invalid command. Try again.')


def welcome():
    while True:
        email = input('Welcome to NotNetflix! Please enter your email address to sign up or login: ')
        is_user = is_a_user(email)

        # Salt the input before saving it
        if not is_user:
            while True:
                password = input('Create a password for your account: ')
                verify_password = input('Verify the password matches: ')
                if password == verify_password:
                    break
                else:
                    print('Passwords did not match. Please try again.')
        else:
            password = input('Enter your password to login: ')

        try:
            user = login(email, password, is_user)
            print('Login successful!\n')
            return user
        except Exception:
            print('Login failed...Please try again!\n')


def collection_commands():
    while True:
        print('## MENU ## [COLLECTIONS] ## MOVIES ## FRIENDS ##\n')

        print('DISPLAY')
        print('WATCH')
        print('CREATE')
        print('MODIFY')
        print('HELP')
        print('BACK')

        selection = input('Type a command: ')
        args = selection.split(' ')
        match args[0].upper():
            case 'DISPLAY':
                display_user_collection()
            case 'WATCH':
                # get collection name
                name = input('Enter the collection you would like to watch')
                if is_a_collection(name, user['userId']):
                    watch_collection(name, user['userId'])
                else:
                    print('Not a valid collection')
            case 'CREATE':
                # ask for collection name
                name = input('Enter a name for your collection: ')
                if not is_a_collection(name, user['userId']):
                    create_user_collection(name, user['userId'])
                    # display new list of collections
                    display_user_collection()
                else:
                    print('Collection already exists')
            case 'MODIFY':
                display_user_collection()
                # ask for collection name to modify
                name = input('Enter a collection to modify: ')
                if is_a_collection(name, user['userId']):
                    movie_commands(True, name)
                else:
                    print('Not a valid collection')
            case 'HELP':
                __collection_helper__()
            case 'BACK':
                print('Returning to main menu...')
                break
            case _:
                print('Invalid command. Try again!\n\n')


def movie_commands(is_collection=False, collection_name=None):
    ### Remove asking for collection_name again ###
    ### Change references to collectionName ###
    ### Fill necessary arguments ###
    while True:
        if is_collection:
            print('## MENU ## [COLLECTION-MOVIES] ## MOVIES ## FRIENDS ##\n')
            print('RENAME')
            print('LIST')
            print('ADD')
            print('REMOVE')
            print('DELETE')
        else:
            print('## MENU ## COLLECTIONS ## [MOVIES] ## FRIENDS ##\n')
            print('WATCH')
            print('RATE')
        print('SEARCH')
        print('SORT')
        print('HELP')
        print('FINISH' if is_collection else 'BACK')

        selection = input('Type a command: ')
        args = selection.split(' ')
        match args[0].upper():
            case 'RENAME':
                if is_collection:
                    NewcollectionName = input("What would you like to rename it to? ")
                    rename_collection(collection_name, NewcollectionName, user['userId'])
                    print("Renamed collection from: ", collection_name, " to ", NewcollectionName)

            case 'LIST':
                ### Reformat Output ####
                if is_collection:
                    for movie in display_collection_movies(collection_name, user['userId']):
                        print(movie)

            case 'ADD':
                if is_collection:
                    movies = display_all_movies()
                    i = 0
                    for movie in movies:
                        i = i + 1
                        print(movie[0], ": ", movie[1])
                        if i == 11:
                            break

                    movie_id = input("Which of the movie would you like to add(pick number) ?")

                    if movie_exists(movie_id):

                        if not movie_in_collection(collectionName, int(movie_id), user['userId']):
                            add_to_collection(collectionName, int(movie_id), user['userId'])
                        else:
                            print("Movie is already in the collection")
                    else:
                        print("That movie id does not exist")

            case 'REMOVE':
                if is_collection:
                    display_user_collection()

                    collectionName = input("Which of the collection would you like to remove from?")

                    if is_a_collection(collectionName, user['userId']) == False:
                        print("that is not a correct collection name")
                        # movie_commands(True)
                        break
                    movies = display_collection_movies(collectionName, user['userId'])
                    for movie in movies:
                        print(movie[0], ": ", movie[1])

                    movie_id = input("Which of the movie would you like to remove (pick number)? ")

                    if movie_in_collection(collectionName, int(movie_id), user['userId']):
                        remove_from_collection(collectionName, int(movie_id), user['userId'])
                        print("REMOVED!!")
                    else:
                        print("Movie id you entered is not in the collection")

            case 'DELETE':
                if is_collection:
                    display_user_collection()
                    collectionName = input("Which Collection would you like to delete? ")

                    if is_a_collection(collectionName, user['userId']) == False:
                        print("that is not a correct collection name")
                        # movie_commands(True)
                        break

                    delete_collection(collectionName, user['userId'])
                    print("Deleted ", collectionName)

            case 'WATCH':
                watch_movie()
            case 'RATE':
                rate_movie()
            case 'SEARCH':
                search_movies()
            case 'SORT':
                sort_movies()
            case 'HELP':
                __movie_helper__(is_collection)
            case 'FINISH':
                if is_collection:
                    print('Returning to collection menu...')
                    break


def display_user_collection():
    collection_name_header = "Collection Name"
    movie_count_header = "# of Movies"
    runtime_sum_header = "Length of Movies"
    print(f"{collection_name_header:<50}{movie_count_header:<16}{runtime_sum_header:<24}")
    collections = display_collections(user['userId'])
    for collection in collections:
        """
        collection[0] = Collection Name
        collection[1] = # of Movies
        collection[2] = Length of Movies
        """
        hours_string = "hours"
        minutes_string = "minutes"
        total_minutes = collection[2] * 60
        hours = math.floor(collection[2])
        remainder_minutes = math.floor(total_minutes - hours * 60)
        if hours == 1:
            hours_string = "hour"
        if remainder_minutes == 1:
            minutes_string = "minute"
        print(f"{collection[0]:<50}{collection[1]:<16}{hours:<6}"
              f"{hours_string:<6}{remainder_minutes:<4}{minutes_string}")


def friend_commands():
    while True:
        print('## MENU ## COLLECTIONS ## MOVIES ## [FRIENDS] ##\n')
        print('SEARCH')
        print('ADD')
        print('REMOVE')
        print('HELP')
        print('BACK')

        selection = input('Type a command: ')
        args = selection.split(' ')
        match args[0].upper():
            case 'SEARCH':
                search_friends()
            case 'ADD':
                add_friend()
            case 'REMOVE':
                remove_friend()
            case 'HELP':
                __friend_helper__()
            case 'BACK':
                print('Returning to main menu...')
                break


def __collection_helper__():
    print("""
        DISPLAY : Lists all user collections
        WATCH --collectionName : Watches a collection
        CREATE --collectionName : Creates a new collection with specified name
        MODIFY --collectionName : Allows commands to modify a collection
    """)


def __movie_helper__(is_collection=False):
    if is_collection:
        print("""
            RENAME --newName : Renames current modified collection
            LIST : list all the movies in the collection
            ADD --movieId : Adds the movie matching the given ID to the collection
            REMOVE --movieId : Removes movie matching the given ID from the collection
            DELETE : deletes the currently modified collection
            SEARCH --[title | year | cast | studio | genre] --searchTerm : search by and on term
            SORT --[title | year | studio | genre] --[ASC | DESC] : sort current display by
        """)
    else:
        print("""
            WATCH --movieId : Watch the movie with the given ID
            RATE --movieId --rating : Rate the movie with the given ID
            SEARCH --[title | year | cast | studio | genre] --searchTerm : search by and on term
            SORT --[title | year | studio | genre] --[ASC | DESC] : sort current display by
        """)


def __friend_helper__():
    print("""
        SEARCH --userEmail : search for users with the specified email
        ADD --userId : add user to friends list
        REMOVE --userId : remove user from friends list
    """)


if __name__ == '__main__':
    main()
