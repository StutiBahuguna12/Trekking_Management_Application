from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from model import db, User, Trek, Booking


class StaffDashboardAPI(Resource):

    @jwt_required()
    def get(self):

        current_user = User.query.get(int(get_jwt_identity()))

        if current_user.role != "staff":
            return {"message": "Access Denied"}, 403

        return {
            "assigned_treks": Trek.query.filter_by(staff_id=current_user.id).count(),
            "open_treks": Trek.query.filter_by(
                staff_id=current_user.id,
                status="Open"
            ).count(),
            "completed_treks": Trek.query.filter_by(
                staff_id=current_user.id,
                status="Completed"
            ).count()
        }, 200


class StaffTrekAPI(Resource):

    @jwt_required()
    def get(self):

        current_user = User.query.get(int(get_jwt_identity()))

        if current_user.role != "staff":
            return {"message": "Access Denied"}, 403

        treks = Trek.query.filter_by(staff_id=current_user.id).all()

        result = []

        for trek in treks:

            result.append({
                "id": trek.id,
                "name": trek.name,
                "location": trek.location,
                "difficulty": trek.difficulty,
                "duration": trek.duration,
                "available_slots": trek.available_slots,
                "status": trek.status,
                "start_date": str(trek.start_date),
                "end_date": str(trek.end_date)
            })

        return result, 200


    @jwt_required()
    def put(self):

        current_user = User.query.get(int(get_jwt_identity()))

        if current_user.role != "staff":
            return {"message": "Access Denied"}, 403

        data = request.get_json()

        trek = Trek.query.get(data.get("trek_id"))

        if not trek:
            return {"message": "Trek not found"}, 404

        if trek.staff_id != current_user.id:
            return {"message": "You are not assigned to this trek"}, 403

        if "available_slots" in data:

            available_slots = data["available_slots"]

        if available_slots > trek.total_slots:
           return {
               "message": "Available slots cannot exceed total slots"
           }, 400

        if available_slots < 0:
            return {
                "message": "Invalid slots"
            }, 400

        trek.available_slots = available_slots
        if "status" in data:
            trek.status = data["status"]
        db.session.commit()

        return {"message": "Trek updated successfully"}, 200
    


class ParticipantsAPI(Resource):

    @jwt_required()
    def get(self):

        current_user = User.query.get(int(get_jwt_identity()))

        if current_user.role != "staff":
            return {"message": "Access denied"}, 403

        trek_id = request.args.get("trek_id", type=int)

        trek = Trek.query.get(trek_id)

        if not trek:
            return {"message": "Trek not found"}, 404

        if trek.staff_id != current_user.id:
            return {"message": "You are not assigned to this trek"}, 403

        bookings = Booking.query.filter_by(
            trek_id=trek.id,
            status="Booked"
        ).all()

        result = []

        for booking in bookings:

            result.append({
                "booking_id": booking.id,
                "user_id": booking.user.id,
                "name": booking.user.name,
                "email": booking.user.email,
                "phone": booking.user.phone
            })

        return result, 200
class CompleteTrekAPI(Resource):

    @jwt_required()
    def put(self):

        current_user = User.query.get(int(get_jwt_identity()))

        if current_user.role != "staff":
            return {"message": "Access Denied"}, 403

        data = request.get_json()

        trek = Trek.query.get(data.get("trek_id"))

        if not trek:
            return {"message": "Trek not found"}, 404

        if trek.staff_id != current_user.id:
            return {"message": "Not your trek"}, 403
        if trek.status == "Completed":
              return {"message": "Trek already completed"}, 400
        trek.status = "Completed"

        bookings = Booking.query.filter_by(
            trek_id=trek.id,
            status="Booked"
        ).all()

        for booking in bookings:
            booking.status = "Completed"

        db.session.commit()

        return {"message": "Trek marked as completed"}, 200