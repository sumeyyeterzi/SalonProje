Parts Implemented by Halis Ibrahim Aydin
========================================

My Tables in Database
---------------------

Posts  Table

==================  ==============================  =============  ================  ==============  ==============  =============  ================
id                  people_id                       post_title     post_content      like_number     dislike_number  subject        date_time
==================  ==============================  =============  ================  ==============  ==============  =============  ================
SERIAL PRIMARY KEY  INTEGER REFERENCES People(id)   VARCHAR(50)    VARCHAR(500)      INTEGER         INTEGER         VARCHAR(20)    TIMESTAMP
==================  ==============================  =============  ================  ==============  ==============  =============  ================

Post_comment Table

==================  ============================  ==============================   =============  ================  ==============  ==============   ================
id                  post_id                       people_id                        post_title     post_content      like_number     dislike_number   date_time
==================  ============================  ==============================   =============  ================  ==============  ==============   ================
SERIAL PRIMARY KEY  INTEGER REFERENCES Posts(id)  INTEGER REFERENCES People(id)	   VARCHAR(50)    VARCHAR(500)      INTEGER         INTEGER          TIMESTAMP
==================  ============================  ==============================   =============  ================  ==============  ==============   ================

Campaigns Table

==================  =================================  =============  ================  ==============  ==============  =============
id                  barbershop_id                      campaign_name  definition        start_date      end_date        discount
==================  =================================  =============  ================  ==============  ==============  =============
SERIAL PRIMARY KEY  INTEGER REFERENCES Berbershop(id)  VARCHAR(50)    VARCHAR(200)      TIMESTAMP       TIMESTAMP       INTEGER
==================  =================================  =============  ================  ==============  ==============  =============


Entity Classes
--------------
In this project, I have created 3 Entity Class representing tables in database. I have created constructors for those classes
as a initial values. Therefore 4 Model Classes are created for the purpose of managing database Create, Read, Update, Delete operations.

**Entity classes**::

    class Post:
        def __init__(self):
            self.id = None
            self.people_id = None
            self.post_title = None
            self.post_content = None
            self.like = None
            self.dislike = None
            self.subject = None
            self.date_time = None
            self.comments = None

    class Post_comment:
        def __init__(self):
            self.id = None
            self.post_id = None
            self.people_id = None
            self.title = None
            self.content = None
            self.like = 0
            self.dislike = 0
            self.date_time = None

    class Campaign:
        def __init__(self):
            self.id = None
            self.barbershop_id = None
            self.campaign_name = None
            self.definition = None
            self.start_date = None
            self.end_date = None
            self.discount = None


Database Init
-------------

**Database Init**::

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
        barbershop_id integer  REFERENCES Berbershop(id) ON DELETE CASCADE,
        campaign_name VARCHAR(50),
        definition VARCHAR(200),
        start_date TIMESTAMP,
        end_date TIMESTAMP,
        discount integer
    )
    """

Model Classes
--------------
Model Classes are packages that contain functions that run SQL statements for the corresponding entity and table.

Posts Model
-----------

**Postsmodel class**::

    def insert(self,post):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute("""INSERT INTO Posts (people_id, post_title, post_content, like_number, dislike_number, subject, date_time)
                            VALUES(%s, %s, %s, %s, %s, %s, %s) """, (post.people_id, post.post_title, post.post_content,
                                                                     post.like, post.dislike, post.subject, post.date_time))

    def getAll(self):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute("""SELECT * from Posts p left join post_comment c
                                        on p.id = c.post_id order by p.id desc """)
            rows = cursor.fetchall()

        posts = []
        previus = -1
        for row in rows:
            if row[0] != previus:
                post = Post()
                post.id, post.people_id, post.post_title, post.post_content, post.like, post.dislike, post.subject, post.date_time = row[0], row[1], row[2], row[3], row[4],row[5],row[6],row[7]
                post.comments = []
                if row[8] is not None:
                    comment = Post_comment()
                    comment.id = row[8]
                    comment.post_id = row[9]
                    comment.people_id = row[10]
                    comment.title = row[11]
                    comment.content = row[12]
                    comment.like_number = row[13]
                    comment.dislike_number = row[14]
                    comment.date_time = row[15]
                    post.comments.append(comment)
                posts.append(post)
                previus = post.id
            else:
                comment = Post_comment()
                comment.id = row[8]
                comment.post_id = row[9]
                comment.people_id = row[10]
                comment.title = row[11]
                comment.content = row[12]
                comment.like_number = row[13]
                comment.dislike_number = row[14]
                comment.date_time = row[15]
                posts[len(posts) - 1].comments.append(comment)
        return posts

    def delete_post(self, id):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                DELETE from Posts where id = %s
            """, (id,))

    def  increaseLikeNumber(self, id):
         with dbapi2.connect(url) as connection:
             cursor = connection.cursor()
             cursor.execute(""" UPDATE Posts as c SET like_number = like_number +1  where c.id = %s""",
                                   (id,))

    def increaseDislikeNumber(self, id):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute(""" UPDATE Posts as c SET dislike_number = dislike_number +1  where c.id = %s""",
                           (id,))

PostComment Model
-----------------

**PostCommentmodel class**::

    def insert(self,post_comment):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute("""INSERT INTO post_comment (post_id, people_id, title, content, like_number, dislike_number, date_time)
                            VALUES(%s, %s, %s, %s, %s, %s, %s) """, (post_comment.post_id, post_comment.people_id, post_comment.title, post_comment.content,
                                                                     post_comment.like, post_comment.dislike, post_comment.date_time))

    def increaseLikeNumber(self, id):
        with dbapi2.connect(url) as connection:
             cursor = connection.cursor()
             cursor.execute(""" UPDATE post_comment as c SET like_number = like_number +1  where c.id = %s""",
                                   (id,))

    def increaseDislikeNumber(self, id):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute(""" UPDATE post_comment as c SET dislike_number = dislike_number +1  where c.id = %s""",
                           (id,))

    def delete_comment(self, id):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                DELETE from post_comment where id = %s
            """, (id,))

Campaign Model
--------------

**campaignModel class**::

    def insert(self, campaign):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute("""INSERT INTO campaigns (barbershop_id, campaign_name, definition, start_date, end_date, discount)
                            VALUES(%s, %s, %s, %s, %s, %s) """, (campaign.barbershop_id, campaign.campaign_name, campaign.definition, campaign.start_date,
                                                                     campaign.end_date, campaign.discount))

    def delete_campaign(self, id):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                DELETE from campaigns where id = %s
            """, (id,))

    def get_campaigns(self):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * from campaigns")
            rows = cursor.fetchall()

        campaigns = []
        for row in rows:
            campaign = Campaign()
            campaign.id, campaign.barbershop_id, campaign.campaign_name, campaign.definition, campaign.start_date, campaign.end_date, campaign.discount = row[0], row[1], row[2], row[3], row[4], row[5], row[6]
            campaigns.append(campaign)
        return campaigns


