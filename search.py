from fasthtml.common import *
from routing import app, rt
import BackEnd, time

company = BackEnd.company

@rt('/search', methods=["GET"])
def search():
    search_section = Div(
        Div(
            Div(
                Img(src="/static/images/logo.png", alt="Drivy Logo", style="width: 70px; height: auto; margin-right: 10px;"),
                H2("DRIVY", style="color: #0d47a1; margin: 0; font-size: 42px; letter-spacing: 2px;"),
                style="display: flex; align-items: center;"
            ),
            style="display: flex; justify-content: space-between; align-items: center; width: 100%;"
        ),
        style="""
            width: 100%;
            background: #e3f2fd;
            padding: 25px;
            border-bottom: 2px solid #90caf9;
            position: fixed;
            top: 0;
            left: 0;
            z-index: 1000;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        """
    )
    back_button = A(
        Img(src="/static/images/back_icon.png", alt="Back", style="width:40px; height:auto;"),
        href="/search"
    )
    search_form = Div(
        Form(
            Div(
                Div(
                    Label("Model", style="color: #0d47a1; font-size: 18px; font-weight: bold;"),
                    Select(
                        Option("All"),
                        *[Option(car.get_model(), value=car.get_model()) for car in company.get_cars() if car.get_status() == "available"],
                        id="model",
                        name="model",
                        style="background: #ffffff; padding: 8px; border-radius: 8px; border: 1px solid #90caf9; width: 100%;"
                    )
                ),
                Div(
                    Label("Start Date", style={"color": "#0d47a1", "font-size": "18px", "font-weight": "bold"}),
                    Input(type="date", id="start_date", name="start_date", required=True, style={"border-radius": "8px", "border": "1px solid #90caf9", "width": "100%"})
                ),
                Div(
                    Label("End Date", style={"color": "#0d47a1", "font-size": "18px", "font-weight": "bold"}),
                    Input(type="date", id="end_date", name="end_date", required=True, style={"border-radius": "8px", "border": "1px solid #90caf9", "width": "100%"})
                ),
                style="display: grid; gap: 15px;"
            ),
            Button("Search", type="submit", style="background: #42a5f5; color: white; font-weight: bold; padding: 10px 20px; border: none; border-radius: 8px; cursor: pointer; margin-top: 20px; width: 100%;"),
            method="get",
            action="/cal",
            _class="search-form",
            style="max-width: 500px; margin: auto; background: #f1f8ff; padding: 20px; border-radius: 10px; box-shadow: 0px 2px 4px rgba(0,0,0,0.1);"
        ),
        style="margin-top: 120px;"
    )
    date_validation_script = Script("""
        document.querySelector('.search-form').addEventListener('submit', function(e) {
            var startDate = new Date(document.getElementById('start_date').value);
            var endDate = new Date(document.getElementById('end_date').value);
            if (startDate >= endDate) {
                alert('Start Date must be earlier than End Date');
                e.preventDefault();
            }
        });
    """)
    current_user = BackEnd.User(3001, "user1", "pass1", "renter", "U-111")
    my_reservations = [res for res in company.get_reservations() if res.get_renter().get_username() == current_user.get_username()]
    reservation_list = []
    if my_reservations:
        for res in my_reservations:
            car = res.get_car()
            reviews_display = Div(
                *[P("Review: " + rev.get_comment() + " (Date: " + rev.get_date() + ")", style="font-size:14px;") for rev in car.get_reviews()]
            )
            driver_approved = res.get_driver() is None or res.is_driver_approved()
            if res.is_admin_approved() and driver_approved:
                if not res.is_paid():
                    payment_status = A("Not Paid", href="/payment?reservation_id=" + res.get_id(), style="color: red; font-weight: bold; font-size:18px;")
                    rating_form = ""
                else:
                    payment_status = P("Booking Confirmed", style="color: green; font-weight: bold; font-size:18px;")
                    rating_form = Form(
                        Input(name="reservation_id", value=res.get_id(), type="hidden"),
                        Div(
                            Label("Rating:"), 
                            Input(name="rating", type="number", min="1", max="5", step="1", required=True)
                        ),
                        Div(
                            Label("Comment:"), 
                            Input(name="comment", type="text", required=True)
                        ),
                        Button("Submit Rating", type="submit"),
                        action="/reservation/rate", method="POST"
                    )
            else:
                print(res.get_status())
                if res.get_status() == "Canceled":
                    payment_status = P("Canceled", style="color: red; font-weight: bold; font-size:18px;")
                else:
                    payment_status = P("Pending Approval", style="color: orange; font-weight: bold; font-size:18px;")
                rating_form = ""
            insurance_info = ""
            if res.get_insurance():
                insurance_info = f" with insurance: $ {str(res.get_insurance().get_price())}"
            reservation_list.append(
                Div(
                    P("Reservation ID: " + res.get_id(), style="font-size:18px;"),
                    P("Car Model: " + car.get_model(), style="font-size:18px;"),
                    P("Start Date: " + res.get_start_date(), style="font-size:18px;"),
                    P("End Date: " + res.get_end_date(), style="font-size:18px;"),
                    P("Price: $" + str(res.get_price()) + insurance_info, style="font-size:18px;"),
                    P("Average Rating: " + str(round(car.cal_rating(), 1)), style="font-size:18px;"),
                    reviews_display,
                    payment_status,
                    rating_form,
                    Style("border: 1px solid #ddd; padding: 15px; margin-bottom: 15px; border-radius: 5px; background: #ffffff;")
                )
            )
    else:
        reservation_list.append(P("No reservation history", style="font-size:20px; text-align:center;"))
    reservation_section = Div(
        Div(
            H2("My Reservations", style="color: #0d47a1; margin: 0; font-size: 32px;"),
            _class="header"
        ),
        Div(
            H3("Welcome", style="color: #0d47a1;"),
            *reservation_list,
            _class="content",
            style="padding: 20px;"
        ),
        style="margin-top: 40px;"
    )
    return Container(
        Style("""
html, body {
    height: 100%;
    font-family: 'Roboto', sans-serif;
    margin: 0;
    padding: 0;
    background: linear-gradient(135deg, #bbdefb, #e3f2fd);
}
.header {
    text-align: center;
}
.content {
    max-width: 800px;
    margin: 20px auto;
    background: #ffffff;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}
"""),
        search_section,
        Body(
            search_form,
            reservation_section,
            style="padding: 20px; min-height: 100vh; margin-top: 80px;"
        ),
        date_validation_script
    )

@rt('/reservation/rate', methods=["POST","GET"])
def rate_car(reservation_id: str, rating: float, comment: str):
    for res in company.get_reservations():
        if res.get_id() == reservation_id:
            car = res.get_car()
            car.add_rating_car(float(rating))
            car.add_review_car(BackEnd.Review(comment, time.strftime("%Y-%m-%d")))
            print("Reviews:", car.get_reviews())  # เช็คว่ามีข้อมูลหรือไม่
            print("Ratings:", car.get_ratings())  # เช็คว่ามีข้อมูลหรือไม่
    return RedirectResponse("/search", status_code=302)

@rt('/cal', methods=["GET", "POST"])
def cal_data(model: str, start_date: str, end_date: str):
    return RedirectResponse(f"/showcar/{model}/{start_date}/{end_date}")

serve()
