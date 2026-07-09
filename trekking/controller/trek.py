from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from model import Trek


class UserTrekAPI(Resource):

    @jwt_required()
    def get(self):

        treks = Trek.query.filter_by(status="Open").all()

        result = []

        for trek in treks:
            result.append({
                "id": trek.id,
                "name": trek.name,
                "location": trek.location,
                "difficulty": trek.difficulty,
                "duration": trek.duration,
                "available_slots": trek.available_slots,
                "staff": trek.staff.name if trek.staff else None,
                "start_date": str(trek.start_date),
                "end_date": str(trek.end_date)
            })

        return result, 200
    
class SearchTrekAPI(Resource):

    def get(self):

        location = request.args.get("location")
        difficulty = request.args.get("difficulty")
        duration = request.args.get("duration")

        query = Trek.query.filter_by(status="Open")

        if location:
            query = query.filter(Trek.location.ilike(f"%{location}%"))

        if difficulty:
            query = query.filter_by(difficulty=difficulty)

        if duration:
            query = query.filter_by(duration=int(duration))

        treks = query.all()

        result = []

        for trek in treks:

            result.append({
                "id": trek.id,
                "name": trek.name,
                "location": trek.location,
                "difficulty": trek.difficulty,
                "duration": trek.duration,
                "available_slots": trek.available_slots,
                "status": trek.status
            })

        return result, 200
    
class TrekDetailsAPI(Resource):

    @jwt_required()
    def get(self, trek_id):

        trek = Trek.query.get(trek_id)

        if not trek:
            return {"message": "Trek not found"}, 404

        return {
            "id": trek.id,
            "name": trek.name,
            "location": trek.location,
            "difficulty": trek.difficulty,
            "duration": trek.duration,
            "description": trek.description,
            "available_slots": trek.available_slots,
            "status": trek.status,
            "staff": trek.staff.name if trek.staff else None,
            "start_date": str(trek.start_date),
            "end_date": str(trek.end_date)
        }, 200