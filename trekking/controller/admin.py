from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from model import db, User, Trek, Booking, StaffProfile


class AdminDashboardAPI(Resource):

    @jwt_required()
    def get(self):

        current_user = User.query.get(int(get_jwt_identity()))

        if current_user.role != "admin":
            return {"message": "Access Denied"}, 403

        return {
            "total_users": User.query.filter_by(role="user").count(),
            "total_staff": User.query.filter_by(role="staff").count(),
            "total_treks": Trek.query.count(),
            "total_bookings": Booking.query.count()
        }, 200


class StaffAPI(Resource):

    @jwt_required()
    def post(self):

        current_user = User.query.get(int(get_jwt_identity()))

        if current_user.role != "admin":
            return {"message": "Access Denied"}, 403

        data = request.get_json()

        name = data.get("name")
        email = data.get("email")
        password = data.get("password")
        phone = data.get("phone")
        experience = data.get("experience")
        specialization = data.get("specialization")

        if not all([
            name,
            email,
            password,
            phone,
            experience,
            specialization
        ]):
            return {"message": "All fields are required."}, 400

        if User.query.filter_by(email=email).first():
            return {"message": "Email already exists."}, 400

        staff = User(
            name=name,
            email=email,
            phone=phone,
            role="staff"
        )

        staff.set_password(password)

        db.session.add(staff)
        db.session.flush()

        profile = StaffProfile(
            user_id=staff.id,
            experience=experience,
            specialization=specialization
        )

        db.session.add(profile)
        db.session.commit()

        return {"message": "Staff created successfully."}, 201


    @jwt_required()
    def get(self):

        current_user = User.query.get(int(get_jwt_identity()))

        if current_user.role != "admin":
            return {"message": "Access Denied"}, 403

        staff_members = User.query.filter_by(role="staff").all()

        result = []

        for staff in staff_members:

            result.append({
                "id": staff.id,
                "name": staff.name,
                "email": staff.email,
                "phone": staff.phone,
                "experience": staff.staff_profile.experience,
                "specialization": staff.staff_profile.specialization,
                "active": staff.active
            })

        return result, 200


class TrekAPI(Resource):

    @jwt_required()
    def post(self):

        current_user = User.query.get(int(get_jwt_identity()))

        if current_user.role != "admin":
            return {"message": "Access Denied"}, 403

        data = request.get_json()

        name = data.get("name")
        location = data.get("location")
        difficulty = data.get("difficulty")
        duration = data.get("duration")
        total_slots = data.get("total_slots")
        description = data.get("description")
        start_date = data.get("start_date")
        end_date = data.get("end_date")

        if not all([
            name,
            location,
            difficulty,
            duration,
            total_slots,
            start_date,
            end_date
        ]):
            return {"message": "All fields are required."}, 400

        start = datetime.strptime(start_date, "%Y-%m-%d").date()
        end = datetime.strptime(end_date, "%Y-%m-%d").date()

        if end < start:
            return {
                "message": "End date cannot be before start date"
            }, 400

        trek = Trek(
            name=name,
            location=location,
            difficulty=difficulty,
            duration=duration,
            total_slots=total_slots,
            available_slots=total_slots,
            description=description,
            start_date=start,
            end_date=end
        )

        db.session.add(trek)
        db.session.commit()

        return {"message": "Trek created successfully."}, 201


    @jwt_required()
    def get(self):

        current_user = User.query.get(int(get_jwt_identity()))

        if current_user.role != "admin":
            return {"message": "Access Denied"}, 403

        treks = Trek.query.all()

        result = []

        for trek in treks:

            result.append({
                "id": trek.id,
                "name": trek.name,
                "location": trek.location,
                "difficulty": trek.difficulty,
                "duration": trek.duration,
                "total_slots": trek.total_slots,
                "available_slots": trek.available_slots,
                "status": trek.status,
                "staff_name": trek.staff.name if trek.staff else None
            })

        return result, 200


    @jwt_required()
    def put(self):

        current_user = User.query.get(int(get_jwt_identity()))

        if current_user.role != "admin":
            return {"message": "Access Denied"}, 403

        data = request.get_json()

        trek = Trek.query.get(data.get("trek_id"))

        if not trek:
            return {"message": "Trek not found"}, 404

        staff = User.query.filter_by(
            id=data.get("staff_id"),
            role="staff"
        ).first()

        if not staff:
            return {"message": "Staff not found"}, 404

        if trek.staff_id == staff.id:
            return {
                "message": "This staff is already assigned to the trek"
            }, 400

        trek.staff_id = staff.id

        db.session.commit()

        return {
            "message": "Staff assigned successfully"
        }, 200


    @jwt_required()
    def delete(self):

        current_user = User.query.get(int(get_jwt_identity()))

        if current_user.role != "admin":
            return {"message": "Access Denied"}, 403

        data = request.get_json()

        trek = Trek.query.get(data.get("trek_id"))

        if not trek:
            return {"message": "Trek not found"}, 404

        if Booking.query.filter_by(
            trek_id=trek.id,
            status="Booked"
        ).count() > 0:
            return {
                "message": "Cannot delete a trek with active bookings"
            }, 400

        db.session.delete(trek)
        db.session.commit()

        return {
            "message": "Trek deleted successfully"
        }, 200