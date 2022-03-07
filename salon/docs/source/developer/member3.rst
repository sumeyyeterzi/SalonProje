Parts Implemented by Fatih Mustafa Bucak
========================================

My Tables in Database
---------------------
Berbershop  Table

=======  ==================  ===========  ============  ===========  ============  ============  ============  =========
id       owner_people_id     shopname     location      city         opening_time  closing_time  trade_number  shop_logo
=======  ==================  ===========  ============  ===========  ============  ============  ============  =========
PRIMARY  INTEGER People(id)  VARCHAR(50)  VARCHAR(300)  VARCHAR(50)  TIME          TIME          NUMERIC(10)   BYTEA
=======  ==================  ===========  ============  ===========  ============  ============  ============  =========

Serviceprices Table

=======  ======================  ============  ============  ===========  ============  ========
id       shop_id                 service_name  definition    gender       price         duration
=======  ======================  ============  ============  ===========  ============  ========
PRIMARY  INTEGER Berbershop(id)  VARCHAR(50)   VARCHAR(300)  VARCHAR(10)  DECIMAL(6,2)  INTEGER
=======  ======================  ============  ============  ===========  ============  ========

Creditcards Table

=======  ==================  ===========  ===========  ==========  ==========  ==========  ============
id       people_id           name         card_number  cvv_number  last_month  last_year   created_time
=======  ==================  ===========  ===========  ==========  ==========  ==========  ============
PRIMARY  INTEGER People(id)  VARCHAR(50)  NUMERIC(16)  NUMERIC(4)  NUMERIC(2)  NUMERIC(2)  TIMESTAMP
=======  ==================  ===========  ===========  ==========  ==========  ==========  ============

Creating Tables
---------------

**dbinit.py**::

    INIT_STATEMENTS = ["""
        CREATE TABLE IF NOT EXISTS Berbershop(
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
        CREATE TABLE IF NOT EXISTS Serviceprices(
            id SERIAL PRIMARY KEY,
            shop_id INTEGER REFERENCES Berbershop(id) ON DELETE CASCADE,
            service_name VARCHAR(50),
            definition VARCHAR(300),
            gender VARCHAR(10),
            price DECIMAL(6,2),
            duration INTEGER
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
        """]

Tables are created in dbinit.py file with above SQL queries.
With initialize method in dbinit.py, these queries are executed one by one.


Classes
-------
**Berbershop class**::

        class Berbershop:
            def __init__(self):
                self.id = None
                self.shopname = None
                self.ownerpeople_id = None
                self.location = None
                self.city = None
                self.openingtime = None
                self.closingtime = None
                self.tradenumber = None
                self.campaigns = None
                self.contactInfo = None
                self.numberofemployee = None
                self.shop_logo = None

**ServicePrice class**::

        class ServicePrice:
            def __init__(self):
                self.id = None
                self.shop_id = None
                self.service_name = None
                self.definition = None
                self.gender = None
                self.price = None
                self.duration = None

**CreditCard class**::

        class CreditCard:
            def __init__(self):
                self.id = None
                self.people_id = None
                self.name = None
                self.card_number = None
                self.cvv = None
                self.last_month = None
                self.last_year = None
                self.created_time = None

These classes are used to store information from SQL tables above respectively. Some classes has more number of variable than number of column of related table. Extra variables are used store extra information after join queries with other tables.

CRUD Operations
---------------

**Berbershop Insert**::

        def insert(self, berbershop):
            with dbapi2.connect(url) as connection:
                cursor = connection.cursor()
                cursor.execute("""INSERT INTO Berbershop (
                owner_people_id, shopname, location,
                city, opening_time, closing_time,
                trade_number, shop_logo)
                VALUES (%s , %s , %s , %s , %s , %s, %s, %s)""",
                (berbershop.ownerpeople_id, berbershop.shopname,
                 berbershop.location, berbershop.city,
                 berbershop.openingtime, berbershop.closingtime,
                 berbershop.tradenumber, berbershop.shop_logo))


**Berbershop Select**::

    def get_berbershops_with_number_of_employee_by_people_owner_id(self, people_owner_id):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute("""
            SELECT s.id, s.owner_people_id, s.shopname, s.location, s.city,
            s.opening_time, s.closing_time, s.trade_number, count(b.id)
            from Berbershop s left join Berber b
            on s.id = b.berbershop_id
            where s.owner_people_id = %s group by s.id""",
            (people_owner_id,))
            rows = cursor.fetchall()

        berbershops = []
        for row in rows:
            berbershop = Berbershop()
            berbershop.id, berbershop.ownerpeople_id, berbershop.shopname, berbershop.location, berbershop.city, \
            berbershop.openingtime, berbershop.closingtime, berbershop.tradenumber, berbershop.numberofemployee = \
            row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]

            berbershops.append(berbershop)
        return berbershops

**Berbershop Update**::

        def update(self, barbershop):
            with dbapi2.connect(url) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    UPDATE Berbershop SET shopname = %s, location = %s, city = %s,
                    opening_time = %s, closing_time = %s, trade_number = %s where id = %s""",
                    (barbershop.shopname, barbershop.location, barbershop.city,
                    barbershop.openingtime, barbershop.closingtime, barbershop.tradenumber,
                    barbershop.id))

**Berbershop Delete**::

        def delete_barbershop(self, id):
            with dbapi2.connect(url) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    DELETE from Berbershop where id = %s
                """, (id,))


**ServicePrice Insert**::

        def insert(self, serviceprice):
            with dbapi2.connect(url) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                INSERT INTO Serviceprices (shop_id, service_name, definition, gender, price, duration)
                                 VALUES (%s , %s , %s , %s , %s , %s)""", (
                                 serviceprice.shop_id, serviceprice.service_name,
                                 serviceprice.definition, serviceprice.gender,
                                 serviceprice.price, serviceprice.duration))


**ServicePrice Select**::

    def listByBerberShop(self,berbershopid):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute("""SELECT * from serviceprices where shop_id = %s """,
                           (berbershopid,))

        rows = cursor.fetchall()

        services = []
        for row in rows:
            sv = ServicePrice()
            sv.id = row[0]
            sv.shop_id = row[1]
            sv.service_name = row[2]
            sv.definition = row[3]
            sv.gender = row[4]
            sv.price = row[5]
            sv.duration = row[6]
            services.append(sv)
        return services

**ServicePrice Update**::

        def update(self, service_price):
            with dbapi2.connect(url) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    UPDATE Serviceprices SET service_name = %s, definition = %s,
                    gender = %s, price = %s, duration = %s where id = %s""",
                               (service_price.service_name, service_price.definition,
                               service_price.gender, service_price.price,
                                service_price.duration, service_price.id))


**ServicePrice Delete**::

    def delete_list_of_service(self, tuple):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                DELETE from Serviceprices where id in %s
            """, (tuple,))

**CreditCard Insert**::

    def insert(self, credit_card):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute("""
            INSERT INTO Creditcards
            (people_id, name, card_number, cvv_number, last_month, last_year, created_time)
                             VALUES (%s , %s , %s , %s , %s , %s, %s )""",
                             (credit_card.people_id, credit_card.name,
                             credit_card.card_number,
                             credit_card.cvv, credit_card.last_month,
                             credit_card.last_year,
                             credit_card.created_time))

**CreditCard Select**::

    def get_all_credit_cards_of_a_person(self, user_id):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute(""" SELECT * from Creditcards where people_id = %s order by id""", (user_id,))
            creditcards_list = []
            rows = cursor.fetchall()
            for i in rows:
                creditcard = CreditCard()
                creditcard.id = i[0]
                creditcard.people_id = i[1]
                creditcard.name = i[2]
                creditcard.card_number = i[3]
                creditcard.cvv = i[4]
                creditcard.last_month = i[5]
                creditcard.last_year = i[6]
                creditcard.created_time = i[7]
                if creditcard.created_time is not None:
                    creditcard.created_time = (str(creditcard.created_time))[0:16]
                creditcards_list.append(creditcard)
            return creditcards_list

**CreditCard Update**::

    def update(self, credit_card):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute("""
            UPDATE Creditcards SET name = %s,
            card_number = %s, cvv_number = %s,
            last_month = %s, last_year = %s where id = %s""",
            (credit_card.name, credit_card.card_number,
            credit_card.cvv, credit_card.last_month,
            credit_card.last_year, credit_card.id))


**CreditCard Update**::

    def delete_credit_card(self, id):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                DELETE from Creditcards where id = %s
            """, (id,))


Validation
----------

I used html form types to provide validation generally. However, I wrote some javascript code for credit card form validation.

**Card Number Validation**::

    var cardno = document.getElementById("cardno");
    cardno.addEventListener('input', function(evt) {
        var res = "";
        var temp = 0;
        for (var i = 0; i < cardno.value.length; i++) {
            if (cardno.value[i] <= "9" && cardno.value[i] >= "0") {
                res = res + cardno.value[i];
                temp = temp + 1;
            }
            if (temp == 4) {
                res = res + " ";
                temp = 0;
            }
        }
        if (cardno.value.length < 19) {
            cardno.value = res;
        }
    });

When card number text box is changed, addEventListener method is called automatically. It regulates the typed numbers for grouping 4 digits as shown normal credit card.

**Valid Thru Validation**::

    var thru = document.getElementById("thru");
    thru.addEventListener('input', function(evt) {
        var res = "";
        var temp = 0;
        for (var i = 0; i < thru.value.length; i++) {
            if (thru.value[i] <= "9" && thru.value[i] >= "0") {
                res = res + thru.value[i];
                temp = temp + 1;
            }
            if (temp == 2) {
                res = res + "/";
                temp = 0;
            }
        }
        if (thru.value.length < 5) {
            thru.value = res;
        }

    });

When thru text box is changed, addEventListener method is called automatically. It automaticly puts "/" character after two digits.
