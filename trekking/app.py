from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from config import Config
from model import db, User

from controller.auth import RegisterAPI, LoginAPI, ProfileAPI
from controller.admin import AdminDashboardAPI, StaffAPI, TrekAPI
from controller.staff import (
    StaffDashboardAPI,
    StaffTrekAPI,
    ParticipantsAPI,
    CompleteTrekAPI
)
from controller.trek import (
    UserTrekAPI,
    SearchTrekAPI,
    TrekDetailsAPI
)
from controller.booking import (
    BookingAPI,
    BookingHistoryAPI
)

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)

api = Api(app)
jwt = JWTManager(app)
db.init_app(app)

api.add_resource(RegisterAPI, "/register")
api.add_resource(LoginAPI, "/login")
api.add_resource(ProfileAPI, "/profile")

api.add_resource(AdminDashboardAPI, "/admin/dashboard")
api.add_resource(StaffAPI, "/admin/staff")
api.add_resource(TrekAPI, "/admin/treks", "/admin/treks/<int:trek_id>")

api.add_resource(StaffDashboardAPI, "/staff/dashboard")
api.add_resource(StaffTrekAPI, "/staff/treks")
api.add_resource(ParticipantsAPI, "/staff/participants")
api.add_resource(CompleteTrekAPI, "/staff/complete")

api.add_resource(UserTrekAPI, "/treks")
api.add_resource(SearchTrekAPI, "/treks/search")
api.add_resource(TrekDetailsAPI, "/treks/<int:trek_id>")

api.add_resource(BookingAPI, "/bookings", "/bookings/<int:booking_id>")
api.add_resource(BookingHistoryAPI, "/bookings/history")


def create_admin():
    admin = User.query.filter_by(email="admin@trek.com").first()

    if not admin:
        admin = User(
            name="Admin",
            email="admin@trek.com",
            phone="9999999999",
            role="admin"
        )
        admin.set_password("admin123")

        db.session.add(admin)
        db.session.commit()

        print("Admin Created Successfully!")

    else:
        print("Admin Already Exists!")


if __name__ == "__main__":

    with app.app_context():
        db.create_all()
        create_admin()

    app.run(debug=app.config["DEBUG"])