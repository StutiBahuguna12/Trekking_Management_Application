from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from model import db, User, Trek, Booking

class BookingAPI(Resource):
    @jwt_required()
    def post(self):
        current_user = User.query.get(int(get_jwt_identity()))
        if current_user.role != "user":
            return {"message": "Only users can book treks"}, 403
        data = request.get_json()
        trek = Trek.query.get(data.get("trek_id"))
        if not trek:
            return {"message": "Trek not found"}, 404
        if trek.status != "Open":
            return {"message": "Bookings are closed for this trek"}, 400
        if trek.available_slots <= 0:
            return {"message": "No slots available"}, 400
        already_booked = Booking.query.filter_by(
    user_id=current_user.id,
    trek_id=trek.id,
    status="Booked"
).first()
        if already_booked:
            return {"message": "You have already booked this trek"}, 400
        booking = Booking(
            user_id=current_user.id,
            trek_id=trek.id
        )
        db.session.add(booking)
        trek.available_slots -= 1
        db.session.commit()
        return {
            "message": "Trek booked successfully"
        }, 201
    @jwt_required()
    def get(self):
        current_user = User.query.get(int(get_jwt_identity()))
        if current_user.role != "user":
            return {"message": "Access Denied"}, 403
        bookings = Booking.query.filter_by( user_id=current_user.id).all()
        result = []
        for booking in bookings:
             result.append({
                "booking_id": booking.id,
                "trek_id": booking.trek.id,
                "trek_name": booking.trek.name,
                "location": booking.trek.location,
                "booking_date": str(booking.booking_date),
                "status": booking.status,
                "start_date": str(booking.trek.start_date),
                "end_date": str(booking.trek.end_date)
            })
        return result, 200
    @jwt_required()
    def delete(self, booking_id):
        current_user = User.query.get(int(get_jwt_identity()))

        if current_user.role != "user":
             return {"message": "Access Denied"}, 403

        booking = Booking.query.get(booking_id)

        if not booking:
            return {"message": "Booking not found"}, 404

        if booking.user_id != current_user.id:
            return {"message": "You cannot cancel this booking"}, 403

        if booking.status == "Cancelled":
            return {"message": "Booking already cancelled"}, 400

        if booking.status == "Completed":
           return { "message": "Completed bookings cannot be cancelled"}, 400

        booking.status = "Cancelled"

        if booking.trek.available_slots < booking.trek.total_slots:
            booking.trek.available_slots += 1

        db.session.commit()

        return {"message": "Booking cancelled successfully"}, 200
class BookingHistoryAPI(Resource):

    @jwt_required()
    def get(self):
        current_user = User.query.get(int(get_jwt_identity()))
        if current_user.role != "user":
             return {"message": "Access Denied"}, 403
        history = Booking.query.filter(
            Booking.user_id == current_user.id,
            Booking.status.in_(["Cancelled", "Completed"])
        ).all()
        result = []
        for booking in history:
            result.append({
                "booking_id": booking.id,
                "trek_name": booking.trek.name,
                "location": booking.trek.location,
                "status": booking.status,
                "booking_date": str(booking.booking_date)
            })
        return result, 200