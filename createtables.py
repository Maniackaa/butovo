import psycopg2


class DB:
    def __init__(self, dbname, user, password, host):
        self.connection = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, sslmode='disable')
        self.cursor = self.connection.cursor()
        self.connection.autocommit = True

    def create(self):
        with self.connection:
            self.cursor.execute('''CREATE TABLE public.box
(
    id serial NOT NULL,
    user_id bigint,
    goodid bigint,
    PRIMARY KEY (id)
);''')

            self.cursor.execute('''CREATE TABLE public.categories
(
    id serial NOT NULL,
    name character varying,
    vladimir character varying DEFAULT 'no',
    skolkovo character varying DEFAULT 'no',
    vidnoe character varying DEFAULT 'no',
    sovhoz character varying DEFAULT 'no',
    miti character varying DEFAULT 'no',
    domod character varying DEFAULT 'no',
    moscow character varying DEFAULT 'no',
    PRIMARY KEY (id)
);''')

            self.cursor.execute('''CREATE TABLE public.subcatgoods
(
    id serial NOT NULL,
    categoryid bigint,
    name character varying,
    subcatid bigint,
    type character varying,
    description character varying,
    photo character varying,
    price_vladimir character varying DEFAULT '0',
    price_skolkovo character varying DEFAULT '0',
    price_vidnoe character varying DEFAULT '0',
    price_sovhoz character varying DEFAULT '0',
    price_miti character varying DEFAULT '0',
    price_domod character varying DEFAULT '0',
    price_moscow character varying DEFAULT '0',
    PRIMARY KEY (id)
);''')

            self.cursor.execute('''CREATE TABLE public.users
(
    id serial NOT NULL,
    user_id bigint,
    PRIMARY KEY (id)
);''')


DB('botblyda', 'postgres', '123321', 'localhost').create()