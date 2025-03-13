from fasthtml.common import *
from routing import app, rt
import BackEnd, time, datetime

company = BackEnd.company

THEME_STYLE = """
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
* { box-sizing: border-box; }
html, body {
    height: 100%;
    margin: 0;
    padding: 0;
    font-family: 'Roboto', sans-serif;
    background: linear-gradient(135deg, #bbdefb, #e3f2fd);
}
"""

@rt('/reservation/form', methods=["GET"])
def reservation_form(car_id: str = "", start_date: str = "", end_date: str = ""):
    selected_car = None
    for car in company.get_cars():
        if car.get_id() == car_id:
            selected_car = car
            break
    if not selected_car:
        return Container(
            Style(THEME_STYLE + "body { padding: 20px; }"),
            H1("Car not found")
        )
    try:
        start_dt = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        num_days = (end_dt - start_dt).days
    except Exception as e:
        return Container(
            Style(THEME_STYLE + "body { padding: 20px; }"),
            H1("Invalid date format")
        )
    return Container(
        Style(THEME_STYLE + """
body { padding: 20px; }
.form-container {
    max-width: 600px;
    margin: 40px auto;
    background: rgba(255,255,255,0.95);
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}
.car-details {
    display: flex;
    gap: 20px;
    margin-bottom: 20px;
    align-items: center;
}
.car-image img {
    width: 100px;
    height: auto;
    border-radius: 5px;
    border: 2px solid #90caf9;
}
.car-info {
    font-size: 18px;
    color: #333;
}
.car-info p {
    margin: 5px 0;
}
label { 
    display: block; 
    margin-top: 10px; 
    font-weight: bold; 
    color: #0d47a1;
}
input, select {
    width: 100%;
    padding: 8px;
    margin-top: 5px;
    border: 1px solid #90caf9;
    border-radius: 5px;
}
button {
    margin-top: 20px;
    background: #42a5f5;
    color: #fff;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    cursor: pointer;
    transition: background 0.3s;
}
button:hover { 
    background: #1e88e5; 
}
"""),
        Div(
            H2("Reservation Form", style="text-align: center;"),
            Div(
                Div(
                    Div(
                        H3(selected_car.get_model()),
                        P("License: " + selected_car.get_licensecar()),
                        P("Price per day: " + str(selected_car.get_price())+"bath"),
                        P("Status: " + selected_car.get_status()),
                        P("Color: " + selected_car.get_color()),
                        P("Seats: " + selected_car.get_seat_count()),
                        P("Start Date: " + start_date),
                        P("End Date: " + end_date),
                        P("Total Days: " + str(num_days)),
                        _class="car-info"
                    ),
                    _class="car-details"
                ),
                Form(
                    Input(name="car_id", value=car_id, type="hidden"),
                    Input(name="start_date", type="hidden", value=start_date),
                    Input(name="end_date", type="hidden", value=end_date),
                    Label("Promotion Code (if any):"),
                    Input(name="promotion_code", type="text", placeholder="Enter promotion code"),
                    Label("Do you want insurance:"),
                    Select(
                        Option("No", value="No"),
                        Option("Yes", value="Yes"),
                        name="insurance_option",
                        required=True
                    ),
                    Label("Do you require a driver:"),
                    Select(
                        Option("No", value="No"),
                        Option("Yes", value="Yes"),
                        name="driver_option",
                        required=True
                    ),
                    Button("Reserve Car", type="submit"),
                    action="/reservation", method="POST"
                )
            ),
            _class="form-container"
        )
    )

@rt('/reservation', methods=["POST"])
def save_reservation(car_id: str, start_date: str, end_date: str,
                     promotion_code: str = "", insurance_option: str = "No", driver_option: str = "No"):
    selected_car = None
    for car in company.get_cars():
        if car.get_id() == car_id:
            selected_car = car
            break
    if not selected_car:
        return Container(
            Style(THEME_STYLE + "body { padding: 20px; }"),
            H1("Car not found")
        )
    renter = BackEnd.User(3001, "user1", "pass1", "renter", "U-111")
    try:
        start_dt = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    except Exception as e:
        return Container(
            Style(THEME_STYLE + "body { padding: 20px; }"),
            H1("Invalid date format")
        )
    days = (end_dt - start_dt).days
    if days <= 0:
        return Container(
            Style(THEME_STYLE + "body { padding: 20px; }"),
            H1("Start date must be earlier than end date")
        )
    base_price = selected_car.get_price()
    price = base_price * days
    promotion_instance = None
    promotion_info = "No promotion"
    discount_percent = 0
    promo_code = promotion_code.strip().upper()
    for promo in company.get_promotions():
        if promo.check_promotion(promo_code):
            discount_percent = promo.get_percent()
            promotion_instance = promo
            promotion_info = f"Discount: {discount_percent}%"
            break
    if discount_percent > 0:
        discount = price * (discount_percent / 100)
        price -= discount
    insurance_instance = None
    if insurance_option == "Yes":
        insurance_instance = BackEnd.Insurance("I1", "Basic Insurance", "Standard coverage", 200)
        price += insurance_instance.get_price()
    driver_assigned = None
    if driver_option == "Yes":
        for user in company.get_users():
            if user.get_role() == "driver":
                driver_assigned = user
                break
    selected_car.status_car("unavailable")
    reservation_id = "R" + car_id + "_" + str(int(time.time()))
    reservation = BackEnd.Reservation(
        reservation_id, 
        renter, 
        selected_car, 
        start_date, 
        end_date, 
        price,
        driver=driver_assigned, 
        promotion=promotion_instance, 
        insurance=insurance_instance
    )
    company.add_reservation(reservation)
    return RedirectResponse("/payment?reservation_id=" + reservation.get_id(), status_code=302)

@rt('/reservation/status', methods=["GET"])
def reservation_status(reservation_id: str):
    for res in company.get_reservations():
        if res.get_id() == reservation_id:
            driver_approved = res.get_driver() is None or res.is_driver_approved()
            if res.is_admin_approved() and driver_approved:
                if not res.is_paid():
                    return RedirectResponse("/payment?reservation_id=" + reservation_id, status_code=302)
                else:
                    return Container(
                        Style(THEME_STYLE + "body { padding: 20px; }"),
                        H2("Reservation Successful", style="color: green;"),
                        P("Reservation ID: " + reservation_id)
                    )
            else:
                admin_status = "Approved" if res.is_admin_approved() else "Pending"
                driver_status = "Not required" if res.get_driver() is None else ("Approved" if res.is_driver_approved() else "Pending")
                return Container(
                    Style(THEME_STYLE + "body { padding: 20px; }"),
                    H2("Reservation Status"),
                    P("Reservation ID: " + reservation_id),
                    P("Admin Approval: " + admin_status),
                    P("Driver Approval: " + driver_status),
                    P("Please check back later for updated status")
                )
    return Container(
        Style(THEME_STYLE + "body { padding: 20px; }"),
        H1("Reservation not found")
    )

serve()
