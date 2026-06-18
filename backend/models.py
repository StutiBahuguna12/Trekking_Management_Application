from extensions import db
from flask_security import UserMixin, RoleMixin
from uuid import uuid4

user_roles = db.Table(
    'user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('users.user_id')),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'))
)


class Role(db.Model, RoleMixin):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"<Role name={self.name}>"



class User(db.Model, UserMixin):
    __tablename__ = "users"
    user_id = db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(255), unique=True, nullable=False)
    email=db.Column(db.String(255),nullable=False,unique=True)
    password=db.Column(db.String(255),nullable=False)
    active=db.Column(db.Boolean,default=True)
    active = db.Column(db.Boolean, default=True)

    fs_uniquifier = db.Column(
        db.String(64),
        unique=True,
        nullable=False,
        default=lambda: str(uuid4())
    )

    roles = db.relationship(
        'Role',
        secondary=user_roles,
        backref=db.backref('users', lazy='dynamic')
    )
    def __repr__(self):
        role_names = [role.name for role in self.roles]
        return f"Name: {self.username}, Roles: {role_names}, Email: {self.email}"
    



class Trek(db.Model):
    __tablename__ = "trek"
    trek_id = db.Column(db.Integer, primary_key=True)
    trek_name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    available_slots = db.Column(db.Integer, nullable=False)
    # allow treks without an assigned staff initially
    assigned_staff_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)
    assigned_staff = db.relationship('User', backref=db.backref('assigned_treks', lazy='dynamic'))
    status = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    contact = db.Column(db.String(15), nullable=False)
    price = db.Column(db.Float)

    def __repr__(self):
        return (
            f"Trek_name: {self.trek_name}, Location: {self.location}, "
            f"Difficulty: {self.difficulty}, Duration: {self.duration}, "
            f"Slots: {self.available_slots}, Status: {self.status}, "
            f"Start: {self.start_date}, End: {self.end_date}, "
            f"Contact: {self.contact}, Price: {self.price}"
        )


class Booking(db.Model):
    __tablename__ = "booking"
    booking_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    trek_id = db.Column(db.Integer, db.ForeignKey('trek.trek_id'), nullable=False)
    booking_date = db.Column(db.Date, nullable=False, server_default=db.func.current_date())
    status = db.Column(db.String(50), nullable=False)
    payment_status = db.Column(db.String(20), nullable=False)

    user = db.relationship('User', backref=db.backref('bookings', lazy='dynamic'))
    trek = db.relationship('Trek', backref=db.backref('bookings', lazy='dynamic'))

    def __repr__(self):
        return (
            f"Booking(id={self.booking_id}, user_id={self.user_id}, trek_id={self.trek_id}, "
            f"date={self.booking_date}, status={self.status}, payment_status={self.payment_status})"
        )


class Staff_Profile(db.Model):
    __tablename__ = "staff_profile"
    staff_id = db.Column(db.Integer, primary_key=True, nullable=False)
    staff_name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(15), unique=True, nullable=False)
    # assigned treks are represented by Trek.assigned_staff_id; remove duplicated string field
    status = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)
    user = db.relationship('User', backref=db.backref('staff_profile', uselist=False))

    def __repr__(self):
        return (
            f"Staff_Profile(staff_id={self.staff_id}, staff_name={self.staff_name}, "
            f"contact={self.contact}, assigned_treks={self.assigned_treks}, status={self.status})"
        )










