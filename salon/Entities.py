from datetime import datetime




class Comment:
    def __init__(self):
        self.id = None
        self.peopleId = None
        self.manicurist = None
        self.salon = None
        self.title = ""
        self.content = ""
        self.rate = 0
        self.dateTime = datetime.now()
        self.like = 0
        self.dislike = 0
        self.peopleobj = None
        self.likedDislikedobj = None
        self.keywords = None
        self.image = None

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
        self.salon_id = None
        self.type = None
        self.telephoneNumber = None
        self.facebook = None
        self.twitter = None
        self.instagram = None



class Rezervation:
    def __init__(self):
        self.id = None
        self.peopleId = None
        self.salon_id = None
        self.dateTimeRegistration = datetime.now()
        self.dateTimeRezervation = None
        self.status = None
        self.note = None
        self.priceType = None
        self.paymentMethod = None



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

class Manicurist:
    def __init__(self):
        self.id = None
        self.people_id = None
        self.salon_id = None
        self.gender_choice = None
        self.experience_year = None
        self.start_time = None
        self.finish_time = None
        self.rates = None
        self.people = None 

class Owner:
    def __init__(self):
        self.id = None
        self.people_id = None
        self.tc_number = None
        self.serial_number = None
        self.vol_number = None
        self.family_order_no = None
        self.order_no = None


class ServicePrice:
    def __init__(self):
        self.id = None
        self.salon_id = None
        self.service_name = None
        self.definition = None
        self.gender = None
        self.price = None
        self.duration = None


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


class Salon:
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
        self.salon_id = None
        self.campaign_name = None
        self.definition = None
        self.start_date = None
        self.end_date = None
        self.discount = None
