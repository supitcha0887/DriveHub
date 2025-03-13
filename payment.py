from fasthtml.common import *
from routing import app, rt
import BackEnd, datetime, time

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
    background-size: cover;
}
"""

@rt('/payment', methods=["GET"])
def payment_page(reservation_id: str):
    reservation = None
    for res in company.get_reservations():
        if res.get_id() == reservation_id:
            reservation = res
            break
    if not reservation:
        return Container(
            Style(THEME_STYLE + "body { padding: 20px; }"),
            H1("Reservation not found")
        )
    
    car = reservation.get_car()
    car_model = car.get_model()
    car_license = car.get_licensecar()
    car_price = car.get_price()
    car_status = car.get_status()
    car_color = car.get_color()
    car_seats = car.get_seat_count()
    
    start_date = reservation.get_start_date()
    end_date = reservation.get_end_date()
    try:
        start_dt = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        num_days = (end_dt - start_dt).days
    except Exception as e:
        num_days = 0

    insurance_cost = reservation.get_insurance().get_price() if reservation.get_insurance() else 0
    total_cost = reservation.get_price()
    base_total = car_price * num_days
    discount_amount = (base_total + insurance_cost) - total_cost
    if discount_amount < 0:
        discount_amount = 0

    return Container(
        Style("""
html, body {
    height: 100%;
    font-family: 'Roboto', sans-serif;
    margin: 0;
    padding: 0;
    background: linear-gradient(135deg, #bbdefb, #e3f2fd);
    background-size: cover;
}
.header {
    width: 100%;
    background: #e3f2fd;
    padding: 25px;
    border-bottom: 2px solid #90caf9;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    display: flex;
    align-items: center;
}
.header h2 {
    color: #0d47a1;
    margin: 0;
    font-size: 42px;
    letter-spacing: 2px;
}
.content {
    max-width: 600px;
    margin: 40px auto;
    background: rgba(255,255,255,0.95);
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}
.content h3, .content h4 {
    margin: 10px 0;
    color: #0d47a1;
}
.content p {
    margin: 10px 0;
    font-size: 18px;
    color: #333;
}
label {
    font-weight: bold;
}
.payment-options {
    margin-bottom: 20px;
}
button {
    background: linear-gradient(45deg, #2196F3, #21CBF3);
    color: #fff;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    cursor: pointer;
    transition: background 0.3s;
}
button:hover {
    background: linear-gradient(45deg, #1976D2, #1E88E5);
}
#credit-card-info, #qrcode-info {
    display: none;
    margin-top: 10px;
}
"""),
        Div(
            Body(
                Div(
                    H2("Payment Form", style="text-align: center;"),
                    H3("Payment Details", style="margin-bottom:15px;"),
                    P("Reservation ID: " + reservation_id),
                    H4("Car Details:"),
                    P("Model: " + car_model),
                    P("License: " + car_license),
                    P("Price per day: " + str(car_price)+"bath"),
                    P("Status: " + car_status),
                    P("Color: " + car_color),
                    P("Seats: " + car_seats),
                    H4("Reservation Period:"),
                    P("Start Date: " + start_date),
                    P("End Date: " + end_date),
                    P("Total Days: " + str(num_days)),
                    H4("Additional Costs:"),
                    P("Insurance Cost: " + str(insurance_cost)+"bath"),
                    P("Promotion Discount: " + str(discount_amount)+"bath"),
                    H4("Total Cost:"),
                    P( str(total_cost), style="font-weight:bold;"+"bath"),
                    Form(
                        Div(
                            Label("Select Payment Method:"),
                            Div(
                                Input(type="radio", name="payment_method", value="creditcard", required=True, _class="payment-option"),
                                Label("Credit Card Payment")
                            ),
                            Div(
                                Input(type="radio", name="payment_method", value="qrcode", required=True, _class="payment-option"),
                                Label("QR Code Payment")
                            )
                        ),
                        Div(
                            Div(
                                Label("Cardholder Name:"),
                                Input(name="cardholder_name", type="text", placeholder="Enter your name")
                            ),
                            Div(
                                Label("Credit Card Number:"),
                                Input(name="card_number", type="text", placeholder="Enter card number")
                            ),
                            _id="credit-card-info"
                        ),
                        Div(
                            Img(src="/static/images/qrcode.png", alt="QR Code Placeholder", style="width:100px; height:auto;"),
                            _id="qrcode-info"
                        ),
                        Input(type="hidden", name="reservation_id", value=reservation_id),
                        Button("Pay Now", type="submit"),
                        action="/payment/process", method="POST"
                    ),
                    Script("""
document.querySelectorAll("input[name='payment_method']").forEach(function(radio) {
    radio.addEventListener('change', function() {
        if (this.value === 'creditcard') {
            document.getElementById('credit-card-info').style.display = 'block';
            document.getElementById('qrcode-info').style.display = 'none';
        } else if (this.value === 'qrcode') {
            document.getElementById('credit-card-info').style.display = 'none';
            document.getElementById('qrcode-info').style.display = 'block';
        }
    });
});
"""),
                    _class="content"
                ),
                style="padding: 20px; min-height: 100vh;"
            )
        )
    )

@rt('/payment/process', methods=["POST"])
def process_payment(reservation_id: str, payment_method: str, cardholder_name: str = "", card_number: str = ""):
    if payment_method == "creditcard":
         payment_instance = BackEnd.Payment("Pay" + reservation_id, creditcard=f"{cardholder_name}:{card_number}")
    elif payment_method == "qrcode":
         payment_instance = BackEnd.Payment("Pay" + reservation_id, qrcode="qrcode")
    else:
         payment_instance = BackEnd.Payment("Pay" + reservation_id)
    
    company.add_payment(payment_instance)
    
    for res in company.get_reservations():
         if res.get_id() == reservation_id:
              res.mark_paid()
              break
    return RedirectResponse("/reservation/status?reservation_id=" + reservation_id, status_code=302)

serve()
