Parts Implemented by Ertugrul Semiz
=====================================

My Tables in Database
---------------------
Comments  Table

=====  =========  ==============  ==========  ================  ==============  ======  ==========================  ============  ===============  ===========================
id     people_id  berber          berbershop  title	        content         rate    date_time                   comment_like  comment_dislike  keywords
=====  =========  ==============  ==========  ================  ==============  ======  ==========================  ============  ===============  ===========================
25     87	  NULL            13          izmirin en iyisi  gayet begendik  4       2019-12-14 21:02:56.554483  0             0                Expensive,Talentless,Dirty
=====  =========  ==============  ==========  ================  ==============  ======  ==========================  ============  ===============  ===========================

Contact_info Table

===  =============  ========   ================   ===========     ==========  ===========
id   berbershop_id  type       telephone_number   facebook        twitter     instagram
===  =============  ========   ================   ===========     ==========  ===========
5    11             company    5359266963         ertugrulsm      ertugrulsm  ertugrulsmz
===  =============  ========   ================   ===========     ==========  ===========

Rezervation Table

=====  =========    =============   ==========================   ====================  =============== =========  ==========  ==============
id     people_id    berbershop_id   datetime_registration        datetime_rezervation  status          note       price_type  payment_method
=====  =========    =============   ==========================   ====================  =============== =========  ==========  ==============
1      78           11              2019-12-14 15:36:52.266049   2019-12-15 09:00:00   notokey         ordayimmm  1           creditcard
=====  =========    =============   ==========================   ====================  =============== =========  ==========  ==============

Commentlikedislike Table

===  =============  =========   ========   ==========
id   comment_id     people_id   ifliked    ifdisliked
===  =============  =========   ========   ==========
1    1              79          1          0
===  =============  =========   ========   ==========



In this project I was in charge of  4 tables. Many filter and rules added to my tables. For instance, Even though database rules does permit different length of phone numbers, i have done
validation for it to be 10 digits exactly. Also, comment title, content can not be null so it is covered also form validation.



Entity Classes
--------------

In this project, I have created 4 Entity Class representing tables in database. I have created constructors for those classes
as a initial values. Besides, 4 Model Classes are created for the purpose of managing database Create, Read, Update, Delete operations.



.. code-block:: python

   class Comment:
    def __init__(self):
        self.id = None
        self.peopleId = None
        self.berber = None
        self.berbershop = None
        self.title = ""
        self.content = ""
        self.rate = 0
        self.dateTime = datetime.now()
        self.like = 0
        self.dislike = 0
        self.peopleobj = None
        self.likedDislikedobj = None
        self.keywords = None

    class LikedDisliked:
        def __init__(self):
            self.id = None
            self.comment_id = None
            self.peopleId = None
            self.ifliked = None
            self.ifDisliked = None



    class ContactInfo:
        def __init__(self):
            self.id = None
            self.berberShopId = None
            self.type = None
            self.telephoneNumber = None
            self.facebook = None
            self.twitter = None
            self.instagram = None



    class Rezervation:
        def __init__(self):
            self.id = None
            self.peopleId = None
            self.berberShopId = None
            self.dateTimeRegistration = datetime.now()
            self.dateTimeRezervation = None
            self.status = None
            self.note = None
            self.priceType = None
            self.paymentMethod = None


Database Init
-------------
The following initialize function in dbinit.py was running when the site was opened. This function was running to create tables with SQL codes that are kept
in INIT_STATEMENT string array. Each developer's sql statements are listed here, my statements are as follows.


.. code-block:: python

    def initialize(url):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            for statement in INIT_STATEMENTS:
                cursor.execute(statement)
            cursor.close()

INIT_STATEMENT is below.

.. code-block:: python

    INIT_STATEMENTS = [
    """
    CREATE TABLE IF NOT EXISTS Comments(
        id SERIAL PRIMARY KEY,
        people_id integer NOT NULL REFERENCES People(id) ON DELETE CASCADE,
        berber integer  REFERENCES Berber(id) ON DELETE CASCADE,
        berbershop integer  REFERENCES Berbershop(id) ON DELETE CASCADE,
        title VARCHAR (100),
        content VARCHAR (500),
        rate integer  NOT NULL,
        date_time TIMESTAMP,
        comment_like integer DEFAULT 0 NOT NULL,
        comment_dislike  integer DEFAULT 0 NOT NULL,
        CHECK (rate > 0), CHECK (rate < 6)
    )""",
    #  CREATE TYPE IF NOT EXISTS type AS ENUM ('company', 'personal');
    """

    CREATE TABLE IF NOT EXISTS Contact_info(
        id SERIAL PRIMARY KEY,
        berbershop_id integer  REFERENCES Berbershop(id) ON DELETE CASCADE,
        type type,
        telephone_number VARCHAR (15) NOT NULL,
        facebook VARCHAR (500),
        twitter VARCHAR (500),
        instagram VARCHAR (500)
    )""",
    # CREATE TYPE status AS ENUM ('okey','notokey');
    #Create type method as enum ('creditcard','cash');
    """
       CREATE TABLE IF NOT EXISTS Rezervation(
           id SERIAL PRIMARY KEY,
           people_id integer NOT NULL REFERENCES People(id) ON DELETE CASCADE,
           berbershop_id integer NOT NULL REFERENCES Berbershop(id) ON DELETE CASCADE,
           datetime_registration TIMESTAMP,
           datetime_rezervation TIMESTAMP,
           status status,
           note VARCHAR (100),
           price_type integer REFERENCES ServicePrices(id) ON DELETE CASCADE,
           payment_method method
       )""",

    """
       CREATE TABLE IF NOT EXISTS CommentLikeDislike(
           id SERIAL PRIMARY KEY,
           comment_id integer NOT NULL REFERENCES Comments(id) ON DELETE CASCADE,
           people_id integer NOT NULL REFERENCES People(id) ON DELETE CASCADE,
           ifliked  integer NOT NULL,
           ifdisliked integer NOT NULL,
           CHECK (ifliked <2), CHECK (ifliked >-2), CHECK (ifdisliked <2), CHECK (ifdisliked >-2)
       )"""
    ]

Model Classes
--------------
Model Classes are the packages that includes functions runs sql statements for the corresponding entity and table.




Statistics Model
----------------
.. code-block:: python

    class StatisticsModel :
    def mostPopularBerbershops(self):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                Select s.* from (SELECT  count(*) as c, Berbershop   from comments GROUP BY Berbershop ) as j join berbershop as s on j.berbershop = s.id
                ORDER BY j.c DESC LIMIT 3
            """)
            rows = cursor.fetchall()

        berbershops = []
        for row in rows:
            berbershop = Berbershop()
            berbershop.id, berbershop.ownerpeople_id, berbershop.shopname, berbershop.location, berbershop.city, \
            berbershop.openingtime, berbershop.closingtime, berbershop.tradenumber = row[0], row[1], row[2], row[3], \
                                                                                     row[4], \
                                                                                     row[5], row[6], row[7]
            berbershops.append(berbershop)
        return berbershops

    def lastAddedBarbershops(self):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute("""
               SELECT * from berbershop ORDER BY Id DESC limit 3
            """)
            rows = cursor.fetchall()

        berbershops = []
        for row in rows:
            berbershop = Berbershop()
            berbershop.id, berbershop.ownerpeople_id, berbershop.shopname, berbershop.location, berbershop.city, \
            berbershop.openingtime, berbershop.closingtime, berbershop.tradenumber = row[0], row[1], row[2], row[3], \
                                                                                     row[4], \
                                                                                     row[5], row[6], row[7]
            berbershops.append(berbershop)
        return berbershops



Comment Model
--------------
.. code-block:: python

    class CommentModel:

        # to decide insert or update
        def save(self, comment):
            if (comment.id == None):  # if object has no id value then insert
                self.insert(comment)
            else:
                if (self.ifExist(comment.id) != True):  # object has value but if it exists in database
                    self.insert(comment)  # then insert since that object not in database
                else:
                    self.update(comment)  # it exists in database update

        # insert method that will be do insertion
        def insert(self, comment):
            with dbapi2.connect(url) as connection:
                cursor = connection.cursor()
                cursor.execute("""INSERT INTO Comments (people_id ,  berber , berbershop, title , content , rate , date_time ,
                    comment_like , comment_dislike, keywords)
                    VALUES (%s , %s, %s , %s , %s , %s , %s , %s , %s, %s)""", (comment.peopleId, comment.berber,comment.berbershop,comment.title,
                                                                        comment.content, comment.rate, comment.dateTime,
                                                                        comment.like,
                                                                        comment.dislike, comment.keywords))

        # get by id
        def getById(self, id):
            with dbapi2.connect(url) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    SELECT * from Comments as c where c.id = %s """, (id,))
                row = cursor.fetchone()

            # return one comment object
            comment = Comment()
            comment.id, comment.peopleId, comment.berber, comment.berbershop, comment.title, comment.content, comment.rate, comment.dateTime, \
            comment.like, comment.dislike = row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]
            return comment

        # get All
        def getAll(self):
            with dbapi2.connect(url) as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT * from Comments as c order by c.date_time desc")
                rows = cursor.fetchall()

            comments = []
            for row in rows:
                comment = Comment()
                comment.id, comment.peopleId, comment.berber, comment.berbershop, comment.title, comment.content, comment.rate, comment.dateTime, \
                comment.like, comment.dislike = row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]
                comments.append(comment)
            return comments



        def deleteById(self, id):
            with dbapi2.connect(url) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    DELETE from Comments where id = %s
                """, (id,))

        # update method that will do update
        def update(self, comment):
            with dbapi2.connect(url) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    UPDATE Comments SET id = %s, people_id = %s , berber = %s , berbershop =%s title = %s , content = %s ,
                    rate = %s , date_time = %s , comment_like =%s , comment_dislike = %s where id = %s""",
                               (comment.id, comment.peopleId, comment.berber, comment.berbershop, comment.title, comment.content, comment.rate,
                                comment.dateTime,
                                comment.like, comment.dislike, comment.id))

        def ifExist(self, id):
            with dbapi2.connect(url) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    SELECT * from Comments where id = %s
                """, (id,))
            row = cursor.fetchone()
            if (row == None):
                return False
            return True

        def getAllCommentswithPeopleByBerbershopId(self,id):
            with dbapi2.connect(url) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    SELECT c.*, p.id, p.username from comments as c join people as  p on c.people_id = p.id
                    WHERE c.berbershop = %s order by c.date_time desc
                """,(id,))

            rows = cursor.fetchall()
            comments = []
            for row in rows:
                comment = Comment()
                comment.id, comment.peopleId, comment.berber, comment.berbershop, comment.title, comment.content, comment.rate, comment.dateTime, \
                comment.like, comment.dislike, comment.keywords = row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8],row[9], row[10]

                people = People()
                people.id, people.username = row[11], row[12]
                comment.peopleobj = people
                comments.append(comment)
            return comments

        def commentCurrentUserRelationship(self, id, peopleid):
            with dbapi2.connect(url) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                  select com.id, com.people_id, com.ifliked, com.ifdisliked from
                   commentlikedislike as com where com.comment_id = %s and com.people_id = %s
                """,(id,peopleid))

            row = cursor.fetchone()
            likedDisliked = LikedDisliked()
            if (row == None) :
                return None
            likedDisliked.id, likedDisliked.peopleId, likedDisliked.ifliked, likedDisliked.ifDisliked= row[0], \
            row[1], row[2], row[3]
            return likedDisliked

        def updateByIdTitleTextRate(self, id, title, content, datetime, rate):
            with dbapi2.connect(url) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                           UPDATE Comments SET title = %s , content= %s, date_time = %s, rate =%s  where id = %s""",
                               (title,content,datetime,rate,id))


        def  increaseLikeNumber(self, commentid):
             with dbapi2.connect(url) as connection:
                 cursor = connection.cursor()
                 cursor.execute(""" UPDATE Comments as c SET comment_like = comment_like +1  where c.id = %s""",
                                       (commentid,))

        def increaseDislikeNumber(self, commentid):
            with dbapi2.connect(url) as connection:
                cursor = connection.cursor()
                cursor.execute(""" UPDATE Comments as c SET comment_dislike = comment_dislike +1  where c.id = %s""",
                               (commentid,))

        def decreaseDislikeNumber(self, commentid):
            with dbapi2.connect(url) as connection:
                cursor = connection.cursor()
                cursor.execute(""" UPDATE Comments as c SET comment_dislike = comment_dislike -1  where c.id = %s""",
                               (commentid,))

        def decreaseLikeNumber(self, commentid):
            with dbapi2.connect(url) as connection:
                cursor = connection.cursor()
                cursor.execute(""" UPDATE Comments as c SET comment_like = comment_like -1  where c.id = %s""",
                               (commentid,))

        def increaseLikeDecreaseDislike(self, commentid):
            with dbapi2.connect(url) as connection:
                cursor = connection.cursor()
                cursor.execute(""" UPDATE Comments as c SET comment_like = comment_like +1 , comment_dislike = comment_dislike -1
                  where c.id = %s""",
                               (commentid,))

        def decreaseLikeIncreaseDislike(self, commentid):
            with dbapi2.connect(url) as connection:
                cursor = connection.cursor()
                cursor.execute(""" UPDATE Comments as c SET comment_like = comment_like -1 , comment_dislike = comment_dislike + 1
                  where c.id = %s""",
                               (commentid,))



        def likeDislikeUpdateCondition(self,commentid, peopleid, bool , likedislikeid):
            #it is not existed
            if(bool == 1 or bool == 2):
                like , dislike = 0, 0
                if(bool == 1):
                    self.increaseLikeNumber(commentid)
                    like = 1
                else :
                    dislike = 1
                    self.increaseDislikeNumber(commentid)

                with dbapi2.connect(url) as connection:
                    cursor = connection.cursor()
                    cursor.execute("""  INSERT into CommentLikeDislike (comment_id, people_id, ifliked, ifdisliked)
                                                   values (%s, %s, %s, %s) """,
                                   (commentid, peopleid, like, dislike))


            elif (bool == 3):
                self.decreaseLikeNumber(commentid)
                with dbapi2.connect(url) as connection:
                    cursor = connection.cursor()
                    cursor.execute(""" DELETE from CommentLikeDislike as c where c.id = %s """,
                                   (likedislikeid,))






            elif (bool == 4):

                like = 0
                dislike = 1
                self.decreaseLikeIncreaseDislike(commentid)
                with dbapi2.connect(url) as connection:
                    cursor = connection.cursor()
                    cursor.execute(""" UPDATE CommentLikeDislike as c SET ifliked = %s, ifdisliked = %s where c.id = %s """,
                                   (like, dislike, likedislikeid))
            elif (bool == 5):
                like = 1
                dislike = 0
                self.increaseLikeDecreaseDislike(commentid)
                with dbapi2.connect(url) as connection:
                    cursor = connection.cursor()
                    cursor.execute(""" UPDATE CommentLikeDislike as c SET ifliked = %s, ifdisliked = %s where c.id = %s """,
                                   (like, dislike, likedislikeid))
            else :
                self.decreaseDislikeNumber(commentid)
                with dbapi2.connect(url) as connection:
                    cursor = connection.cursor()
                    cursor.execute("""DELETE from CommentLikeDislike as c where c.id = %s""",
                                   (likedislikeid,))








        def likedislikeUpdate(self, commentid, peopleid, bool , likedislikeid):

            if( likedislikeid == None): #no like-dislike exist
                like = 0
                dislike = 0
                if(bool ==1):
                    self.increaseLikeNumber(commentid)
                    like = 1
                if (bool == -1):
                    dislike = 1
                    self.increaseDislikeNumber(commentid)
                with dbapi2.connect(url) as connection:
                    cursor = connection.cursor()
                    cursor.execute("""
                                        INSERT into CommentLikeDislike (comment_id, people_id, ifliked, ifdisliked)
                                        values (%s, %s, %s, %s) """,
                                   (commentid, peopleid,like,dislike))

            else:
                if(bool == 1 or bool==-1): #delete it got notr
                    if(bool == 1) :
                        self.decreaseDislikeNumber(commentid)
                    else:
                        self.decreaseLikeNumber(commentid)
                    with dbapi2.connect(url) as connection:
                        cursor = connection.cursor()
                        cursor.execute("""DELETE from CommentLikeDislike as c where c.id = %s""",
                                       (likedislikeid,))
                else:
                    like,dislike = 0,0
                    if(bool == 2):
                        like = 1
                        self.increaseLikeDecreaseDislike(commentid)
                    else:
                        dislike = 1
                        self.decreaseLikeIncreaseDislike(commentid)
                    with dbapi2.connect(url) as connection:
                        cursor = connection.cursor()
                        cursor.execute(""" UPDATE CommentLikeDislike as c SET ifliked = %s, ifdisliked = %s where c.id = %s """,
                                       (like,dislike,likedislikeid))







ContactInfo Model
-----------------

.. code-block:: python

    class ContactInfoModel:

        #  to decide insert or update
        def save(self, comment):
            if (comment.id == None):  # if object has no id value then insert
                self.insert(comment)
            else:
                if (self.ifExist(comment.id) != True):  # object has value but if it exists in database
                    self.insert(comment)  # then insert since that object not in database
                else:
                    self.update(comment)  # it exists in database update

        # insert method that will do insertion
        def insert(self, contactInfo):
            with dbapi2.connect(url) as connection:
                cursor = connection.cursor()
                cursor.execute("""INSERT INTO Contact_info (berbershop_id , type , telephone_number , facebook , twitter ,
                        instagram)
                        VALUES ( %s , %s , %s , %s , %s , %s)""",
                               (contactInfo.berberShopId, contactInfo.type,
                                contactInfo.telephoneNumber, contactInfo.facebook, contactInfo.twitter,
                                contactInfo.instagram))

        # update method that will do update
        def update(self, contactInfo):
            with dbapi2.connect(url) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    UPDATE Contact_Info SET id = %s, berbershop_id = %s , type  =%s , telephone_number = %s ,
                    facebook = %s , twitter = %s , instagram =%s where id = %s """,
                               (contactInfo.id, contactInfo.berberShopId, contactInfo.type,
                                contactInfo.telephoneNumber,
                                contactInfo.facebook, contactInfo.twitter, contactInfo.instagram, contactInfo.id))


        # get by id
        def getById(self, id):
            with dbapi2.connect(url) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    SELECT * from Contact_info as c where c.id = %s """, (id,))
                row = cursor.fetchone()

            # return one comment object
            contactInfo = ContactInfo()
            contactInfo.id, contactInfo.berberShopId, contactInfo.type, contactInfo.telephoneNumber, \
            contactInfo.facebook, contactInfo.twitter, contactInfo.instagram = row[0], row[1], row[2], row[3], row[4], row[
                5], row[6]
            return contactInfo

        def getByBarbershopId(self,id):
            row = None
            with dbapi2.connect(url) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    SELECT * from Contact_info as c where c.berbershop_id  = %s """, (id,))
                row = cursor.fetchone()
            if row == None:
                return None

            # return one comment object
            contactInfo = ContactInfo()
            contactInfo.id, contactInfo.berberShopId, contactInfo.type, contactInfo.telephoneNumber, \
            contactInfo.facebook, contactInfo.twitter, contactInfo.instagram = row[0], row[1], row[2], row[3], row[4], \
                                                                               row[5], row[6]
            return contactInfo

        def deleteById(self, id):
            with dbapi2.connect(url) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    DELETE from Contact_info where id = %s
                """, (id,))

        # get All
        def getAll(self):
            with dbapi2.connect(url) as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT * from Contact_info as c")
                rows = cursor.fetchall()

            contacts = []
            for row in rows:
                contactInfo = ContactInfo()
                contactInfo.id, contactInfo.berberShopId, contactInfo.type, contactInfo.telephoneNumber, \
                contactInfo.facebook, contactInfo.twitter, contactInfo.instagram = row[0], row[1], row[2], row[3], row[4], \
                                                                                   row[5], row[6]
                contacts.append(contactInfo)
            return contacts

        def ifExist(self, id):
            with dbapi2.connect(url) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    SELECT * from Contact_info where id = %s
                """, (id,))
            row = cursor.fetchone()
            if (row == None):
                return False
            return True

        def getByBarbershopId (self, barbershopid):
            with dbapi2.connect(url) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                           SELECT * from Contact_info as c where c.berbershop_id = %s """, (barbershopid,))
                row = cursor.fetchone()

                # return one comment object
            if(row == None):
                return None
            contactInfo = ContactInfo()
            contactInfo.id,  contactInfo.berberShopId, contactInfo.type, contactInfo.telephoneNumber, \
            contactInfo.facebook, contactInfo.twitter, contactInfo.instagram = row[0], row[1], row[2], row[3], row[4], row[
                5], row[6]
            return contactInfo



Rezervation Model
-----------------
.. code-block:: python

    class RezervationModel:

        # to decide insert or update
        def save(self, rezervation):
            if (rezervation.id == None):  # if object has no id value then insert
                self.insert(rezervation)
            else:
                if (self.ifExist(rezervation.id) != True):  # object has value but if it exists in database
                    self.insert(rezervation)  # then insert since that object not in database
                else:
                    self.update(rezervation)  # it exists in database update

        # insert method that will do insertion
        def insert(self, rezervation):
            with dbapi2.connect(url) as connection:
                cursor = connection.cursor()
                cursor.execute("""INSERT INTO Rezervation (people_id, berbershop_id, datetime_registration, datetime_rezervation, status, note,
                        price_type, payment_method)
                        VALUES (%s , %s , %s , %s , %s , %s , %s, %s)""",
                               (rezervation.peopleId, rezervation.berberShopId, rezervation.dateTimeRegistration,
                                rezervation.dateTimeRezervation, rezervation.status, rezervation.note,
                                rezervation.priceType,rezervation.paymentMethod))
                return None

        # update method that will do update
        def updateByIdDate(self, id, daterez):
            with dbapi2.connect(url) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    UPDATE Rezervation SET datetime_rezervation = %s where id = %s """,
                               (
                                   daterez, id))

        # get by id
        def getById(self, id):
            with dbapi2.connect(url) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    SELECT * from Rezervation as r where r.id = %s """, (id,))
                row = cursor.fetchone()

            # return one comment object
            rezervation = Rezervation()
            rezervation.id, rezervation.peopleId, rezervation.berberShopId, rezervation.dateTimeRegistration, rezervation.dateTimeRezervation, \
            rezervation.status, rezervation.note, rezervation.priceType = row[0], row[1], row[2], row[3], row[4], \
                                                                          row[5], row[6], row[7]
            return rezervation

        def deleteById(self, id):
            with dbapi2.connect(url) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    DELETE from Rezervation where id = %s
                """, (id,))

        # get All
        def getAllByBarberShop(self,berbershopid,currenttime,tomorrow):
            with dbapi2.connect(url) as connection:
                cursor = connection.cursor()
                cursor.execute("""SELECT r.*, s.* from Rezervation as r left join serviceprices as s on r.price_type = s.id where r.berbershop_id = %s and r.datetime_rezervation >= %s and
                    r.datetime_rezervation < %s order by r.datetime_rezervation asc
                """,
                               (berbershopid,currenttime,tomorrow))
                rows = cursor.fetchall()
            if(rows == None):
                return  None
            rezervations = []
            for row in rows:
                rezervation = Rezervation()
                rezervation.id, rezervation.peopleId, rezervation.berberShopId, rezervation.dateTimeRegistration, rezervation.dateTimeRezervation, \
                rezervation.status, rezervation.note, rezervation.paymentMethod = row[0], row[1], row[2], row[3], row[4], \
                                                                              row[5], row[6], row[8]
                servicePrice = ServicePrice()
                servicePrice.id, servicePrice.service_name, servicePrice.price, servicePrice.duration  = row[9], row[11], row[14], row[15]
                rezervation.priceType = servicePrice
                rezervations.append(rezervation)
            return rezervations

        def ifExist(self, id):
            with dbapi2.connect(url) as connection:
                cursor = connection.cursor()
                cursor.execute("""
                    SELECT * from Rezervation where id = %s
                """, (id,))
            row = cursor.fetchone()
            if (row == None):
                return False
            return True


