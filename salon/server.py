from flask import Flask, current_app, url_for, redirect
import views
from flask_login import LoginManager
import Models
import config
import os

os.environ['DATABASE_URL'] = config.DATABASE_URL

url = os.getenv("DATABASE_URL")
lm = LoginManager()


@lm.user_loader
def load_user(user_id):
    if user_id in current_app.config["LOGGED_USERS"]:
        login_user = current_app.config["LOGGED_USERS"][user_id]
        return login_user
    else:
        login_user = Models.Peoplemodel().get_all(user_id)
        current_app.config["LOGGED_USERS"][user_id] = login_user
        return login_user


def create_app():
    app2 = Flask(__name__)
    app2.config.from_object("settings")
    app2.secret_key = 'super secret key'
    app2.add_url_rule("/", view_func=views.home_page)
    app2.add_url_rule("/statistics",view_func=views.statistics)
    app2.add_url_rule("/salon/<id>", view_func=views.salon_view, methods=["GET", "POST"])
    app2.add_url_rule("/salon/edit/<id>", view_func=views.salon_view_edit, methods=["POST"])
    app2.add_url_rule("/salon/delete/<id>", view_func=views.salon_view_delete, methods=["POST"])
    app2.add_url_rule("/salon/likedislike/<id>", view_func=views.salon_comment_like_dislike, methods=["POST"])
    app2.add_url_rule("/rezervation/<id>", view_func=views.rezervation, methods=["GET","POST"])
    app2.add_url_rule("/rezervation/delete/<id>", view_func=views.rezervation_delete, methods=["POST"])
    app2.add_url_rule("/rezervation/edit/<id>", view_func=views.rezervation_edit, methods=["POST"])
    app2.add_url_rule("/contact/<id>", view_func=views.contact_settings, methods=["GET","POST"])
    app2.add_url_rule("/contact/delete/<id>", view_func=views.contact_delete, methods=["POST"])
    app2.add_url_rule("/blog", view_func=views.blog_page)
    app2.add_url_rule("/campaign", view_func=views.campaign_page)
    app2.add_url_rule("/profile", view_func=views.profile_page, methods=["GET", "POST"])
    app2.add_url_rule("/addcreditcard", view_func=views.addcreditcard_page, methods=["GET", "POST"])
    app2.add_url_rule("/updatecreditcard", view_func=views.updatecreditcard_page, methods=["GET", "POST"])
    app2.add_url_rule("/signup", view_func=views.signupbase_page, methods=["GET", "POST"])
    app2.add_url_rule("/signup_manicurist", view_func=views.signup_manicurist_page, methods=["GET", "POST"])
    app2.add_url_rule("/signup_owner", view_func=views.signup_owner_page, methods=["GET", "POST"])
    app2.add_url_rule("/signup_user", view_func=views.signup_user_page, methods=["GET", "POST"])
    app2.add_url_rule("/signin", view_func=views.signin, methods=["GET", "POST"])
    app2.add_url_rule("/signout", view_func=views.signout)
    app2.add_url_rule("/admin_panel", view_func=views.admin_panel, methods=["GET", "POST"])
    app2.add_url_rule("/newpost/<people_id>", view_func=views.newpost_page, methods=["GET", "POST"])
    app2.add_url_rule("/add_salon", view_func=views.add_salon_page, methods=["GET", "POST"])
    app2.add_url_rule("/salon_details/<id>", view_func=views.salon_details_page, methods=["GET", "POST"])
    app2.add_url_rule("/salon_delete/<id>", view_func=views.salon_delete, methods=["GET", "POST"])
    app2.add_url_rule("/manicurist_employ/<manicurist_id>/<status>/<salon_id>", view_func=views.manicurist_employ, methods=["GET", "POST"])
    app2.add_url_rule("/add_service_price/<salon_id>", view_func=views.add_service_price_page, methods=["GET", "POST"])
    app2.add_url_rule("/delete_services/<salon_id>", view_func=views.delete_service_prices, methods=["GET", "POST"])
    app2.add_url_rule("/post_comment/<post_id>/<people_id>", view_func=views.comment_page, methods=["GET", "POST"])
    app2.add_url_rule("/like_post/<post_id>", view_func=views.like_post, methods=["GET", "POST"])
    app2.add_url_rule("/dislike_post/<post_id>", view_func=views.dislike_post, methods=["GET", "POST"])
    app2.add_url_rule("/like_comment/<comment_id>", view_func=views.like_comment, methods=["GET", "POST"])
    app2.add_url_rule("/dislike_comment/<comment_id>", view_func=views.dislike_comment, methods=["GET", "POST"])
    app2.add_url_rule("/delete_post/<post_id>", view_func=views.post_delete, methods=["GET", "POST"])
    app2.add_url_rule("/delete_comment/<id>", view_func=views.comment_delete, methods=["GET", "POST"])
    app2.add_url_rule("/newcampaign", view_func=views.newcampaign, methods=["GET", "POST"])
    app2.add_url_rule("/campaign", view_func=views.campaign_page)

    lm.init_app(app2)
    lm.login_view = "login_page"

    app2.config["DEBUG"] = True
    return app2


app = create_app()


if __name__ == "__main__":
    #port = app.config.get("PORT", 5000)
    #app.run(host="0.0.0.0", port=port)
    app.run()