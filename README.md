# Movie Search Application (Python + SQL)

## Project Overview

This project is a console-based application designed to search for movies using the `sakila` database. The application allows users to search for movies by keyword, genre, and year, and also provides functionality to view the most popular search queries. All search queries are stored in a separate database table for tracking and analysis.

---

## Project Concept

The goal of this project is to create a user-friendly console application that interacts with the `sakila` database, a sample database containing information about movies, actors, and rentals. The application enables users to search for movies using various criteria and stores their search queries for future reference. Additionally, users can view the most popular search queries based on historical data.

---

## Key Features

1. **Search Movies by Keyword**:  
   - Users can search for movies by entering a keyword. The application returns a list of 10+ movies that match the keyword.

2. **Search Movies by Genre and Year**:  
   - Users can search for movies by specifying a genre and a year. The application returns a list of 10+ movies that match the criteria.

3. **View Popular Search Queries**:  
   - Users can view the most popular search queries based on historical data stored in a separate database table.

4. **Query Logging**:  
   - All search queries are saved in a separate database table for tracking and analysis.

---

## How It Works

### Database Setup
1. Install the `sakila` database on your local MySQL server.
2. Create a separate database and table to store search queries.

### Application Workflow
1. **Search by Keyword**:  
   - Enter a keyword (e.g., "Action").  
   - The application queries the `sakila` database and returns a list of movies containing the keyword in their title or description.

2. **Search by Genre and Year**:  
   - Enter a genre (e.g., "Comedy") and a year (e.g., "2006").  
   - The application queries the `sakila` database and returns a list of movies matching the specified genre and year.

3. **View Popular Queries**:  
   - Use a specific command (e.g., "popular") to view the most frequently searched queries.

4. **Query Logging**:  
   - Every search query is logged in a separate database table for future analysis.

---

## Technical Implementation

### Tools and Technologies
- **Python**: Used for building the console application and handling user input.
- **MySQL**: Used as the database to store movie data and search queries.
- **SQLAlchemy**: Used for interacting with the MySQL database in Python.
- **Pandas**: Optional for data manipulation and analysis of search queries.

### Database Schema
1. **Sakila Database**:  
   - Contains tables such as `film`, `film_category`, `category`, and `film_text` for movie details.
2. **Search Log Database**:  
   - Contains a table to store search queries, including the search term, timestamp, and user ID (if applicable).

### Code Structure
1. **Database Connection**:  
   - Establishes a connection to the `sakila` database and the search log database.
2. **Search Functions**:  
   - Functions to search movies by keyword, genre, and year.
3. **Query Logging**:  
   - Function to log search queries into the search log database.
4. **Popular Queries**:  
   - Function to retrieve and display the most popular search queries.

---

## How to Run the Application

1. **Set Up the Database**:  
   - Install the `sakila` database on your local MySQL server.  
   - Create a separate database and table for logging search queries.

2. **Install Dependencies**:  
   - Install the required Python libraries:  
     ```bash
     pip install sqlalchemy pandas
     ```

3. **Run the Application**:  
   - Execute the Python script:  
     ```bash
     python movie_search.py
     ```

4. **Follow the Prompts**:  
   - Use the console to search for movies or view popular queries.

---

## Example Usage

### Search by Keyword
```
Enter a keyword: Action
Search Results:
1. The Matrix
2. Die Hard
3. Terminator 2: Judgment Day
...
```

### Search by Genre and Year
```
Enter a genre: Comedy
Enter a year: 2006
Search Results:
1. Borat
2. Little Miss Sunshine
3. The Devil Wears Prada
...
```

### View Popular Queries
```
Enter command: popular
Most Popular Search Queries:
1. Action (50 searches)
2. Comedy (35 searches)
3. 2006 (20 searches)
...
```

---

## License

This project is open-source and available under the [MIT License](LICENSE).

---

Feel free to explore the application and provide feedback! For any questions or suggestions, please open an issue or contact me directly.
