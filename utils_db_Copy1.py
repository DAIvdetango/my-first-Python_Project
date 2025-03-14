from connect_db_Copy1 import connect_to_db_sakila, connect_to_db_ich, close_connection
from tabulate import tabulate
from colorama import Fore, Style, init
init()

#------------------------------------------------------------------------------------------
''' Search movies by genre and year/years'''
#------------------------------------------------------------------------------------------

unic_genre = '''Select  distinct name
                from category '''

def get_genreList():
    connection, cursor = connect_to_db_sakila()
    cursor.execute(unic_genre)
    genres = cursor.fetchall()
    close_connection(connection, cursor)

    headers = ['Select a genre from the list provided']
    print(tabulate(genres,
            headers=headers,
            tablefmt='pretty',
            colalign=('center',)))
    return genres
#------------------------------------------------------------------------------------------

def get_year_to_genre():
    start_year = input('If you want to search also by year, enter the year, otherwise press enter: ').strip()
    if start_year == '':
        return None, None
    else:
        end_year = input('If you want to search in a range of years, put the ending year, otherwise press enter: ').strip()
        if end_year == '':
            return int(start_year), None
        else:
            return int(start_year), int(end_year)

#------------------------------------------------------------------------------------------

db_query_by_genre_year = """
    Select t1.title, t1.release_year, t3.name
    from film t1
    inner join film_category t2 on t1.film_id = t2.film_id
    inner join category t3 on t2.category_id = t3.category_id
    where t3.name = %s and t1.release_year = %s
    limit 20
"""

db_query_by_genre_years = """
    Select t1.title, t1.release_year, t3.name
    from film t1
    inner join film_category t2 on t1.film_id = t2.film_id
    inner join category t3 on t2.category_id = t3.category_id
    where t3.name = %s and t1.release_year between %s and %s
    order by t1.release_year
    limit 20
"""

db_query_by_genre = """
    Select t1.title, t1.release_year, t3.name
    from film t1
    inner join film_category t2 on t1.film_id = t2.film_id
    inner join category t3 on t2.category_id = t3.category_id
    where t3.name = %s
    limit 20
"""

def get_user_genre():
    genre = input('Input the selected genre from provided list: ').strip().capitalize()
    return genre


def get_query_genre_year(genre, start_year  =None, end_year = None):
    if start_year:
        if end_year:
            query = db_query_by_genre_years
            query_id = 'GY'
            return query, (genre, start_year, end_year), query_id
        else:
            query = db_query_by_genre_year
            query_id = 'GY'
            return query, (genre, start_year), query_id
    else:
        query = db_query_by_genre
        query_id = 'G'
        return query, (genre,), query_id

#------------------------------------------------------------------------------------------

def select_film_by_genre_year():
    genres = get_genreList()
    genre = get_user_genre()
    start_year, end_year = get_year_to_genre()
    query, params, query_id = get_query_genre_year(genre, start_year, end_year)
    films = execute_query(query, params)
    request_text = ', '.join(map(str, params))
    insert_film_query(query_id, request_text)
    
    if films:
        print(f'SEARCH RESULT BY GENRE: {genre}, year/\'s: {start_year}{" - " + str(end_year) if end_year else ""}')
        headers = ['Title', 'Year', 'Genre']
        print(tabulate(films,
              headers=headers,
              tablefmt='pretty',
              colalign=('center', 'center', 'center')))
    else:
        print('No movies found in this Genre')

#------------------------------------------------------------------------------------------

def select_film_by_genre_year_for_top():
    top_request = get_top_request()
    request_text = top_request[0][1]
    info = request_text = top_request[0][1].split(', ')
    start_year = info[1]
    genre = info[0]
    try:
        end_year = info[2]
    except IndexError:
        end_year = None
    query, params, query_id = get_query_genre_year(genre, start_year, end_year)
    films = execute_query(query, params)
    request_text = ', '.join(params)
    if films:
        print(f'SEARCH RESULT BY GENRE: {genre}, year/\'s: {start_year}{" - " + str(end_year) if end_year else ""}')
        headers = ['Title', 'Year', 'Genre']
        print(tabulate(films,
              headers=headers,
              tablefmt='pretty',
              colalign=('center', 'center', 'center')))
    else:
        print('No movies found in this Genre')


def select_by_genre_for_top():
    top_request = get_top_request()
    request_text = top_request[0][1]
    info = top_request[0][1].split(', ')
    genre = info[0]
    db_query_by_genre = """
    Select t1.title, t1.release_year, t3.name
    from film t1
    inner join film_category t2 on t1.film_id = t2.film_id
    inner join category t3 on t2.category_id = t3.category_id
    where t3.name = %s
    limit 20 """
    connection, cursor = connect_to_db_sakila()
    cursor.execute(db_query_by_genre, (genre,))
    films = cursor.fetchall()
    close_connection(connection, cursor)
    if films:
        print(f'SEARCH RESULT BY GENRE: {genre}')
        headers = ['Title', 'Year', 'Genre']
        print(tabulate(films,
              headers=headers,
              tablefmt='pretty',
              colalign=('center', 'center', 'center')))
    else:
        print('No movies found with this keyword')
#------------------------------------------------------------------------------------------
''' Search film by actor '''
#------------------------------------------------------------------------------------------

def get_actorsList():
    query_get_actorsList = 'select first_name, last_name from actor limit 30'
    connection, cursor = connect_to_db_sakila()
    cursor.execute(query_get_actorsList)
    actors = cursor.fetchall()
    close_connection(connection, cursor)
    print('Actor\'s list provided')
    headers = ['First name', 'Lasst name']
    print(tabulate(actors,
            headers=headers,
            tablefmt='pretty',
            colalign=('center', 'center')))
#------------------------------------------------------------------------------------------

def get_actor_name_from_user():
    actor_first_name = (input('Input actor\'s first name: ')).strip().upper()
    actor_last_name = (input('Input actor\'s last name: ')).strip().upper()
    return actor_first_name, actor_last_name

def select_film_by_actor(actor_first_name, actor_last_name):
    db_query_by_actor = """select t1.first_name, t1.last_name, t3.title, t3.release_year from actor t1
                        inner join film_actor t2
                        on t1.actor_id = t2.actor_id
                        inner join film t3
                        on t2.film_id = t3.film_id
                        where t1.first_name = %s and t1.last_name = %s limit 10
                    """
    connection, cursor = connect_to_db_sakila()
    cursor.execute(db_query_by_actor, (actor_first_name, actor_last_name))
    film_by_actor = cursor.fetchall()
    close_connection(connection, cursor)
    return film_by_actor
    
#------------------------------------------------------------------------------------------

def set_film_by_actor():
    get_actorsList()
    actor_first_name, actor_last_name = get_actor_name_from_user()
    films = select_film_by_actor(actor_first_name, actor_last_name)
    if films:
        query_id = 'A'
        request_text = ', '.join([actor_first_name, actor_last_name])
        insert_film_query(query_id, request_text)
        print(f'SEARCH RESULT BY ACTOR: {actor_first_name} {actor_last_name}')
        headers = ['First name', 'Last name', 'Title', 'Year']
        print(tabulate(films,
              headers=headers,
              tablefmt='pretty',
              colalign=('center', 'center', 'center', 'center')))
    else:
        print('No movies found with this actor')
        
 #------------------------------------------------------------------------------------------

def search_by_actor_for_top():
    top_request = get_top_request()
    first_name, last_name = top_request[0][1].split(', ')
    films = select_film_by_actor(first_name, last_name)      
     
    if films:
        print(f'SEARCH RESULT BY ACTOR: {first_name} {last_name}')
        headers = ['First name', 'Last name', 'Title', 'Year']
        print(tabulate(films,
              headers=headers,
              tablefmt='pretty',
              colalign=('center', 'center', 'center', 'center')))
    else:
        print('No movies found with this actor')
    

#------------------------------------------------------------------------------------------
''' Search film by keyword '''
#------------------------------------------------------------------------------------------

def get_kw():
    keyword =(input('Input keyword: ')).strip()
    return keyword

def search_by_keyword():
    keyword = get_kw()
    connection, cursor = connect_to_db_sakila()
    query = '''
    select title, release_year, description
    from film
    where title like %s or description like %s 
    limit 20'''
    keyword = f'%{keyword}%'      
    cursor.execute(query, (keyword, keyword))
    films = cursor.fetchall()
    query_id = 'KW'
    request_text = keyword
    insert_film_query(query_id, request_text)
    close_connection(connection, cursor)

    if films:
        print(f'SEARCH RESULT BY KEYWORD: {keyword.strip("%")}')
        colored_films = []
        
        for title, release_year, description in films:
            
            colored_title = title.replace(keyword.strip('%').upper(), f"{Fore.RED}{keyword.strip('%').upper()}{Style.RESET_ALL}")
            colored_description = description.replace(keyword.strip('%'), f"{Fore.RED}{keyword.strip('%')}{Style.RESET_ALL}")
            colored_films.append((colored_title, release_year, colored_description))
            
        headers = ['Title', 'Year', 'Description']
        print(tabulate(colored_films,
                  headers=headers,
                  tablefmt='pretty',
                  colalign=('center', 'center', 'center')))
    else:
        print('No movies found with this keyword')

   
#------------------------------------------------------------------------------------------

def search_by_keyword_for_top():
    top_request = get_top_request()
    keyword = top_request[0][1] 
    connection, cursor = connect_to_db_sakila()
    query = '''
    select title, release_year, description
    from film
    where title like %s or description like %s 
    limit 20'''
    keyword = f'%{keyword.strip("%")}%'
    cursor.execute(query, (keyword, keyword))
    films = cursor.fetchall()
    close_connection(connection, cursor)
    if films:
        colored_films = []
        print(f'SEARCH RESULT BY KEYWORD: {keyword.strip("%")}')
        for title, release_year, description in films:
            
            colored_title = title.replace(keyword.strip('%').upper(), f"{Fore.RED}{keyword.strip('%').upper()}{Style.RESET_ALL}")
            colored_description = description.replace(keyword.strip('%'), f"{Fore.RED}{keyword.strip('%')}{Style.RESET_ALL}")
            colored_films.append((colored_title, release_year, colored_description))
            
        headers = ['Title', 'Year', 'Description']
        print(tabulate(colored_films,
              headers=headers,
              tablefmt='pretty',
              colalign=('center', 'center', 'center')))
    else:
        print('No movies found with this keyword')
       

#------------------------------------------------------------------------------------------
''' Execute query_params '''
#------------------------------------------------------------------------------------------

def execute_query(query, params):
    connection, cursor = connect_to_db_sakila()
    cursor.execute(query, params)
    result = cursor.fetchall()
    close_connection(connection, cursor)
    return result



#------------------------------------------------------------------------------------------
''' insert request to database '''
#------------------------------------------------------------------------------------------

def insert_film_query(query_id, request_text):
    query_description = None  

    if query_id == 'G':
        query_description = 'genre'
    elif query_id == 'A':
        query_description = 'actor'
    elif query_id == 'GY':
        query_description = 'genre, year'
    elif query_id == 'Y':
        query_description = 'year'
    elif query_id == 'Y-Y':
        query_description = 'range year'
    elif query_id == 'KW':
        query_description = 'keyword'
    elif query_id == 'TR':
        query_description = 'top request'
    elif query_id == '0':
        query_description = 'random'

    if query_description is None:
        raise ValueError("Invalid query_id provided")
    
    insert_query = """
    insert into film_queries (query_id, query_description, request_text)
    values (%s, %s, %s)
    """
    
    connection, cursor = connect_to_db_ich()
    
    try:
        cursor.execute(insert_query, (query_id, query_description, request_text))
        connection.commit()
        
    except Exception:
        connection.rollback()  
    finally:
        close_connection(connection, cursor)

#------------------------------------------------------------------------------------------
''' Get top request '''
#------------------------------------------------------------------------------------------

def get_top_request():
    request_get_top = '''select query_id, request_text, count(*) as cnt_queries
                    from film_queries
                    group by query_id, request_text
                    order by cnt_queries desc
                    limit 1'''

    connection, cursor = connect_to_db_ich()
    cursor.execute(request_get_top)
    top_request = cursor.fetchall() 
    close_connection(connection, cursor)
    return top_request

def execute_top_request():
    top_request = get_top_request()
    query_id = top_request[0][0]
    request_text = top_request[0][1]
    
    if query_id == 'G':
        film_set = select_by_genre_for_top()
    elif query_id == 'A':
        #actor_first_name, actor_last_name = request_text.split(', ')
        film_set = search_by_actor_for_top()    
    elif query_id == 'GY':
        film_set = select_film_by_genre_year_for_top()
    elif query_id in ['Y', 'Y-Y']:
        film_set = select_film_by_year_for_top()
    elif query_id == 'KW':
        film_set = search_by_keyword_for_top()
    elif query_id == '0':
        film_set = search_random()
    
    return  film_set
    

'''def execute_top_request():
    top_request = get_top_request()
    query_id = top_request[0][0]
    if query_id == 'G':
        films = select_by_genre_for_top(top_request)
    elif query_id == 'A':
        films = search_by_actor_for_top(top_request)
    elif query_id == 'GY':
        films = select_film_by_genre_year_for_top(top_request)
    #elif query_id == 'Y' or query_id == 'Y-Y':
        #films = select_film_by_year_for_top()
    #elif query_id == 'Y-Y':
        #films = select_film_by_year_for_top()
    elif query_id == 'KW':
        films = search_by_keyword_if_top()
    elif query_id == '0':
        films = search_random()

    if query_description is None:
        raise ValueError("Invalid query_id provided")
    return  films'''
        
    


#------------------------------------------------------------------------------------------
''' Search movies by year/years'''
#------------------------------------------------------------------------------------------

def get_user_year():
    start_year = int(input('Enter the year of the movie\'s release: ').strip())
    
    end_year = input('If you want to search in a range of years, put the ending year, otherwise press enter: ').strip()
    
    return start_year, int(end_year) if end_year else None

def get_query_by_years(start_year, end_year = None):
    if end_year:
        query = """
        Select t1.title, t1.release_year, t3.name
        from film t1
        inner join film_category t2 on t1.film_id = t2.film_id
        inner join category t3 on t2.category_id = t3.category_id
        where t1.release_year between %s and %s
        order by t1.release_year
        limit 30
        """
        return query, (start_year, end_year)
    else:
        query = """
        Select t1.title, t1.release_year, t3.name
        from film t1
        inner join film_category t2 on t1.film_id = t2.film_id
        inner join category t3 on t2.category_id = t3.category_id
        where t1.release_year = %s limit 20
        """
        return query, (start_year,)

def select_films_by_years():
    start_year, end_year = get_user_year() 
    query, params = get_query_by_years(start_year, end_year)
    films = execute_query(query, params)
    request_text = str(params)
    if end_year:
        query_id = 'Y-Y'
    else:
        query_id = 'Y'
    if films:
        insert_film_query(query_id, request_text)
        print('SEARCH RESULT BY YEARS')
        headers = ['Title', 'Year', 'Genre']
        print(tabulate(films,
              headers=headers,
              tablefmt='pretty',
              colalign=('center', 'center', 'center')))
    else:
        print('No movies found in this Year')
    

def select_film_by_year_for_top():
    top_request = get_top_request()
    info = top_request[0][1].split(', ')
    start_year = info[0]
    try:
        end_year = info[1]
    except IndexError:
        end_year = None
    query, params = get_query_by_years(start_year, end_year)
    films = execute_query(query, params)
    if films:
        print(F'SEARCH FILMS BY YEAR/\'s: {start_year}{" - " + str(end_year) if end_year else ""}')
        headers = ['Title', 'Year', 'Genre']
        print(tabulate(films,
              headers=headers,
              tablefmt='pretty',
              colalign=('center', 'center', 'center')))
    else:
        print('No movies found in this Year')

    
#------------------------------------------------------------------------------------------
''' Search movies random'''
#------------------------------------------------------------------------------------------

def search_random():
    connection, cursor = connect_to_db_sakila()
    query_description = None 
    
    query = '''
        select t1.title, t3.name, t1.release_year, t1.description
        from film t1
        join film_category t2
        on t1.film_id = t2.film_id
        join category t3
        on t2.category_id = t3.category_id 
        order by rand()
        limit 20'''
        
    cursor.execute(query)
    films = cursor.fetchall()

    max_description_length = 50 
    films = [(title, genre, year, (description[:max_description_length] + '...') if len(description) > max_description_length else description) 
             for title, genre, year, description in films]
        
    if films:
        
        query_id, request_text = '0', 'random'
        insert_film_query(query_id, request_text)
        print('RANDOM SELECTION OF MOVIES')
        headers = ['Title', 'Genre', 'Year', 'Description']
        print(tabulate(films, headers=headers, tablefmt='pretty', colalign=('center', 'center', 'center', 'center')))
    else:
        print('No movies found in the random selection.')
    
    close_connection(connection, cursor)
                
#----------------------------------------------
#----------------------------------------------

if __name__=='__main__':
    pass