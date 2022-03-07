import os
import sys
import config
os.environ['DATABASE_URL'] = config.DATABASE_URL

import psycopg2 as dbapi2
INIT_TYPES = [
"""CREATE TYPE status AS ENUM ('okey','notokey');""",
    """Create type method as enum ('creditcard','cash');""",
    """CREATE TYPE type AS ENUM ('company', 'personal');""",
    """CREATE TYPE GENDER_TYPE AS ENUM ('male', 'female', 'unisex'); """,
    """CREATE TYPE ROLE AS ENUM ('manicurist','owner','user', 'admin' ); """
]

INIT_STATEMENTS = [
    """
    CREATE TABLE IF NOT EXISTS People(
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE,
        name_surname VARCHAR(50),
        mail VARCHAR(300) UNIQUE,
        password_hash VARCHAR(300),
        gender VARCHAR(10),
        age integer,
        role VARCHAR(10)    
    )""",
    """
    CREATE TABLE IF NOT EXISTS Salon(
        id SERIAL PRIMARY KEY,
        owner_people_id INTEGER REFERENCES People(id) ON DELETE CASCADE,
        shopname VARCHAR(50),
        location VARCHAR(300),
        city VARCHAR(50),
        opening_time TIME,
        closing_time TIME,
        trade_number NUMERIC(10) NOT NULL,
        shop_logo bytea 
    )   
    """,
    """
    CREATE TABLE IF NOT EXISTS Manicurist(
        id SERIAL PRIMARY KEY,
        people_id INTEGER REFERENCES People(id) ON DELETE CASCADE,
        salon_id INTEGER DEFAULT NULL REFERENCES salon(id) ON DELETE SET NULL,
        gender_choice VARCHAR(10),
        experience_year INTEGER DEFAULT 0,
        start_time INTEGER,
        finish_time INTEGER,
        rates INTEGER DEFAULT 0 
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS Serviceprices(
        id SERIAL PRIMARY KEY,
        salon_id INTEGER REFERENCES Salon(id) ON DELETE CASCADE,
        service_name VARCHAR(50),
        definition VARCHAR(300),
        gender VARCHAR(10),
        price DECIMAL(6,2),
        duration INTEGER
    )   
    """,
    """
      CREATE TABLE IF NOT EXISTS Rezervation(
           id SERIAL PRIMARY KEY,
           people_id integer NOT NULL REFERENCES People(id) ON DELETE CASCADE,
           salon_id integer NOT NULL REFERENCES Salon(id) ON DELETE CASCADE,
           datetime_registration TIMESTAMP,
           datetime_rezervation TIMESTAMP,
           status status,
           note VARCHAR (100),
           price_type integer,
           payment_method method
   )""",
    """    
    CREATE TABLE IF NOT EXISTS Comments(
        id SERIAL PRIMARY KEY, 
        people_id integer NOT NULL REFERENCES People(id) ON DELETE CASCADE,
        manicurist integer  REFERENCES Manicurist(id) ON DELETE CASCADE,
        salon_id integer  REFERENCES Salon(id) ON DELETE CASCADE,
        title VARCHAR (100) NOT NULL,
        content VARCHAR (500) NOT NULL,
        rate integer  NOT NULL,
        date_time TIMESTAMP, 
        comment_like integer DEFAULT 0 NOT NULL, 
        comment_dislike  integer DEFAULT 0 NOT NULL,
        keywords VARCHAR(100),
        image bytea,
        CHECK (rate > 0), CHECK (rate < 6) 
    )""",
    """
    
    CREATE TABLE IF NOT EXISTS Contact_info(
        id SERIAL PRIMARY KEY, 
        salon_id integer  REFERENCES Salon(id) ON DELETE CASCADE,
        type type,
        telephone_number VARCHAR (15) NOT NULL,
        facebook VARCHAR (500),
        twitter VARCHAR (500),
        instagram VARCHAR (500)
    )""",
    """      
   CREATE TABLE IF NOT EXISTS CommentLikeDislike(
       id SERIAL PRIMARY KEY,
       comment_id integer NOT NULL REFERENCES Comments(id) ON DELETE CASCADE,
       people_id integer NOT NULL REFERENCES People(id) ON DELETE CASCADE,
       ifliked  integer NOT NULL,
       ifdisliked integer NOT NULL,
       CHECK (ifliked <2), CHECK (ifliked >-2), CHECK (ifdisliked <2), CHECK (ifdisliked >-2) 
   )""",
    """
    CREATE TABLE IF NOT EXISTS Owner(
        id SERIAL PRIMARY KEY,
        people_id INTEGER REFERENCES People(id) ON DELETE CASCADE,
        tc_number NUMERIC(11) UNIQUE NOT NULL,
        serial_number NUMERIC(5) NOT NULL,
        vol_number NUMERIC(5),
        family_order_no NUMERIC(5),
        order_no NUMERIC(5)
    )   
    """,
    """
    CREATE TABLE IF NOT EXISTS Creditcards(
        id SERIAL PRIMARY KEY,
        people_id INTEGER REFERENCES People(id) ON DELETE CASCADE,
        name VARCHAR(50),
        card_number NUMERIC(16) NOT NULL,
        cvv_number NUMERIC(4) NOT NULL,
        last_month NUMERIC(2) NOT NULL,
        last_year NUMERIC(2) NOT NULL,
        created_time TIMESTAMP
    )   
    """,
    """
    CREATE TABLE IF NOT EXISTS Posts(
        id SERIAL PRIMARY KEY,
        people_id INTEGER REFERENCES People(id) ON DELETE CASCADE,
        post_title VARCHAR(50),
        post_content VARCHAR(500),
        like_number INTEGER,
        dislike_number INTEGER,
        subject VARCHAR(20),
        date_time TIMESTAMP
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS post_comment(
        id SERIAL PRIMARY KEY,
        post_id INTEGER REFERENCES Posts(id) ON DELETE CASCADE,
        people_id INTEGER REFERENCES People(id) ON DELETE CASCADE,
        title VARCHAR(50),
        content VARCHAR(500),
        like_number INTEGER,
        dislike_number INTEGER,
        date_time TIMESTAMP
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS campaigns(
        id SERIAL PRIMARY KEY,
        salon_id integer  REFERENCES Salon(id) ON DELETE CASCADE,
        campaign_name VARCHAR(50),
        definition VARCHAR(200),
        start_date TIMESTAMP,
        end_date TIMESTAMP,
        discount integer
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS manicurist_salon_changes(
        id SERIAL PRIMARY KEY,
        people_id integer references people(id) on delete cascade,
        prew_salon_name varchar(50),
        prew_salon_city varchar(50),
        current_salon_name varchar(50),
        current_salon_city varchar(50),
        datetime timestamp not null default NOW()
    )
    """,
    """
        CREATE TABLE IF NOT EXISTS serviceprices_audit(
            operation   char(1)     not null,
            stamp       timestamp   not null,
            people_id   int         not null,
            service_id int,
            salon_id INTEGER,
            service_name VARCHAR(50),
            definition VARCHAR(300),
            gender VARCHAR(10),
            price DECIMAL(6,2),
            duration INTEGER,
            id serial primary key 
        )
    """,
    """
        CREATE TABLE IF NOT EXISTS reservation_logs(
            operation   char(1)     not null,
            stamp       timestamp   not null,
            reservation_id int,
            people_id integer NOT NULL,
            salon_id integer NOT NULL,
            datetime_registration TIMESTAMP,
            datetime_rezervation TIMESTAMP,
            status status,
            note VARCHAR (100),
            price_type integer,
            payment_method method,
            id serial primary key 
        )
    """,
    """
       CREATE TABLE IF NOT EXISTS posts_log(
            operation   char(1)     not null,
            stamp       timestamp   not null,
            post_id int,
            people_id INTEGER,
            post_title VARCHAR(50),
            post_content VARCHAR(500),
            like_number INTEGER,
            dislike_number INTEGER,
            subject VARCHAR(20),
            date_time TIMESTAMP,
            id serial primary key 
       )
       """

]

stored_procedures = [
]


stored_functions = [
    """
    create or replace function log_manicurist_change()
    returns trigger as $manicurist_salon_change$
        DECLARE
        old_shopname varchar(50);
        old_city varchar(50);
        new_shopname varchar(50);
        new_city varchar(50);
        
        BEGIN
           IF (OLD.salon_id <> NEW.salon_id 
           OR (OLD.salon_id IS NULL AND NEW.salon_id IS NOT NULL)
            OR (OLD.salon_id IS NOT NULL AND NEW.salon_id IS NULL) )
            THEN
                IF OLD.salon_id IS NULL THEN
                    old_shopname := 'unemployed';
                    old_city := null;
                ELSE
                    select shopname into old_shopname from salon where salon.id = OLD.salon_id;
                    select city into old_city from salon where salon.id = OLD.salon_id;
                END IF;
                
                IF NEW.salon_id is NULL then
                    new_shopname := 'unemployed';
                    new_city := null;
                ELSE
                    select shopname into new_shopname from salon where salon.id = NEW.salon_id;
                    select city into new_city from salon where salon.id = NEW.salon_id; 
                END IF;
                execute 'insert into manicurist_salon_changes (people_id, prew_salon_name, 
                prew_salon_city, current_salon_name, current_salon_city) values ($1, $2, $3, $4, $5)'
                    using OLD.people_id, old_shopname, old_city, new_shopname, new_city;
                return null;
            END IF;
            return null;
        END;
    $manicurist_salon_change$ language plpgsql;
    """,

    """
        CREATE OR REPLACE FUNCTION process_servicepricess_audit() RETURNS TRIGGER AS $sp_audit$
        declare 
        user_id int;
        BEGIN            
            IF (TG_OP = 'DELETE') THEN
                select owner_people_id into user_id from salon where id = OLD.salon_id;
                INSERT INTO serviceprices_audit SELECT 'D', now(), user_id, OLD.*;
                RETURN OLD;
            ELSIF (TG_OP = 'UPDATE') THEN
                select owner_people_id into user_id from salon where id = NEW.salon_id;
                INSERT INTO serviceprices_audit SELECT 'U', now(), user_id, NEW.*;
                RETURN NEW;
            ELSIF (TG_OP = 'INSERT') THEN
                select owner_people_id into user_id from salon where id = NEW.salon_id;
                INSERT INTO serviceprices_audit SELECT 'I', now(), user_id, NEW.*;
                RETURN NEW;
        END IF;
        execute 'insert into test (kek) values (2)';
        RETURN NULL;
        END;
    $sp_audit$ LANGUAGE plpgsql;
    """,

    """
        CREATE OR REPLACE FUNCTION log_reservations() RETURNS TRIGGER AS $reservation_change$
        BEGIN            
            IF (TG_OP = 'DELETE') THEN
                INSERT INTO serviceprices_audit SELECT 'D', now(), OLD.*;
                RETURN OLD;
            ELSIF (TG_OP = 'UPDATE') THEN
                INSERT INTO serviceprices_audit SELECT 'U', now(), NEW.*;
                RETURN NEW;
            ELSIF (TG_OP = 'INSERT') THEN
                INSERT INTO serviceprices_audit SELECT 'I', now(), NEW.*;
                RETURN NEW;
        END IF;
        execute 'insert into test (kek) values (2)';
        RETURN NULL;
        END;
    $reservation_change$ LANGUAGE plpgsql;
    """,
    """
        CREATE OR REPLACE FUNCTION log_posts() RETURNS TRIGGER AS $post_change$
        BEGIN            
            IF (TG_OP = 'DELETE') THEN
                INSERT INTO posts_log SELECT 'D', now(), OLD.*;
                RETURN OLD;
            ELSIF (TG_OP = 'UPDATE') THEN
                INSERT INTO posts_log SELECT 'U', now(), NEW.*;
                RETURN NEW;
            ELSIF (TG_OP = 'INSERT') THEN
                INSERT INTO posts_log SELECT 'I', now(), NEW.*;
                RETURN NEW;
        END IF;
        execute 'insert into test (kek) values (2)';
        RETURN NULL;
        END;
    $post_change$ LANGUAGE plpgsql;
    """


]

stored_triggers = [
    """
        create trigger manicurist_salon_change
        after update on manicurist
        for each row
        execute function log_manicurist_change();
    """,
    """
        CREATE TRIGGER sp_audit
        AFTER INSERT OR UPDATE OR DELETE ON serviceprices
        FOR EACH ROW EXECUTE PROCEDURE process_servicepricess_audit();
    """,
    """
        CREATE TRIGGER reservation_change
        AFTER INSERT OR UPDATE OR DELETE ON rezervation
        FOR EACH ROW EXECUTE PROCEDURE log_reservations();
    """,
    """
        CREATE TRIGGER post_change
        AFTER INSERT OR UPDATE OR DELETE ON posts
        FOR EACH ROW EXECUTE PROCEDURE log_posts();
    """
]

def initialize(url):
    with dbapi2.connect(url) as connection:
        print("Creating types")
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            try:
                cursor.execute(statement)
            except:
                print("Types already exists, to recreate please drop it")
        cursor.close()
        print("Created all of the tables")

    with dbapi2.connect(url) as connection:
        print("Creating tables")
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
        cursor.close()
        print("Created all of the tables")

    with dbapi2.connect(url) as connection:
        print("Creating functions")
        cursor = connection.cursor()
        for statement in stored_functions:
            cursor.execute(statement)
        cursor.close()
        print("Created all functions")

    with dbapi2.connect(url) as connection:
        print("Creating triggers")
        cursor = connection.cursor()
        for statement in stored_triggers:
            try:
                cursor.execute(statement)
            except:
                print("trigger already exists, to recreate please drop it")
        cursor.close()
        print("Created all triggers")
        

if __name__ == "__main__":
    url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    initialize(url)
