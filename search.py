from fasthtml.common import *
from routing import app, rt
import BackEnd, time

company = BackEnd.company

@rt('/search', methods=["GET"])
def search():
    search_section = Div(
        Div(
            Div(
                H2("DRIVY", style="color: #FFF; margin: 0; font-size: 42px; letter-spacing: 2px;"),
                style="display: flex; align-items: center;"
            ),
            style="display: flex; justify-content: space-between; align-items: center; width: 100%;"
        ),
        style="""
            width: 100%;
            background: rgba(0,0,0,0.6);
            padding: 25px;
            border-bottom: 2px solid rgba(0,0,0,0.3);
            position: fixed;
            top: 0;
            left: 0;
            z-index: 1000;
        """
    )
    
    # Search form with date validation via JavaScript
    search_form = Div(
        Form(
            Div(
                Div(
                    Label("Model", style="color: #1C1C3B; font-size: 18px; font-weight: bold;"),
                    Select(
                        Option("All"),
                        *[Option(car.get_model(), value=car.get_model()) for car in company.get_cars()],
                        id="model",
                        name="model",
                        style="background: #fff; padding: 8px; border-radius: 15px; border: 1px solid #1C1C3B; width: 100%;"
                    )
                ),
                Div(
                    Label("Start Date", style="color: #1C1C3B; font-size: 18px; font-weight: bold;"),
                    Input(type="date", id="start_date", name="start_date", required=True)
                ),
                Div(
                    Label("End Date", style="color: #1C1C3B; font-size: 18px; font-weight: bold;"),
                    Input(type="date", id="end_date", name="end_date", required=True)
                ),
                style="display: grid; gap: 15px;"
            ),
            Button("Search", type="submit", style="background: #2196F3; color: white; font-weight: bold; padding: 10px 20px; border: none; border-radius: 20px; cursor: pointer; margin-top: 20px; width: 100%;"),
            method="get",
            action="/cal",
            _class="search-form",
            style="max-width: 500px; margin: auto; background: #fff; padding: 20px; border-radius: 10px; box-shadow: 0px 2px 4px rgba(0,0,0,0.2);"
        ),
        style="margin-top: 120px;"
    )
    
    # JavaScript for validating start_date < end_date
    date_validation_script = Script("""
        document.querySelector('.search-form').addEventListener('submit', function(e) {
            var startDate = new Date(document.getElementById('start_date').value);
            var endDate = new Date(document.getElementById('end_date').value);
            if (startDate >= endDate) {
                alert('Start Date ต้องน้อยกว่า End Date');
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
            # ตรวจสอบ driver approval แบบเดียวกับที่เราแก้ไขใน reservation/status
            driver_approved = res.get_driver() is None or res.is_driver_approved()
            if res.is_admin_approved() and driver_approved:
                if not res.is_paid():
                    payment_status = A("ยังไม่ได้ชำระ", href="/payment?reservation_id=" + res.get_id(), style="color: red; font-weight: bold; font-size:18px;")
                    rating_form = ""  # ไม่แสดง rating เพราะยังไม่ชำระ
                else:
                    payment_status = P("จองสำเร็จ", style="color: green; font-weight: bold; font-size:18px;")
                    # แสดงฟอร์ม rating เฉพาะเมื่อจองสำเร็จ
                    rating_form = Form(
                        Input(name="reservation_id", value=res.get_id(), type="hidden"),
                        Div(
                            Label("Rating:"), 
                            Input(name="rating", type="number", min="0", max="5", step="0.1", required=True)
                        ),
                        Div(
                            Label("Comment:"), 
                            Input(name="comment", type="text", required=True)
                        ),
                        Button("Submit Rating", type="submit"),
                        action="/reservation/rate", method="POST"
                    )
            else:
                payment_status = P("รอการอนุมัติ", style="color: orange; font-weight: bold; font-size:18px;")
                # ถ้ายังรออนุมัติ ไม่ให้แสดงฟอร์ม rating
                rating_form = ""
            
            # ถ้ามีประกัน ให้แสดงรายละเอียดเบี้ยประกัน
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
                    Style("border: 1px solid #ddd; padding: 15px; margin-bottom: 15px; border-radius: 5px; background: #fff;")
                )
            )
    else:
        reservation_list.append(P("ไม่มีประวัติการจอง", style="font-size:20px; text-align:center;"))
    
    reservation_section = Div(
        Div(
            H2("ประวัติการจองของฉัน", style="color: #fff; margin: 0; font-size: 32px;"),
            _class="header"
        ),
        Div(
            H3("ยินดีต้อนรับ " + current_user.get_username(), style="color: #333;"),
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
                background: linear-gradient(135deg, #2196F3, #21CBF3);
                background-size: cover;
            }
            .header {
                text-align: center;
            }
            .content {
                max-width: 800px;
                margin: 20px auto;
                background: rgba(255,255,255,0.95);
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            }
        """),
        search_section,
        Body(
            search_form,
            reservation_section,
            style="padding: 20px; min-height: 100vh; margin-top: 80px;"
        ),
        date_validation_script  # แทรกสคริปต์การตรวจสอบวันที่
    )

@rt('/reservation/rate', methods=["POST"])
def rate_car(reservation_id: str, rating: float, comment: str):
    for res in company.get_reservations():
        if res.get_id() == reservation_id:
            car = res.get_car()
            car.add_rating_car(float(rating))
            car.add_review_car(BackEnd.Review(comment, time.strftime("%Y-%m-%d")))
            return RedirectResponse("/search", status_code=302)
    return Container(
         Style("body { font-family: Arial; background: #F5F5F5; padding: 20px; }"),
         H1("ไม่พบ Reservation ที่ต้องการให้ Rate")
    )

@rt('/cal', methods=["GET", "POST"])
def cal_data(model: str, start_date: str, end_date: str):
    return RedirectResponse(f"/showcar/{model}/{start_date}/{end_date}")

serve()
