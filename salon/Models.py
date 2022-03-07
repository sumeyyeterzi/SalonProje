import psycopg2 as dbapi2
from Entities import Comment, ContactInfo, Rezervation, People, Manicurist, Owner, LikedDisliked, Salon, CreditCard, \
    ServicePrice, Post, Post_comment, Campaign, Post
import datetime

import os

url = os.getenv("DATABASE_URL")

class StatisticsModel :
    def mostPopularSalons(self):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                Select s.* from 
                (SELECT  count(*) as c, Salon from comments 
                GROUP BY Salon )
                 as j join salon 
                 as s on j.salon = s.id 
                ORDER BY j.c DESC LIMIT 3
            """)
            rows = cursor.fetchall()

        salons = []
        for row in rows:
            salon = Salon()
            salon.id, salon.ownerpeople_id, salon.shopname, salon.location, salon.city, \
            salon.openingtime, salon.closingtime, salon.tradenumber = row[0], row[1], row[2], row[3], \
                                                                                     row[4], \
                                                                                     row[5], row[6], row[7]
            salons.append(salon)
        return salons

    def lastAddedSalons(self):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute("""
               SELECT * from salon ORDER BY Id DESC limit 3
            """)
            rows = cursor.fetchall()

        salons = []
        for row in rows:
            salon = Salon()
            salon.id, salon.ownerpeople_id, salon.shopname, salon.location, salon.city, \
            salon.openingtime, salon.closingtime, salon.tradenumber = row[0], row[1], row[2], row[3], \
                                                                                     row[4], \
                                                                                     row[5], row[6], row[7]
            salons.append(salon)
        return salons




class CommentModel:


    def save(self, comment):
        if (comment.id == None):
            self.insert(comment)
        else:
            if (self.ifExist(comment.id) != True):
                self.insert(comment)
            else:
                self.update(comment)


    def insert(self, comment):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute("""INSERT INTO Comments (people_id ,  manicurist , salon, title , content , rate , date_time , 
                comment_like, comment_dislike, keywords, image)
                VALUES (%s , %s, %s , %s , %s , %s , %s , %s , %s, %s, %s)""", (comment.peopleId, comment.manicurist,
                                                                                comment.salon,comment.title,
                                                                    comment.content, comment.rate, comment.dateTime,
                                                                    comment.like,
                                                                    comment.dislike, comment.keywords, comment.image))


    def getById(self, id):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT * from Comments as c where c.id = %s """, (id,))
            row = cursor.fetchone()


        comment = Comment()
        comment.id, comment.peopleId, comment.manicurist, comment.salon, comment.title, comment.content, comment.rate, comment.dateTime, \
        comment.like, comment.dislike = row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]
        return comment


    def getAll(self):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * from Comments as c order by c.date_time desc")
            rows = cursor.fetchall()

        comments = []
        for row in rows:
            comment = Comment()
            comment.id, comment.peopleId, comment.manicurist, comment.salon, comment.title, comment.content, comment.rate, comment.dateTime, \
            comment.like, comment.dislike = row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]
            comments.append(comment)
        return comments



    def deleteById(self, id):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                DELETE from Comments where id = %s
            """, (id,))


    def update(self, comment):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE Comments SET id = %s, people_id = %s , manicurist = %s , salon=%s, title = %s , content = %s ,
                rate = %s , date_time = %s , comment_like =%s , comment_dislike = %s where id = %s""",
                           (comment.id, comment.peopleId, comment.manicurist, comment.salon,
                            comment.title, comment.content, comment.rate,
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

    def getAllCommentswithPeopleBysalon_id(self, id):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT c.*, p.id, p.username from comments as c join people as  p on c.people_id = p.id 
                WHERE c.salon_id = %s order by c.date_time desc
            """,(id,))

        rows = cursor.fetchall()
        comments = []
        for row in rows:
            comment = Comment()
            comment.id, comment.peopleId, comment.manicurist, comment.salon, comment.title, comment.content, comment.rate, comment.dateTime, \
            comment.like, comment.dislike, comment.keywords, comment.image = row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8],row[9], row[10], row[11]

            people = People()
            people.id, people.username = row[12], row[13]
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

        if( likedislikeid == None):
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
            if(bool == 1 or bool==-1):
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



class ContactInfoModel:


    def save(self, comment):
        if (comment.id == None):
            self.insert(comment)
        else:
            if (self.ifExist(comment.id) != True):
                self.insert(comment)
            else:
                self.update(comment)


    def insert(self, contactInfo):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute("""INSERT INTO Contact_info (salon_id , type , telephone_number , facebook , twitter , 
                    instagram)
                    VALUES ( %s , %s , %s , %s , %s , %s)""",
                           (contactInfo.salon_id, contactInfo.type,
                            contactInfo.telephoneNumber, contactInfo.facebook, contactInfo.twitter,
                            contactInfo.instagram))


    def update(self, contactInfo):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE Contact_Info SET id = %s, salon_id = %s , type = %s , telephone_number = %s ,
                facebook = %s , twitter = %s , instagram =%s where id = %s """,
                           (contactInfo.id, contactInfo.salon_id, contactInfo.type,
                            contactInfo.telephoneNumber,
                            contactInfo.facebook, contactInfo.twitter, contactInfo.instagram, contactInfo.id))


    def getById(self, id):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT * from Contact_info as c where c.id = %s """, (id,))
            row = cursor.fetchone()


        contactInfo = ContactInfo()
        contactInfo.id, contactInfo.salon_id, contactInfo.type, contactInfo.telephoneNumber, \
        contactInfo.facebook, contactInfo.twitter, contactInfo.instagram = row[0], row[1], row[2], row[3], row[4], row[
            5], row[6]
        return contactInfo


    def deleteById(self, id):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                DELETE from Contact_info where id = %s
            """, (id,))


    def getAll(self):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * from Contact_info as c")
            rows = cursor.fetchall()

        contacts = []
        for row in rows:
            contactInfo = ContactInfo()
            contactInfo.id, contactInfo.salon_id, contactInfo.type, contactInfo.telephoneNumber, \
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

    def getBysalon_id (self, salon_id):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                       SELECT * from Contact_info as c where c.salon_id = %s """, (salon_id,))
            row = cursor.fetchone()


        if(row == None):
            return None
        contactInfo = ContactInfo()
        contactInfo.id, contactInfo.salon_id, contactInfo.type, contactInfo.telephoneNumber, \
        contactInfo.facebook, contactInfo.twitter, contactInfo.instagram = row[0], row[1], row[2], row[3], row[4], row[
            5], row[6]
        return contactInfo


class RezervationModel:


    def save(self, rezervation):
        if (rezervation.id == None):
            self.insert(rezervation)
        else:
            if (self.ifExist(rezervation.id) != True):
                self.insert(rezervation)
            else:
                self.update(rezervation)


    def insert(self, rezervation):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute("""INSERT INTO Rezervation (people_id, salon_id, datetime_registration, datetime_rezervation, status, note, 
                    price_type, payment_method)
                    VALUES (%s , %s , %s , %s , %s , %s , %s, %s)""",
                           (rezervation.peopleId, rezervation.salon_id, rezervation.dateTimeRegistration,
                            rezervation.dateTimeRezervation, rezervation.status, rezervation.note,
                            rezervation.priceType,rezervation.paymentMethod))
            return None


    def updateByIdDate(self, id, daterez):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE Rezervation SET datetime_rezervation = %s where id = %s """,
                           (
                               daterez, id))


    def getById(self, id):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT * from Rezervation as r where r.id = %s """, (id,))
            row = cursor.fetchone()


        rezervation = Rezervation()
        rezervation.id, rezervation.peopleId, rezervation.salon_id, rezervation.dateTimeRegistration, rezervation.dateTimeRezervation, \
        rezervation.status, rezervation.note, rezervation.priceType = row[0], row[1], row[2], row[3], row[4], \
                                                                      row[5], row[6], row[7]
        return rezervation

    def deleteById(self, id):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                DELETE from Rezervation where id = %s
            """, (id,))


    def getAllBySalon(self, shopid, currenttime, tomorrow):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute("""SELECT r.*, s.* from Rezervation as r left join serviceprices as s on r.price_type = s.id where r.salon_id = %s and r.datetime_rezervation >= %s and 
                r.datetime_rezervation < %s order by r.datetime_rezervation asc
            """,
                           (shopid, currenttime, tomorrow))
            rows = cursor.fetchall()
        if(rows == None):
            return  None
        rezervations = []
        for row in rows:
            rezervation = Rezervation()
            rezervation.id, rezervation.peopleId, rezervation.salon_id, rezervation.dateTimeRegistration, rezervation.dateTimeRezervation, \
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

class Peoplemodel:
    def insert(self, people):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute("""INSERT INTO People (username, name_surname, mail, password_hash, gender, age,role)
                           VALUES (%s , %s , %s , %s , %s , %s,  %s )""", (
            people.username, people.name_surname, people.mail, people.password_hash, people.gender, people.age,
            people.role))

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


    def get_hash(self, username):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                               SELECT password_hash from people where username = %s
                            """, (username,))
            hash = cursor.fetchone()[0]
            return hash

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

    def delete_id(self, id):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM People where id = %s", (id,))

    def control_exist_username(self, username):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM People where username = %s ", (username, ))
        row = cursor.fetchone()
        if (row == None):
            return False
        return True

    def update(self, people):
        if self.control_exist_to_update(people) == False:
            with dbapi2.connect(url) as connection:
                cursor = connection.cursor()
                cursor.execute("""UPDATE People SET username = %s, name_surname = %s, mail = %s, password_hash = %s, gender = %s, age = %s where id = %s""",
                               (people.username, people.name_surname, people.mail, people.password_hash, people.gender, people.age, people.id))
            return True
        else:
            return False


class ManicuristModel:
    def get_id(self, username):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                            SELECT id FROM PEOPLE WHERE username = %s 
                            """, (username, ))
        row = cursor.fetchone()
        return row

    def insert(self, manicurist):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute("""INSERT INTO manicurist (people_id, gender_choice, experience_year, start_time, finish_time, rates) 
                             VALUES (%s , %s , %s , %s , %s , %s )""", (manicurist.people_id, manicurist.gender_choice, manicurist.experience_year,
                                                                        manicurist.start_time, manicurist.finish_time, manicurist.rates))

    def delete_with_people_id(self, id):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM manicurist where people_id = %s", (id,))

    def update_manicurist(self, manicurist):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute(
                """UPDATE manicurist SET gender_choice = %s, experience_year = %s, start_time = %s, finish_time = %s  where people_id = %s""",
                (manicurist.gender_choice, manicurist.experience_year, manicurist.start_time, manicurist.finish_time, manicurist.people_id))
        return True


    def update_manicurist_employment(self, id, shop_id):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute(
                """UPDATE manicurist SET salon_id = %s where id = %s""",
                (shop_id, id))

    def get_unemployed_manicurists(self):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute("Select p.id, p.name_surname, p.age, b.id, b.experience_year from manicurist as b join people as p  on b.People_id = p.id where b.salon_id = null")
            rows = cursor.fetchall()

            manicurists = []
            if rows is None:
                return manicurists

            for row in rows:
                manicurist = ManicuristModel()
                people = People()

                people.id = row[0]
                people.name_surname = row[1]
                people.age = row[2]
                manicurist.id = row[3]
                manicurist.experience_year = row[4]

                manicurist.people = people
                manicurists.append(manicurist)
            return manicurists


    def get_manicurists_for_details_page_by_shop_id(self, shop_id):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute("Select p.id, p.name_surname, p.age, b.id, b.experience_year, b.salon_id from manicurist as b join people as p  on b.People_id = p.id where b.salon_id is NULL or b.salon_id = %s order by b.salon_id", (shop_id,))
            rows = cursor.fetchall()

            manicurists = []
            if rows is None:
                return manicurists

            for row in rows:
                manicurist = ManicuristModel()
                people = People()

                people.id = row[0]
                people.name_surname = row[1]
                people.age = row[2]
                manicurist.id = row[3]
                manicurist.experience_year = row[4]
                manicurist.salon_id = row[5]

                manicurist.people = people
                manicurists.append(manicurist)
            return manicurists

    def getManicuristsBySalon(self, salon_id):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute("Select b.id, p.name_surname from manicurist as b join people as p  on b.People_id = p.id where salon_id = %s", (salon_id,))
            rows = cursor.fetchall()

            if(rows == None):
                return None
            manicurists = []
            for row in rows:
                manicurist = ManicuristModel()
                people = People()
                manicurist.id = row[0]
                people.name_surname = row[1]
                manicurist.people = people
                manicurists.append(manicurist)
            if len(manicurists) == 0:
                 return None
            return manicurists

    def get_all_list(self):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute(""" SELECT * from manicurist""")
            manicurist_list = []
            rows = cursor.fetchall()
            for i in rows:
                manicurist = ManicuristModel()
                manicurist.id = i[0]
                manicurist.people_id = i[1]
                manicurist.salon_id = i[2]
                manicurist.gender_choice = i[3]
                manicurist.experience_year = i[4]
                manicurist.start_time = i[5]
                manicurist.finish_time = i[6]
                manicurist.rates = i[7]
                manicurist_list.append(manicurist)
            return manicurist_list


class Ownermodel:
    def get_id(self, username):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                            SELECT id FROM PEOPLE WHERE username = %s 
                            """, (username,))
        row = cursor.fetchone()
        return row


    def insert(self, owner):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute("""INSERT INTO Owner (people_id, tc_number, serial_number, vol_number, family_order_no, order_no)
                            VALUES (%s , %s , %s , %s , %s , %s )""", (owner.people_id, owner.tc_number, owner.serial_number, owner.vol_number, owner.family_order_no, owner.order_no))

    def delete_with_people_id(self, id):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM Owner where people_id = %s", (id,))


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


    def update_owner(self, owner):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute(
                """UPDATE Owner SET tc_number = %s, serial_number = %s, vol_number = %s, family_order_no = %s, order_no = %s  where people_id = %s""",
                (owner.tc_number, owner.serial_number, owner.vol_number, owner.family_order_no, owner.order_no, owner.people_id))
        return True

    def control_exist_tc(self, tc):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Owner where tc_number = %s ", (tc, ))
        row = cursor.fetchone()
        if (row == None):
            return False
        return True

class CreditcardModel:
    def insert(self, credit_card):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()

            cursor.execute("""INSERT INTO Creditcards (people_id, name, card_number, cvv_number, last_month, last_year, created_time) 
                             VALUES (%s , %s , %s , %s , %s , %s, %s )""", (credit_card.people_id, credit_card.name,
                                                                        credit_card.card_number,
                                                                        credit_card.cvv, credit_card.last_month,
                                                                        credit_card.last_year,
                                                                        credit_card.created_time))

    def update(self, credit_card):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE Creditcards SET name = %s, card_number = %s, cvv_number = %s, last_month = %s, last_year = %s where id = %s""",
                           (credit_card.name, credit_card.card_number, credit_card.cvv, credit_card.last_month, credit_card.last_year, credit_card.id))

    def delete_credit_card(self, id):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                DELETE from Creditcards where id = %s
            """, (id,))

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

class SalonModel:

    def insert(self, salon):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute("""INSERT INTO Salon (owner_people_id, shopname, location, city, opening_time, closing_time, trade_number, shop_logo) 
                             VALUES (%s , %s , %s , %s , %s , %s, %s, %s)""", (salon.ownerpeople_id, salon.shopname,
                                                                               salon.location, salon.city,
                                                                               salon.openingtime, salon.closingtime,
                                                                               salon.tradenumber,
                                                                               salon.shop_logo))

    def update(self, salon):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE salon SET shopname = %s, location = %s, city = %s, opening_time = %s, closing_time = %s, trade_number = %s where id = %s""",
                           (salon.shopname, salon.location, salon.city, salon.openingtime, salon.closingtime, salon.tradenumber, salon.id))


    def delete_salon(self, id):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                DELETE from salon where id = %s
            """, (id,))

    def get_salons_by_people_owner_id(self, people_owner_id):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * from salon where owner_people_id = %s", (people_owner_id,))
            rows = cursor.fetchall()

        salon_list = []
        for row in rows:
            salon = Salon()
            salon.id, salon.ownerpeople_id, salon.shopname, salon.location, salon.city, \
            salon.openingtime, salon.closingtime, salon.tradenumber = row[0], row[1], row[2], row[3], row[4], \
                                                                               row[5], row[6], row[7]
            salon_list.append(salon)
        return salon_list

    def get_salons_with_number_of_employee_by_people_owner_id(self, people_owner_id):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT s.id, s.owner_people_id, s.shopname, s.location, s.city, s.opening_time, s.closing_time, s.trade_number, count(b.id) from salon s left join manicurist b on s.id = b.salon_id where s.owner_people_id = %s group by s.id", (people_owner_id,))
            rows = cursor.fetchall()

        salon_list = []
        for row in rows:
            salon = Salon()
            salon.id, salon.ownerpeople_id, salon.shopname, salon.location, salon.city, \
            salon.openingtime, salon.closingtime, salon.tradenumber, salon.numberofemployee = \
            row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]

            salon_list.append(salon)
        return salon_list

    def get_salons_with_number_of_employee_by_id(self, id):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT s.id, s.owner_people_id, s.shopname, s.location, s.city, s.opening_time, s.closing_time, s.trade_number, count(b.id), s.shop_logo from salon s left join manicurist b on s.id = b.salon_id where s.id = %s group by s.id", (id,))
            rows = cursor.fetchall()

        salon_list = []
        for row in rows:
            salon = Salon()
            salon.id, salon.ownerpeople_id, salon.shopname, salon.location, salon.city, \
            salon.openingtime, salon.closingtime, salon.tradenumber, salon.numberofemployee, salon.shop_logo = \
            row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]

            salon_list.append(salon)
        if len(salon_list) == 0:
            return Salon()
        return salon_list[0]


    def getAll(self):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * from salon")
            rows = cursor.fetchall()

        salon_list = []
        for row in rows:
            salon = Salon()
            salon.id, salon.ownerpeople_id, salon.shopname, salon.location, salon.city, \
            salon.openingtime, salon.closingtime, salon.tradenumber = row[0], row[1], row[2], row[3], row[4], \
                                                                               row[5], row[6], row[7]
            salon_list.append(salon)
        return salon_list


    def getById(self, id):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT * from salon as b where b.id = %s """, (id,))
            row = cursor.fetchone()


        salon = Salon()
        salon.id, salon.ownerpeople_id, salon.shopname, salon.location, salon.city, \
        salon.openingtime, salon.closingtime, salon.tradenumber, salon.shop_logo = row[0], row[1], row[2], row[3], row[4], \
                                                                                 row[5], row[6], row[7], row[8]
        return salon






class ServicepriceModel:

    def insert(self, serviceprice):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute("""INSERT INTO Serviceprices (salon_id, service_name, definition, gender, price, duration) 
                             VALUES (%s , %s , %s , %s , %s , %s)""", (serviceprice.salon_id, serviceprice.service_name,
                                                                        serviceprice.definition, serviceprice.gender,
                                                                        serviceprice.price, serviceprice.duration))


    def update(self, service_price):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE Serviceprices SET service_name = %s, definition = %s, gender = %s, price = %s, duration = %s where id = %s""",
                           (service_price.service_name, service_price.definition, service_price.gender, service_price.price, service_price.duration, service_price.id))


    def delete_list_of_service(self, tuple):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                DELETE from Serviceprices where id in %s
            """, (tuple,))


    def listBySalon(self, salon_id):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute("""SELECT * from serviceprices where salon_id = %s """,
                           (salon_id,))

        rows = cursor.fetchall()

        services = []
        for row in rows:
            sv = ServicePrice()
            sv.id = row[0]
            sv.salon_id = row[1]
            sv.service_name = row[2]
            sv.definition = row[3]
            sv.gender = row[4]
            sv.price = row[5]
            sv.duration = row[6]
            services.append(sv)
        return services


    def getServiceById(self, salon_id):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute("""SELECT * from serviceprices where id = %s """,
                           (salon_id,))

        rows = cursor.fetchall()

        services = []
        for row in rows:
            sv = ServicePrice()
            sv.id = row[0]
            sv.salon_id = row[1]
            sv.service_name = row[2]
            sv.definition = row[3]
            sv.gender = row[4]
            sv.price = row[5]
            sv.duration = row[6]
            services.append(sv)
        if len(rows) == 0:
            return ServicePrice()
        return services[0]


class Postsmodel :

    def printposts(self):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * from Posts")
            data = cursor.fetchall()

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


    def getById(self, id):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT * from Posts as c where c.id = %s """, (id,))
            row = cursor.fetchone()

        post = Post()
        post.id, post.people_id, post.post_title, post.post_content, post.date_time, post.like, post.dislike = row[0], row[1], row[2], row[3], row[4], row[5], row[6]
        return post

    def deleteById(self, id):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                DELETE from Posts where id = %s
            """, (id,))

    def getAll_posts_with_people_id(self,id):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT c.*, p.id, p.username from Posts as c join people as  p on c.people_id = p.id 
                WHERE c.salon = %s order by c.date_time desc
            """, (id,))

        rows = cursor.fetchall()
        Posts = []
        for row in rows:
            Post = Post()
            Post.id, Post.people_id, Post.post_title, Post.post_content, Post.date_time, Post.subject,\
            Post.like, Post.dislike = row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]

            people = People()
            people.id, people.username = row[8], row[9]
            Post.peopleobj = people
            Posts.append(Post)
        return Posts

    def update(self, Post):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE Posts SET id = %s, people_id = %s , post_title = %s , post_content =%s like = %s , dislike = %s ,
                subject = %s , date_time = %s """,
                     (Post.id, Post.people_id, Post.post_title, Post.post_content, Post.like, Post.dislike, Post.subject,
                      Post.date_time))

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

    def delete_post(self, id):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute("""
                DELETE from Posts where id = %s
            """, (id,))


class PostCommentmodel :

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

class campaignModel:

    def insert(self, campaign):
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            cursor.execute("""INSERT INTO campaigns (salon_id, campaign_name, definition, start_date, end_date, discount)
                            VALUES(%s, %s, %s, %s, %s, %s) """, (campaign.salon_id, campaign.campaign_name, campaign.definition, campaign.start_date,
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
            campaign.id, campaign.salon_id, campaign.campaign_name, campaign.definition, campaign.start_date, campaign.end_date, campaign.discount = row[0], row[1], row[2], row[3], row[4], row[5], row[6]
            campaigns.append(campaign)
        return campaigns