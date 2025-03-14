from connect_db_Copy1 import connect_to_db_sakila, connect_to_db_ich, close_connection
from utils_db_Copy1 import *
import mysql.connector

def main():
    print('Welcome to the movie search app!')
    main_choice()

def main_choice():
    mode = input(""" How do you want to choose a film:
        random search - put                   0
        by genre/genre-year - put:            1
        by keyword - put                      2
        by year or range of years             3
        by actor - put                        4
        by TOP request -                      5
        Finish Search - put                   9
        Start your choice\n""")

    match mode:
        case '1':
            film_set = select_film_by_genre_year()
            continue_search()
        case '2':
            film_set = search_by_keyword()
            continue_search()
        case '3': 
            film_set = select_films_by_years()
            continue_search()
        case '4':
            film_set = set_film_by_actor()
            continue_search()
        case '0':
            film_set = search_random()
            continue_search()
        case '5':
            film_set = execute_top_request()
            continue_search()
        case '9':
            print("Search completed")
            return 
        case _:
            print("Invalid choice. Please try again")
            main_choice()

def continue_search():
    choice = input('''Do you want to continue searching?
                    If yes - put 1
                    if not just press enter: ''')
    match choice:
        case '1':
            main_choice() 
        case _:
            print("Search completed")


if __name__ == "__main__":
    main()