import psycopg2


def create_db(cur):
    cur.execute(
        '''CREATE TABLE IF NOT EXISTS Clients
        (id SERIAL PRIMARY KEY, 
        name VARCHAR NOT NULL, 
        surname VARCHAR NOT NULL, 
        email VARCHAR NOT NULL);'''
    )
    cur.execute(
        '''CREATE TABLE IF NOT EXISTS Phones
        (id SERIAL PRIMARY KEY, 
        phone VARCHAR NOT NULL,
        client_id INTEGER REFERENCES Clients(id));'''
    )
    conn.commit()
    pass


def add_client(cur, first_name, last_name, email, phones=None):
    cur.execute(
        '''INSERT INTO Clients(name, surname, email) 
        VALUES(%s, %s, %s);''',
        (first_name, last_name, email)
    )
    cur.execute(
        '''INSERT INTO Phones(phone, client_id)
        VALUES (%s, (SELECT id FROM Clients WHERE name = %s));''',
        (phones, first_name)
    )
    conn.commit()
    pass


def add_phone(cur, phone, client_id):
    cur.execute(
        '''INSERT INTO Phones (phone)
        VALUES(%s, %s);''',
        (phone, client_id)
    )
    conn.commit()
    pass


def change_client(cur, client_id, first_name=None, last_name=None, email=None, phones=None):
    if first_name is not None:
        cur.execute(
            '''UPDATE Clients
            SET name = %s
            WHERE id = %s AND name <> %s;''',
            (first_name, client_id, first_name)
        )
    elif last_name is not None:
        cur.execute(
            '''UPDATE Clients
            SET surname = %s
            WHERE id = %s AND surname <> %s;''',
            (last_name, client_id, last_name)
        )
    elif email is not None:
        cur.execute(
            '''UPDATE Clients
            SET email = %s
            WHERE id = %s AND email <> %s;''',
            (email, client_id, email)
        )
    elif phones is not None:
        cur.execute(
            '''UPDATE Phones
            SET phone = %s
            WHERE client_id = %s AND phone <> %s;''',
            (phones, client_id, phones)
        )
    conn.commit()
    pass


def delete_phone(cur, phone):
    cur.execute(
        '''DELETE FROM Phones 
        WHERE phone = %s;''',
        (phone)
    )
    conn.commit()
    pass


def delete_client(cur, client_id):
    cur.execute(
        '''DELETE FROM Phones 
        WHERE client_id = %s;''',
        (client_id)
    )
    cur.execute(
        '''DELETE FROM Clients 
        WHERE id = %s;''',
        (client_id)
    )
    conn.commit()
    pass


def find_client(cur, first_name=None, last_name=None, email=None, phones=None):
    if phones is not None:
        cur.execute(
            '''SELECT c.name, c.surname, c.email, p.phone FROM Clients c
            JOIN Phones p ON c.id = p.client_id
            WHERE c.name LIKE %s OR c.surname LIKE %s 
            OR c.email LIKE %s OR p.phone LIKE %s;''',
            (first_name, last_name, email, phones)
        )
    else:
        cur.execute(
            '''SELECT c.name, c.surname, c.email, p.phone FROM Clients c
           JOIN Phones p ON c.id = p.client_id
           WHERE c.name LIKE %s OR c.surname LIKE %s 
           OR c.email LIKE %s;''',
            (first_name, last_name, email)
        )
    print(cur.fetchall())
    pass


if __name__ == '__main__':
    with psycopg2.connect(database='client_management', user='postgres', password='postgres') as conn:
        with conn.cursor() as cur:
            create_db(cur)
            add_client(cur, 'Никита', 'Гнеушев', 'никита@gmail.com', '+70000000')
            add_client(cur, 'Таня', 'Гнеушева', 'таня@gmail.com', '+711111111')
            add_client(cur, 'Ann', 'Mancher', 'ancher.mancher@fdfd.com', '+7222222222')
            add_client(cur, 'Artiom', 'Bessudnov', 'a.bessudnov@gmail.com', '+73333333333')
            find_client(cur, 'никита@gmail.com')
            find_client(cur, 'Гнеушев')
            find_client(cur, 'Таня')
            find_client(cur, '+70000000')
            change_client(cur)