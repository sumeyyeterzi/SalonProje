Parts Implemented by Ahmet Semih Uçan
=====================================

My Tables in Database
---------------------

In this project, I was responsible for 3 tables. These tables were people, berber and owner tables. In people table, username and mail are unique so I wrote code by checking these rules.


People Table

=====  ========  ============   ======   ==============   ======   ======
id     username  name_surname	mail	 password_hash	  gender   age
=====  ========  ============   ======   ==============   ======   ======
5      berberr	 Hasan Berber   a@g.cm   Hash             m        21
=====  ========  ============   ======   ==============   ======   ======

Berber Table

===  =========  ========   ========   ========     ======  =======    ======
id   people_id  bshop_id   g_choice   exp_year     s_time  f_time     rates
===  =========  ========   ========   ========     ======  =======    ======
2    #4         #23        unisex     8            8       17         3
===  =========  ========   ========   ========     ======  =======    ======

Owner Table

=====  =========    =========   =============   ==========  =============== ========
id     people_id    tc_number   serial_number   vol_number  family_order_no order_no
=====  =========    =========   =============   ==========  =============== ========
4       #5          123134433   123             234         435             345
=====  =========    =========   =============   ==========  =============== ========


Entity Classes
--------------
In this project, I created 3 classes to send and receive data as object. My fundamental classes' name are People, Berber and Owner.
In these classes, I write constructors to assign initial values to the object. These classes' codes are below.

.. code-block:: python

   class People:
    def __init__(self):
        self.id = None
        self.username = None
        self.name_surname = None
        self.mail = None
        self.password_hash = None
        self.gender = None
        self.age = None
        self.role = None
        self.active = True

    def get_id(self):
        return self.username

    @property
    def is_active(self):
        return self.active


.. code-block:: python

    class Berber:
        def __init__(self):
            self.id = None
            self.people_id = None
            self.berber_shop_id = None
            self.gender_choice = None
            self.experience_year = None
            self.start_time = None
            self.finish_time = None
            self.rates = None
            self.people = None #will be used for reaching berber's people attributes for berbershop_view page


.. code-block:: python

    class Owner:
        def __init__(self):
            self.id = None
            self.people_id = None
            self.tc_number = None
            self.serial_number = None
            self.vol_number = None
            self.family_order_no = None
            self.order_no = None

Database Init
-------------
The following initialize function in dbinit.py was running when the site was opened. This function was running to create tables with SQL codes that I kept in the variable INIT_STATEMENT in the database.


.. code-block:: python

    def initialize(url):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            for statement in INIT_STATEMENTS:
                cursor.execute(statement)
            cursor.close()



.. code-block:: python

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
        CREATE TABLE IF NOT EXISTS Berber(
            id SERIAL PRIMARY KEY,
            people_id INTEGER REFERENCES People(id) ON DELETE CASCADE,
            berbershop_id INTEGER DEFAULT NULL REFERENCES Berbershop(id) ON DELETE SET NULL,
            gender_choice VARCHAR(10),
            experience_year INTEGER DEFAULT 0,
            start_time INTEGER,
            finish_time INTEGER,
            rates INTEGER DEFAULT 0
        )
        """,
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
        """
    ]


In this project, I have written SQL codes, such as read, insertion, deleting, updating in functions for each table separately. I used the necessary functions in views.py. I have created 3 different classes named Peoplemodel, Berbermodel, and Ownermodel for People, Berber and Owner tables. I wrote the CRUD queries in these classes. I have used the necessary actions by calling the functions I prepared in views.py.

People Model
------------

Here are some examples of functions that I use in the model

.. code-block:: python

    class Peoplemodel:

        # Insert Function
         def insert(self, people):
            with dbapi2.connect(url) as connection:
                cursor = connection.cursor()
                cursor.execute("""INSERT INTO People (username, name_surname, mail, password_hash, gender, age,role)
                               VALUES (%s , %s , %s , %s , %s , %s,  %s )""", (
                people.username, people.name_surname, people.mail, people.password_hash, people.gender, people.age,
                people.role))

        # Read Function for admin panel
        def get_all_list(self):
            with dbapi2.connect(url) as connection:
                cursor = connection.cursor()
                cursor.execute(""" SELECT * from people""")
                people_list = []
                rows = cursor.fetchall()
                for i in rows:
                    person = People()
                    person.id = i[0]
                    person.username = i[1]
                    person.name_surname = i[2]
                    person.mail = i[3]
                    person.password_hash = i[4]
                    person.gender = i[5]
                    person.age = i[6]
                    person.role = i[7]
                    person.active = True
                    people_list.append(person)
                return people_list

        # Delete Id
        def delete_id(self, id):
            with dbapi2.connect(url) as connection:
                cursor = connection.cursor()
                cursor.execute("DELETE FROM People where id = %s", (id,))

        # Update
        def update(self, people):
            if self.control_exist_to_update(people) == False:
                with dbapi2.connect(url) as connection:
                    cursor = connection.cursor()
                    cursor.execute("""UPDATE People SET username = %s, name_surname = %s, mail = %s, password_hash = %s, gender = %s, age = %s where id = %s""",
                                   (people.username, people.name_surname, people.mail, people.password_hash, people.gender, people.age, people.id))
                return True
            else:
                return False


The function is used to update. The difference of control exist and control_exist_to_update is that control_exist_to_update don't considers self existence.

.. code-block:: python

         # The function control exist of people with username and mail.
         def control_exist(self, people):
                with dbapi2.connect(url) as connection:
                    cursor = connection.cursor()
                    cursor.execute("SELECT * FROM People where username = %s or mail = %s ", (people.username, people.mail))
                row = cursor.fetchone()
                if (row == None):
                    return False
                return True

         def control_exist_to_update(self, people):
            with dbapi2.connect(url) as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT id FROM People where username = %s or mail = %s ", (people.username, people.mail))
            row = cursor.fetchall()
            if (row == None):
                return False
            elif len(row) > 1:
                return True
            elif len(row) == 1 and row[0][0]==people.id:
                return False
            return True

         def save(self, people):
            if (self.control_exist(people) == False):
                self.insert(people)
                return True
            else:
                return False


I did the reading from the database with the following functions. With get_role function, role information can be obtained from the username.
The get_all function allows you to obtain a people object from the username.

.. code-block:: python

         def get_role(self, username):
            with dbapi2.connect(url) as connection:
                cursor = connection.cursor()
                cursor.execute("""    SELECT role from people where username = %s
                                       """, (username,))
                role = cursor.fetchone()[0]
                return role

         def get_all(self, username):
            with dbapi2.connect(url) as connection:
                cursor = connection.cursor()
                cursor.execute(""" SELECT * from people where username = %s
                                       """, (username,))
                person = People()
                rows = cursor.fetchall()
                if len(rows) == 0:
                    return person
                person.id = rows[0][0]
                person.username = rows[0][1]
                person.name_surname = rows[0][2]
                person.mail = rows[0][3]
                person.password_hash = rows[0][4]
                person.gender = rows[0][5]
                person.age = rows[0][6]
                person.role = rows[0][7]
                person.active = True
                return person

Berber Model
------------

.. code-block:: python

    class Berbermodel:

        # Read function
        def get_id(self, username):
            with dbapi2.connect(url) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                                SELECT id FROM PEOPLE WHERE username = %s
                                """, (username, ))
            row = cursor.fetchone()
            return row

        # Insert function
        def insert(self, berber):
                with dbapi2.connect(url) as connection:
                    cursor = connection.cursor()
                    cursor.execute("""INSERT INTO Berber (people_id, gender_choice, experience_year, start_time, finish_time, rates)
                                     VALUES (%s , %s , %s , %s , %s , %s )""", (berber.people_id, berber.gender_choice, berber.experience_year,
                                                                                     berber.start_time, berber.finish_time, berber.rates))
        # Delete function
        def delete_with_people_id(self, id):
            with dbapi2.connect(url) as connection:
                cursor = connection.cursor()
                cursor.execute("DELETE FROM Berber where people_id = %s", (id,))

        # Update function
        def update_berber(self, berber):
            with dbapi2.connect(url) as connection:
                cursor = connection.cursor()
                cursor.execute(
                    """UPDATE Berber SET gender_choice = %s, experience_year = %s, start_time = %s, finish_time = %s  where people_id = %s""",
                    (berber.gender_choice, berber.experience_year, berber.start_time, berber.finish_time, berber.people_id))
            return True

        # Read function
        def get_all_list(self):
            with dbapi2.connect(url) as connection:
                cursor = connection.cursor()
                cursor.execute(""" SELECT * from berber""")
                berber_list = []
                rows = cursor.fetchall()
                for i in rows:
                    berber = Berber()
                    berber.id = i[0]
                    berber.people_id = i[1]
                    berber.berber_shop_id = i[2]
                    berber.gender_choice = i[3]
                    berber.experience_year = i[4]
                    berber.start_time = i[5]
                    berber.finish_time = i[6]
                    berber.rates = i[7]
                    berber_list.append(berber)
                return berber_list


get_all_list() function is used in admin panel to list all berbers on panel.

.. code-block:: python

        def get_all_list(self):
            with dbapi2.connect(url) as connection:
                cursor = connection.cursor()
                cursor.execute(""" SELECT * from berber""")
                berber_list = []
                rows = cursor.fetchall()
                for i in rows:
                    berber = Berber()
                    berber.id = i[0]
                    berber.people_id = i[1]
                    berber.berber_shop_id = i[2]
                    berber.gender_choice = i[3]
                    berber.experience_year = i[4]
                    berber.start_time = i[5]
                    berber.finish_time = i[6]
                    berber.rates = i[7]
                    berber_list.append(berber)
                return berber_list

Owner Model
-----------

.. code-block:: python

    class Ownermodel:
        #Read function to get id with username
        def get_id(self, username):
            with dbapi2.connect(url) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                                SELECT id FROM PEOPLE WHERE username = %s
                                """, (username,))
            row = cursor.fetchone()
            return row

        #Insert function with owner object
        def insert(self, owner):
            with dbapi2.connect(url) as connection:
                cursor = connection.cursor()
                cursor.execute("""INSERT INTO Owner (people_id, tc_number, serial_number, vol_number, family_order_no, order_no)
                                VALUES (%s , %s , %s , %s , %s , %s )""", (owner.people_id, owner.tc_number, owner.serial_number, owner.vol_number, owner.family_order_no, owner.order_no))

        #Delete function with id
        def delete_with_people_id(self, id):
            with dbapi2.connect(url) as connection:
                cursor = connection.cursor()
                cursor.execute("DELETE FROM Owner where people_id = %s", (id,))

        #Update function with owner object
        def update_owner(self, owner):
            with dbapi2.connect(url) as connection:
                cursor = connection.cursor()
                cursor.execute(
                    """UPDATE Owner SET tc_number = %s, serial_number = %s, vol_number = %s, family_order_no = %s, order_no = %s  where people_id = %s""",
                    (owner.tc_number, owner.serial_number, owner.vol_number, owner.family_order_no, owner.order_no, owner.people_id))
            return True

        #Control function the duplicate tc_number for validation
        def control_exist_tc(self, tc):
            with dbapi2.connect(url) as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM Owner where tc_number = %s ", (tc, ))
            row = cursor.fetchone()
            if (row == None):
                return False
            return True

        #Read function all owners
        def get_all_list(self):
            with dbapi2.connect(url) as connection:
                cursor = connection.cursor()
                cursor.execute(""" SELECT * from owner""")
                owner_list = []
                rows = cursor.fetchall()
                for i in rows:
                    owner = Owner()
                    owner.id = i[0]
                    owner.people_id = i[1]
                    owner.tc_number = i[2]
                    owner.serial_number = i[3]
                    owner.vol_number = i[4]
                    owner.family_order_no = i[5]
                    owner.order_no = i[6]
                    owner_list.append(owner)
                return owner_list

Used libraries
--------------

.. code-block:: python

    from flask import render_template, Flask, request, redirect, url_for, current_app
    from passlib.hash import pbkdf2_sha256 as hasher
    from flask_login import LoginManager, login_user, logout_user, current_user

Functions in views.py
---------------------
I have built the signup_register_type, signup, signin and admin_panel pages with the following functions.

.. code-block:: python

    def signupbase_page():
        if request.method == 'GET':
            return render_template("register_type.html")
        else:
            if request.form['submit_button'] == 'user':
                return redirect(url_for('signup_user_page'))
            elif request.form['submit_button'] == 'berber':
                return redirect(url_for('signup_berber_page'))
            elif request.form['submit_button'] == 'owner':
                return redirect(url_for('signup_owner_page'))
            return render_template("profile.html")

    def signup_berber_page():
        if request.method == 'GET':
            return render_template("signup_berber.html")
        else:
            person = People()
            person.username = request.form["username"]
            person.name_surname = request.form["name_surname"]
            person.mail = request.form["mail"]
            person.password_hash = hasher.hash(request.form["password"])
            person.gender = request.form["gender"]
            person.age = request.form["age"]
            person.role = "berber"
            people = Peoplemodel()

            if (people.control_exist(person)):
                return render_template("signup_berber.html", message="False")
            else:
                people.save(person)
                berbers = Berbermodel()
                berber = Berber()
                berber.people_id = berbers.get_id(person.username)[0]
                berber.gender_choice = request.form["gender_choice"]
                berber.experience_year = request.form["experience"]
                berber.start_time = request.form["start_time"][:2]
                berber.finish_time = request.form["finish_time"][:2]
                berbers.insert(berber)
                return render_template("signup_berber.html", message="True")

            return redirect(url_for("signup_berber_page"))


    def signup_owner_page():
        if request.method == 'GET':
            return render_template("signup_owner.html")
        else:
            person = People()
            person.username = request.form["username"]
            person.name_surname = request.form["name_surname"]
            person.mail = request.form["mail"]
            person.password_hash = hasher.hash(request.form["password"])
            person.gender = request.form["gender"]
            person.age = request.form["age"]
            person.role = "owner"
            people = Peoplemodel()
            if(people.control_exist(person)):
                return render_template("signup_owner.html", message="False")
            else:
                owners = Ownermodel()
                owner = Owner()
                owner.tc_number = request.form["tc_number"]
                owner.serial_number = request.form["serial_number"]
                owner.vol_number = request.form["vol_number"]
                owner.family_order_no = request.form["family_order_no"]
                owner.order_no = request.form["order_no"]
                if(owners.control_exist_tc(owner.tc_number)):
                    return render_template("signup_owner.html", message="The TC Number has been saved already ")
                elif(len(owner.tc_number)!=11):
                    return render_template("signup_owner.html", message="TC Number Length must be 11 digits")
                elif(len(owner.serial_number)!=3):
                    return render_template("signup_owner.html", message="Serial number must be 3 digits")
                elif (len(owner.vol_number) != 3):
                    return render_template("signup_owner.html", message="Vol number must be 3 digits")
                elif (len(owner.family_order_no) != 3):
                    return render_template("signup_owner.html", message="Family order number must be 3 digits")
                elif (len(owner.order_no) != 3):
                    return render_template("signup_owner.html", message="Order number must be 3 digits")
                else:
                    people.save(person)
                    owner.people_id = owners.get_id(person.username)[0]
                    owners.insert(owner)
                    #tc kimlik varlığını kontrolü
                    return render_template("signup_owner.html", message="True")
            return redirect(url_for("signup_owner_page"))


    def signup_user_page():
        if request.method == 'GET':
            return render_template("signup_user.html", message="")
        else:
            person = People()
            person.username = request.form["username"]
            person.name_surname = request.form["name_surname"]
            person.mail = request.form["mail"]
            person.password_hash = hasher.hash(request.form["password"])
            person.gender = request.form["gender"]
            person.age = request.form["age"]
            person.role = "user"

            people = Peoplemodel()
            if (people.save(person)):
                return render_template("signup_user.html", message="True")
            else:
                return render_template("signup_user.html", message="False")
            return redirect(url_for("signup_user_page"))


    def signin():
        if request.method == 'GET':
            return render_template("signin.html", message="")
        else:
            username = request.form["username"]
            password = request.form["password"]
            people = Peoplemodel()

            #Eğer kullanıcı databasede ekli değilse patlar //Düzeltildi
            if(people.control_exist_username(username)):
                person = People()
                person = people.get_all(username)

                if(hasher.verify(password, person.password_hash)):
                    login_user(person)
                    current_app.config["LOGGED_USERS"][person.username] = person

                    return render_template("signin.html", message="True", role=people.get_role(username))
                else:
                    return render_template("signin.html", message="False")
            else:
                return render_template("signin.html", message="False")

    def signout():
        logout_user()
        return redirect(url_for("home_page"))

    def admin_panel():
        peoples = []
        people = Peoplemodel()
        berbers = Berbermodel()
        owners = Ownermodel()
        peoples = people.get_all_list()
        berber_list = []
        berber_list = berbers.get_all_list()
        owner_list = []
        owner_list = owners.get_all_list()

        if request.method == 'GET':
            if (current_user.role == "admin"):
                return render_template("admin_panel.html", people=peoples, berbers=berber_list, owners=owner_list)
            else:
                return render_template("signin.html", message="admin_error")
        else:
            if request.form["edit"]=="delete":
                form_movie_keys = request.form.getlist("people_keys")
                for i in form_movie_keys:
                    for j in peoples:
                        if j.id == int(i) and j.role == "user":
                            people.delete_id(j.id)
                        elif j.id == int(i) and j.role == "berber":
                            berbers.delete_with_people_id(j.id)
                            people.delete_id(j.id)
                        elif j.id == int(i) and j.role == "owner":
                            owners.delete_with_people_id(j.id)
                            people.delete_id(j.id)

            elif "update" in request.form["edit"]:
                for i in peoples:
                    x = request.form["edit"].split("_")[0]
                    if int(x) == i.id:
                        person = People()
                        person.username = request.form["username"]
                        person.name_surname = request.form["name_surname"]
                        person.mail = request.form["mail"]
                        person.password_hash = hasher.hash(request.form["password"])
                        person.gender = request.form["gender"]
                        person.age = request.form["age"]
                        person.role = "user"
                        person.id = i.id

                        #Validation
                        if len(person.name_surname)>50 or len(person.username) >50 or len(person.mail)>300:
                            return render_template("update.html", person=i, message="You should check input validations.")

                        if i.role == "user" or i.role == "admin":
                            if(people.update(person)):
                                return render_template("admin_panel.html", people=peoples, berbers=berber_list,owners=owner_list, message="True")
                            else:
                                return render_template("admin_panel.html", people=peoples, berbers=berber_list,owners=owner_list, message="False")
                        elif i.role == "berber":
                            berbers = Berbermodel()
                            berber = Berber()
                            berber.people_id = i.id
                            berber.gender_choice = request.form["gender_choice"]
                            berber.experience_year = request.form["experience"]
                            berber.start_time = request.form["start_time"][:2]
                            berber.finish_time = request.form["finish_time"][:2]
                            berbers = Berbermodel()
                            people.update(person)
                            berbers.update_berber(berber)
                            return render_template("admin_panel.html", people=peoples, berbers=berber_list, owners=owner_list, message="True")
                        elif i.role == "owner":
                            owner = Owner()
                            owner.people_id = owners.get_id(person.username)[0]
                            owner.tc_number = request.form["tc_number"]
                            owner.serial_number = request.form["serial_number"]
                            owner.vol_number = request.form["vol_number"]
                            owner.family_order_no = request.form["family_order_no"]
                            owner.order_no = request.form["order_no"]
                            if (owners.control_exist_tc(owner.tc_number)):
                                return render_template("admin_panel.html", people=peoples, berbers=berber_list, owners=owner_list, message="False")
                            people.update(person)
                            owners.update_owner(owner)
                            return render_template("admin_panel.html", people=peoples, berbers=berber_list, owners=owner_list, message="True")

            elif "order_id" in request.form["edit"]:
                peoples = sorted(peoples, key=lambda people: people.id)   # sort by age
                return render_template("admin_panel.html", people=peoples, berbers=berber_list, owners=owner_list)

            elif "order_username" in request.form["edit"]:
                peoples = sorted(peoples, key=lambda people: people.username)  # sort by age
                return render_template("admin_panel.html", people=peoples, berbers=berber_list, owners=owner_list)

            elif "order_role" in request.form["edit"]:
                peoples = sorted(peoples, key=lambda people: people.role)  # sort by age
                return render_template("admin_panel.html", people=peoples, berbers=berber_list, owners=owner_list)
            else:
                for i in peoples:
                    if int(request.form["edit"]) == i.id:
                        return render_template("update.html", person=i)
            return redirect(url_for("admin_panel"))


Validation Examples
-------------------
I checked validation of inputs with control blocks. Validation examples are below.

.. code-block:: python

    if len(person.name_surname)>50 or len(person.username) >50 or len(person.mail)>300:
        return render_template("update.html", person=i, message="You should check input validations.")

    if(owners.control_exist_tc(owner.tc_number)):
                    return render_template("signup_owner.html", message="The TC Number has been saved already ")
                elif(len(owner.tc_number)!=11):
                    return render_template("signup_owner.html", message="TC Number Length must be 11 digits")
                elif(len(owner.serial_number)!=3):
                    return render_template("signup_owner.html", message="Serial number must be 3 digits")
                elif (len(owner.vol_number) != 3):
                    return render_template("signup_owner.html", message="Vol number must be 3 digits")
                elif (len(owner.family_order_no) != 3):
                    return render_template("signup_owner.html", message="Family order number must be 3 digits")
                elif (len(owner.order_no) != 3):
                    return render_template("signup_owner.html", message="Order number must be 3 digits")
                else:
                    people.save(person)
                    owner.people_id = owners.get_id(person.username)[0]
                    owners.insert(owner)
