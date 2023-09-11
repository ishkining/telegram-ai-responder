import psycopg2

from .hello_bitches import hello_einstein, hello_mario

connection_db = None


def _init_tables():
    try:
        cursor = connection_db.cursor()
        cursor.execute("""
                CREATE TABLE characters (
                    id serial PRIMARY KEY,
                    name VARCHAR UNIQUE NOT NULL,
                    hello VARCHAR ( 4096 ) NOT NULL
                );
                
                CREATE TABLE users (
                    id serial PRIMARY KEY,
                    user_id INT UNIQUE NOT NULL,
                    username VARCHAR ( 255 ) NOT NULL,
                    name VARCHAR ( 255 ),
                    surname VARCHAR ( 255 ),
                    time TIMESTAMP NOT NULL,
                    character_id INT,
                    FOREIGN KEY (character_id) REFERENCES characters(id)
                );
                
                CREATE TABLE messages (
                    id serial PRIMARY KEY,
                    user_id INT NOT NULL,
                    character_id INT NOT NULL,
                    request VARCHAR ( 4096 ) NOT NULL,
                    response VARCHAR ( 4096 ),
                    
                    FOREIGN KEY (character_id) REFERENCES characters(id),
                    FOREIGN KEY (user_id) REFERENCES users(id)
                );
            """)
        cursor.close()
    except:
        print('Can`t produce any tables')


def _make_connection(user: str, host: str, password: str, db_name: str):
    global connection_db
    try:
        connection_db = psycopg2.connect(
            dbname=db_name,
            user=user,
            password=password,
            host=host
        )
    except:
        print('Can`t establish connection to database')


def _insert_initial_data():
    global hello_mario, hello_einstein
    try:
        cursor = connection_db.cursor()
        column_names = ['name', 'hello']
        postgres_insert_query = f""" INSERT INTO characters ({','.join(column_names)}) VALUES ({('%s,' * len(column_names))[:-1]})"""
        record_to_insert = ('mario', hello_mario)
        cursor.execute(postgres_insert_query, record_to_insert)
        record_to_insert = ('einstein', hello_einstein)
        cursor.execute(postgres_insert_query, record_to_insert)
        cursor.close()
    except:
        print('Can`t insert characters')


def get_users():
    all_users = None
    try:
        cursor = connection_db.cursor()
        cursor.execute('SELECT * FROM users')
        all_users = cursor.fetchall()
        cursor.close()
    except:
        print('Can`t find users')
    return all_users


def insert_user(user_id: int, username: str, name: str, surname: str, time_now: str):
    try:
        cursor = connection_db.cursor()
        column_names = ['user_id', 'username', 'name', 'surname', 'time']
        postgres_insert_query = f""" INSERT INTO users ({','.join(column_names)}) VALUES ({('%s,' * len(column_names))[:-1]})"""
        record_to_insert = (user_id, username, name, surname, time_now)
        cursor.execute(postgres_insert_query, record_to_insert)
        cursor.close()
    except:
        print('Can`t insert an user')


def is_user_exist(user_id: int):
    that_user = None
    try:
        cursor = connection_db.cursor()
        cursor.execute(f'SELECT * FROM users WHERE user_id = {user_id}')
        that_user = cursor.fetchall()
        cursor.close()
    except:
        print('Can`t find user')
    return False if not that_user else True


def change_character(user_id: int, character: str):
    try:
        cursor = connection_db.cursor()
        cursor.execute(f"SELECT * FROM characters WHERE name='{character}'")
        that_character_id = cursor.fetchall()[0][0]
        cursor.execute(f'UPDATE users SET character_id = {that_character_id} WHERE user_id = {user_id}')
        cursor.close()
    except:
        print('Can`t update mode')


def get_character_from_user(user_id: int):
    user_character = None
    try:
        cursor = connection_db.cursor()
        cursor.execute(f"SELECT * FROM users WHERE user_id = {user_id}")
        character_id = cursor.fetchall()[0][-1]
        if not character_id:
            return None
        cursor.execute(f"SELECT * FROM characters WHERE id = {character_id}")
        user_character = cursor.fetchall()[0]
        cursor.close()
    except:
        print('Can`t get character from user')
        return None
    return user_character


def insert_message(user_id: int, character_id: int, request: str):
    last_message = None
    try:
        cursor = connection_db.cursor()
        cursor.execute(f'SELECT * FROM users WHERE user_id = {user_id}')
        user_foreign_id = cursor.fetchall()[0][0]

        column_names = ['user_id', 'character_id', 'request', 'response']
        postgres_insert_query = f""" INSERT INTO messages ({','.join(column_names)}) VALUES ({('%s,' * len(column_names))[:-1]})"""
        record_to_insert = (user_foreign_id, character_id, request, None)
        cursor.execute(postgres_insert_query, record_to_insert)

        cursor.execute(f"SELECT * FROM messages")
        last_message = cursor.fetchall()[-1]
        cursor.close()
    except:
        print('Can`t insert message')
    return last_message


def get_messages():
    all_users = None
    try:
        cursor = connection_db.cursor()
        cursor.execute('SELECT * FROM messages')
        all_users = cursor.fetchall()
        cursor.close()
    except:
        print('Can`t find users')
    print(all_users)


def update_message(message_id: int, response: str):
    try:
        cursor = connection_db.cursor()
        cursor.execute(f"UPDATE messages SET response = '{response}' WHERE id = {message_id}")
        cursor.close()
        get_messages()
    except:
        print('Can`t update message')
