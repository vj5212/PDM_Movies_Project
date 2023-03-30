# Main executable for program. Command line based
from services import *
import math


def main():
    global user
    user = welcome()

    print('Welcome {} to NotNetflix!\n'.format(user['firstName']))
    while True:
        print('## [MENU] ## COLLECTIONS ## MOVIES ## FRIENDS ## PROFILE ##\n')
        print('COLLECTIONS')
        print('MOVIES')
        print('FRIENDS')
        print('PROFILE')
        print('QUIT')
        category = input("Start with a category: ")

        match category.upper():
            case 'COLLECTIONS':
                collection_commands()
            case 'MOVIES':
                movie_commands()
            case 'FRIENDS':
                friend_commands()
            case 'PROFILE':
                profile_commands()
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

def profile_commands():
    while True:
        print('## MENU ## COLLECTIONS ## MOVIES ## FRIENDS ## [PROFILE] ##\n')
        print('VIEW')
        print('HELP')
        print('BACK')

        selection = input('Type a command: ')
        args = selection.split(' ')
        match args[0].upper():
            case 'VIEW':
                # implement view profile
            case 'HELP':
                __profile_helper__()
            case 'BACK':
                print('Returning to main menu...')
                break
            case _:
                print('Invalid command. Try again!\n\n')
        input('Press enter to finish.')



def collection_commands():
    while True:
        print('## MENU ## [COLLECTIONS] ## MOVIES ## FRIENDS ## PROFILE ##\n')

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
        input('Press enter to finish.')


def movie_commands(is_collection=False, collection_name=None):
    # Search terms stored for use in sort
    category = None
    term = None
    while True:
        if is_collection:
            print('## MENU ## [COLLECTION-MOVIES] ## MOVIES ## FRIENDS ## PROFILE ##\n')
            print('RENAME')
            print('LIST')
            print('ADD')
            print('REMOVE')
            print('DELETE')
        else:
            print('## MENU ## COLLECTIONS ## [MOVIES] ## FRIENDS ## PROFILE ##\n')
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
                if is_collection:
                    results = display_collection_movies(collection_name, user['userId'])
                    __movie_results_helper__(results)

            case 'ADD':
                if is_collection:
                    movies = display_all_movies()
                    i = 0
                    for movie in movies:
                        i = i + 1
                        print(movie[0], ": ", movie[1])
                        if i == 11:
                            break

                    movie_id = input("Which movie would you like to add(pick number) ?")

                    if movie_exists(movie_id):

                        if not movie_in_collection(collection_name, int(movie_id), user['userId']):
                            add_to_collection(collection_name, int(movie_id), user['userId'])
                        else:
                            print("Movie is already in the collection")
                    else:
                        print("That movie id does not exist")

            case 'REMOVE':
                if is_collection:
                    movies = display_collection_movies(collection_name, user['userId'])
                    for movie in movies:
                        print(movie[0], ": ", movie[1])

                    movie_id = input("Which movie would you like to remove (pick number)? ")

                    if movie_in_collection(collection_name, int(movie_id), user['userId']):
                        remove_from_collection(collection_name, int(movie_id), user['userId'])
                        print("REMOVED!!")
                    else:
                        print("Movie id you entered is not in the collection")

            case 'DELETE':
                if is_collection:
                    delete_collection(collection_name, user['userId'])
                    print("Deleted ", collection_name)

            case 'WATCH':
                movieId = args[1] if len(args) > 1 else None
                if movieId == None:
                    print('Id of movie watched is required.')
                else:
                    watch_movie(movieId, user['userId'])
                    print('Movie Id ' + movieId + ' has been watched.')
            case 'RATE':
                movieId = args[1] if len(args) > 1 else None
                rating = args[2] if len(args) > 1 else 'No rating entered'
                if movieId == None:
                    print('Id of movie rated is required.')
                else:
                    rate_movie(movieId, rating, user['userId'])
                    print('Movie Id ' + movieId + ' has been rated as ' + rating)
            case 'SEARCH':
                category = args[1] if len(args) > 1 else None
                term = ' '.join(args[2:]) if len(args) > 2 else None
                print('\nsearching...')
                if category == None:
                    results = search_movies()
                else:
                    movieIds = search_movies_by_term(category, term)
                    results = search_movies(movieIds) if movieIds else []

                __movie_results_helper__(results)
            case 'SORT':
                sort_category = args[1] if len(args) > 1 else None
                direction = args[2] if len(args) > 2 else None
                print('\nsorting results...')
                movieIds = search_movies_by_term(category, term) if category != None else []
                results = search_movies(movieIds, get_sort_movies_clause(sort_category, direction.upper() == 'ASC'))
                __movie_results_helper__(results)
            case 'HELP':
                __movie_helper__(is_collection)
            case 'BACK':
                print('Returning to main menu...')
                break
            case 'FINISH':
                if is_collection:
                    print('Returning to collection menu...')
                    break
        input('Press enter to finish.')


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
        print('## MENU ## COLLECTIONS ## MOVIES ## [FRIENDS] ## PROFILE ##\n')
        print('SEARCH')
        print('ADD')
        print('REMOVE')
        print('HELP')
        print('BACK')

        selection = input('Type a command: ')
        args = selection.split(' ')
        match args[0].upper():
            case 'SEARCH':
                email = args[1] if len(args) > 1 else None
                results = search_friends(email)
                __friend_results_helper__(results)
            case 'ADD':
                userId = args[1] if len(args) > 1 else print('No id specified. Try again')
                if userId:
                    add_friend(userId, user['userId'])
                    print('User with ID {} was followed'.format(userId))
            case 'REMOVE':
                userId = args[1] if len(args) > 1 else print(
                    'No id specified. Try again')
                if userId:
                    remove_friend(userId, user['userId'])
                    print('User with ID {} was unfollowed'.format(userId))
            case 'HELP':
                __friend_helper__()
            case 'BACK':
                print('Returning to main menu...')
                break
        input('Press enter to finish.')

def __profile_helper__():
    print("""
        VIEW --criteria: element to list top 10 movies by ('rating', 'plays', or 'both')
        """)

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


def __movie_results_helper__(results):
    for movie in results:
        if movie[7] != None:
            ratings = [eval(rating)
                            for rating in movie[7].split(', ')]
        else:
            ratings = []
        avg_rating = sum(ratings) / \
                            len(ratings) if len(ratings) > 0 else None
        print()
        print('Movie: ' + movie[1])
        print('MPAA: ' + movie[2])
        hours = math.floor(movie[3])
        minutes = round((movie[3] * 60) % 60)
        print('Runtime: {}h {}m'.format(str(hours), str(minutes)))
        print('Directors: ' +
                movie[5] if movie[5] != None else 'Directors: No directors found')
        print('Cast: ' + movie[4] if movie[4]
                != None else 'Cast: No cast found')
        print('movieId: ' + str(movie[0]))
        print('User Rating: ' + str(round(avg_rating, 1))
                if avg_rating != None else 'Ratings: No ratings found')
    print('Results found: ' + str(len(results)))


def __friend_results_helper__(results):
    for friend in results:
        print()
        print('UserId: {}'.format(friend[0]))
        print('Email: {}'.format(friend[5]))
        print('Name: {}'.format(friend[1] + ' ' + friend[2]))


if __name__ == '__main__':
    main()
