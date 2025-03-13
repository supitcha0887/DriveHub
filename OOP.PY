import os
import json
import time

class Car:
    def __init__(self, id, model, licensecar, price, status, color, seat_count, image=None):
        self.__id = id
        self.__model = model
        self.__licensecar = licensecar
        self.__price = price
        self.__status = status
        self.__color = color
        self.__seat_count = seat_count
        self.__image = image
        self.__reviews = []
        self.__ratings = []
    def get_image(self):
        return self.__image
    def get_id(self):
        return self.__id
    def get_model(self):
        return self.__model
    def get_licensecar(self):
        return self.__licensecar
    def get_price(self):
        return self.__price
    def get_status(self):
        return self.__status
    def get_color(self):
        return self.__color
    def get_seat_count(self):
        return self.__seat_count
    def status_car(self, new_status):
        self.__status = new_status
        return self.__status
    def add_review_car(self, review):
        self.__reviews.append(review)
        return self.__reviews
    def add_rating_car(self, rating):
        self.__ratings.append(rating)
        return self.__ratings
    def get_reviews(self):
        return self.__reviews
    def get_ratings(self):
        return self.__ratings
    def cal_rating(self):
        if len(self.__ratings) == 0:
            return 0
        return sum(self.__ratings) / len(self.__ratings)

class Account:
    def __init__(self, id, username, password, role):
        self.__id = id
        self.__username = username
        self.__password = password
        self.__role = role
    def get_id(self):
        return self.__id
    def get_username(self):
        return self.__username
    def get_password(self):
        return self.__password
    def get_role(self):
        return self.__role

class Driver(Account):
    def __init__(self, id, username, password, role, licenseDrive):
        super().__init__(id, username, password, role)
        self.__licenseDrive = licenseDrive
    def get_licenseDrive(self):
        return self.__licenseDrive
    def accept_job(self):
        return f"Driver {self.get_username()} accepted the job"

class Admin(Account):
    def __init__(self, id, username, password, role):
        super().__init__(id, username, password, role)
        self.__users = []
    def accept_payment(self, payment):
        return f"Admin {self.get_username()} accepted payment with id {payment.get_id()}"

class User(Account):
    def __init__(self, id, username, password, role, licensedrivUser):
        super().__init__(id, username, password, role)
        self.__licenseUser = licensedrivUser
    def get_licenseUser(self):
        return self.__licenseUser
    def search_car(self, company, model):
        matching_cars = [car for car in company.get_cars() if car.get_model() == model]
        return matching_cars

class Reservation:
    def __init__(self, id, renter: User, car: Car, start_date, end_date, price, driver=None, promotion=None, insurance=None):
        self.__id = id
        self.__renter = renter
        self.__car = car
        self.__driver = driver
        self.__start_date = start_date
        self.__end_date = end_date
        self.__promotion = promotion
        self.__insurance = insurance
        self.__price = price
        self.__admin_approved = False
        self.__driver_approved = False
        self.__paid = False
    def get_id(self):
        return self.__id
    def get_renter(self):
        return self.__renter
    def get_car(self):
        return self.__car
    def get_driver(self):
        return self.__driver
    def get_start_date(self):
        return self.__start_date
    def get_end_date(self):
        return self.__end_date
    def get_insurance(self):
        return self.__insurance
    def get_price(self):
        return self.__price
    def update_price(self):
        base_price = float(self.__car._Car__price)
        if self.__promotion:
            discount = base_price * (self.__promotion._Promotion__percent / 100)
            new_price = base_price - discount
        else:
            new_price = base_price
        self.__price = new_price
        return new_price
    def update_status_car(self, new_status="reserved"):
        self.__car.status_car(new_status)
        return self.__car.get_status()
    def is_admin_approved(self):
        return self.__admin_approved
    def is_driver_approved(self):
        return self.__driver_approved
    def approve_admin(self):
        self.__admin_approved = True
        self.__car.status_car("available")
    def approve_driver(self):
        self.__driver_approved = True
    def get_promotion(self):
        return self.__promotion
    def apply_promotion(self, promotion):
        self.__promotion = promotion
        base_price = self.__car.get_price()
        discount = base_price * (promotion.get_percent() / 100)
        self.__price = base_price - discount
    def mark_paid(self):
        self.__paid = True
    def is_paid(self):
        return self.__paid

class Promotion:
    def __init__(self, id, code, percent):
        self.__id = id
        self.__code = code
        self.__percent = percent
    def get_id(self):
        return self.__id
    def get_percent(self):
        return self.__percent
    def check_promotion(self, code):
        return self.__code == code

class Location:
    def __init__(self, id, name):
        self.__id = id
        self.__name = name
    def get_id(self):
        return self.__id
    def get_name(self):
        return self.__name

class Priceseason:
    def __init__(self, id, high_season=1.2, low_season=0.9):
        self.__id = id
        self.__high_season = high_season
        self.__low_season = low_season
    def get_id(self):
        return self.__id
    def check_season(self, current_month):
        if current_month in [6, 7, 8]:
            return self.__high_season
        else:
            return self.__low_season

class Review:
    def __init__(self, comment, date):
        self.__comment = comment
        self.__date = date
    def get_comment(self):
        return self.__comment
    def get_date(self):
        return self.__date

class Payment:
    def __init__(self, id, creditcard=None, qrcode=None):
        self.__id = id
        self.__creditcard = creditcard
        self.__qrcode = qrcode
    def get_id(self):
        return self.__id
    def check_method_payment(self):
        if self.__creditcard:
            return "creditcard"
        elif self.__qrcode:
            return "qrcode"
        else:
            return "unknown"

class Insurance:
    def __init__(self, id, name, detail, price):
        self.__id = id
        self.__name = name
        self.__detail = detail
        self.__price = price
    def get_id(self):
        return self.__id    
    def get_name(self):
        return self.__name
    def get_detail(self):
        return self.__detail
    def get_price(self):
        return self.__price

class Company:
    def __init__(self):
        self.__users = []
        self.__payments = []
        self.__reservations = []
        self.__promotions = []
        self.__location = []
        self.__cars = []
        self.load_users()
    def add_user(self, user: User):
        self.__users.append(user)
        return user
    def get_users(self):
        return self.__users
    def add_payment(self, payment):
        self.__payments.append(payment)
        return payment
    def get_payments(self):
        return self.__payments
    def add_reservation(self, reservation):
        self.__reservations.append(reservation)
        return reservation
    def get_reservations(self):
        return self.__reservations
    

    def find_available(self, start_date, end_date):
        lst = []
        for car in self.__cars:
            print(f"Checking car: {car.get_model()} (ID: {car.get_id()})")
            is_available = True
            for reservation in self.__reservations:
                if car == reservation.get_car():
                    print(f"  Against reservation: {reservation.get_id()} (Start: {reservation.get_start_date()}, End: {reservation.get_end_date()})")
                    if (start_date >= reservation.get_start_date() and start_date <= reservation.get_end_date()):
                        is_available = False
                        break
                    if (end_date > reservation.get_start_date() and end_date <= reservation.get_end_date()):
                        is_available = False
                        break
            if is_available:
                lst.append(car)
        return lst




    def add_promotion(self, promotion):
        self.__promotions.append(promotion)
        return promotion
    def get_promotions(self):
        return self.__promotions
    def add_location(self, location: Location):
        self.__location.append(location)
        return location
    def get_location(self):
        return self.__location
    def add_car(self, car: Car):
        self.__cars.append(car)
        return car
    def get_cars(self):
        return self.__cars
    def edit_car(self, car_id, **kwargs):
        for car in self.__cars:
            if car._Car__id == car_id:
                for key, value in kwargs.items():
                    if key == "model":
                        car._Car__model = value
                    elif key == "licensecar":
                        car._Car__licensecar = value
                    elif key == "price":
                        car._Car__price = value
                    elif key == "status":
                        car._Car__status = value
                    elif key == "color":
                        car._Car__color = value
                    elif key == "seat_count":
                        car._Car__seat_count = value
                return True
        return False
    def del_car(self, car_id):
        for i, car in enumerate(self.__cars):
            if car._Car__id == car_id:
                del self.__cars[i]
                return True
        return False
    def add_driver(self, driver: Driver):
        self.__users.append(driver)
        return driver
    def login(self, username, password):
        for user in self.__users:
            if user.get_username() == username and user.get_password() == password:
                return user.get_role()
        return "again, please"
    def load_users(self):
        if os.path.exists("users.json"):
            with open("users.json", "r") as f:
                try:
                    data = json.load(f)
                    for user_data in data:
                        role = user_data.get("role")
                        uid = user_data.get("id")
                        username = user_data.get("username")
                        password = user_data.get("password")
                        if role == "admin":
                            new_user = Admin(uid, username, password, role)
                        elif role == "driver":
                            licenseDrive = user_data.get("licenseDrive", "default_driver_license")
                            new_user = Driver(uid, username, password, role, licenseDrive)
                        elif role in ["user", "renter"]:
                            licenseUser = user_data.get("licenseUser", "default_license")
                            new_user = User(uid, username, password, role, licenseUser)
                        else:
                            continue
                        self.__users.append(new_user)
                except Exception as e:
                    print("Error loading users:", e)
        else:
            print("No users file found; starting with empty user list.")
    def register(self, username, password, role):
        for user in self.__users:
            if user.get_username() == username:
                return False, "Username already exists"
        new_id = len(self.__users) + 1000
        if role in ["driver", "renter"]:
            if role == "driver":
                new_user = Driver(new_id, username, password, role, "default_driver_license")
            else:
                new_user = User(new_id, username, password, role, "default_license")
        else:
            return False, "Invalid role selected"
        self.__users.append(new_user)
        return True, "Registration successful"
    def load_users(self):
        if os.path.exists("users.json"):
            with open("users.json", "r") as f:
                try:
                    data = json.load(f)
                    for user_data in data:
                        role = user_data.get("role")
                        uid = user_data.get("id")
                        username = user_data.get("username")
                        password = user_data.get("password")
                        if role == "admin":
                            new_user = Admin(uid, username, password, role)
                        elif role == "driver":
                            licenseDrive = user_data.get("licenseDrive", "default_driver_license")
                            new_user = Driver(uid, username, password, role, licenseDrive)
                        elif role in ["user", "renter"]:
                            licenseUser = user_data.get("licenseUser", "default_license")
                            new_user = User(uid, username, password, role, licenseUser)
                        else:
                            continue
                        self.__users.append(new_user)
                except Exception as e:
                    print("Error loading users:", e)
        else:
            print("No users file found; starting with empty user list.")
    def save_users(self):
        data = []
        for user in self.__users:
            d = {
                "id": user.get_id(),
                "username": user.get_username(),
                "password": user.get_password(),
                "role": user.get_role()
            }
            if user.get_role() == "driver":
                d["licenseDrive"] = user.get_licenseDrive()
            elif user.get_role() in ["user", "renter"]:
                d["licenseUser"] = user.get_licenseUser()
            data.append(d)
        with open("users.json", "w") as f:
            json.dump(data, f)

company = Company()
admin1 = Admin(1001, "admin1", "pass1", "admin")
driver1 = Driver(2001, "driver1", "pass1", "driver", "L-123")
user1 = User(3001, "user1", "pass1", "renter", "U-111")
company.add_user(user1)
company.add_driver(driver1)
company.add_user(admin1)
promotion1 = Promotion(1, "PROMO1", 10)
promotion2 = Promotion(2, "PROMO2", 20)
company.add_promotion(promotion1)
company.add_promotion(promotion2)
def init_data():
    if not company.get_cars():
        car1 = Car("1", "Toyota", "D0-1125", 2000, "available", "red", "5", image="/static/images/toyota.png")
        company.add_car(car1)
        review1 = Review("Excellent car", "2025-03-01")
        car1.add_review_car(review1)
        car1.add_rating_car(4.5)
        car1.add_rating_car(5.0)
        car2 = Car("2", "Honda", "D0-1126", 2500, "available", "blue", "6", image="/static/images/honda.jpg")
        company.add_car(car2)
        car3 = Car("3", "Ford", "D0-1127", 3000, "available", "orange", "5", image="/static/images/ford.jpg")
        company.add_car(car3)
init_data()
if __name__ == "__main__":
    print("Registered Users:")
    for u in company.get_users():
        print(f"Username: {u.get_username()}, Role: {u.get_role()}")
    print("\nCars in Company:")
    for c in company.get_cars():
        print(f"ID: {c.get_id()}, Model: {c.get_model()}, License: {c.get_licensecar()}, Price: {c.get_price()}, Status: {c.get_status()}, Color: {c.get_color()}")
    print("\nPayments:")
    for p in company.get_payments():
        print(f"Payment ID: {p.get_id()}, Method: {p.check_method_payment()}")
    print("\nReservations:")
    for res in company.get_reservations():
        driver_info = res.get_driver().get_username() if res.get_driver() else "Not assigned"
        print(f"Reservation ID: {res.get_id()}, Renter: {res.get_renter().get_username()}, Car: {res.get_car().get_model()}, Start: {res.get_start_date()}, End: {res.get_end_date()}, Price: {res.get_price()}, Driver: {driver_info}")
    print("\nPromotions:")
    for promo in company.get_promotions():
        print(f"Promotion ID: {promo.get_id()}, Code: {promo._Promotion__code}, Percent: {promo.get_percent()}")
    print("\nLocations:")
    for loc in company.get_location():
        print(f"Location ID: {loc.get_id()}, Name: {loc.get_name()}")





print()