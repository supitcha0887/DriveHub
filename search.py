from fasthtml.common import *
from routing import app, rt
import BackEnd
import time

company = BackEnd.company

@rt('/search', methods=["GET"])
def search():
    # ส่วนของ Search Header
    search_section = Div(
        Div(
            Div(
                H2("DRIVY", style="color: #FFF; margin: 0; font-size: 42px; letter-spacing: 2px;"),
                style="display: flex; align-items: center; gap: 0px;"
            ),
            style="display: flex; justify-content: space-between; align-items: center; width: 100%;"
        ),
        style=""" 
            width: 100%; 
            background: rgba(0,0,0,0.5); 
            padding: 25px; 
            border-bottom: 2px solid rgba(0,0,0,0.3); 
            position: fixed; 
            top: 0; 
            left: 0; 
            z-index: 1000;
        """
    )
    
    # ฟอร์มค้นหารถ (ส่งไปหน้า /showcar)
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
                    Input(type="date", id="start_date", name="start_date")
                ),
                Div(
                    Label("End Date", style="color: #1C1C3B; font-size: 18px; font-weight: bold;"),
                    Input(type="date", id="end_date", name="end_date", min="start_date")
                ),
                style="display: grid; gap: 15px;"
            ),
            Button("Search", type="submit", style="background: #0052d4; color: white; font-weight: bold; padding: 10px 20px; border: none; border-radius: 20px; cursor: pointer; margin-top: 20px; width: 100%;"),
            method="get",
            action="/cal",
            _class="search-form",
            style="max-width: 500px; margin: auto; background: #fff; padding: 20px; border-radius: 10px; box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.2);"
        ),
        style="margin-top: 120px;"  # ให้มีระยะห่างจาก header
    )
    
    # ส่วนของ "ประวัติการจองของฉัน" พร้อมแสดงข้อมูล rating และ comment
    # (ในระบบจริงควรดึงข้อมูลผู้ใช้จาก session แต่ที่นี้ใช้ user1 เป็นตัวอย่าง)
    current_user = BackEnd.User(3001, "user1", "pass1", "renter", "U-111")
    my_reservations = [res for res in company.get_reservations() if res.get_renter().get_username() == current_user.get_username()]

    reservation_list = []
    if my_reservations:
        for res in my_reservations:
            car = res.get_car()
            # สร้างรายการรีวิวจากรถ
            reviews_display = Div(
                *[P("Review: " + rev.get_comment() + " (Date: " + rev.get_date() + ")") for rev in car.get_reviews()]
            )
            reservation_list.append(
                Div(
                    P("Reservation ID: " + res.get_id()),
                    P("Car Model: " + car.get_model()),
                    P("Start Date: " + res.get_start_date()),
                    P("End Date: " + res.get_end_date()),
                    P("Price: " + str(res.get_price())),
                    P("Average Rating: " + str(round(car.cal_rating(), 1))),
                    reviews_display,
                    # ฟอร์มสำหรับให้คะแนนและคอมเมนต์ (rating เป็นตัวเลข 0-5)
                    Form(
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
                    ),
                    Style("border: 1px solid #ddd; padding: 10px; margin-bottom: 10px; border-radius: 5px;")
                )
            )
    else:
        reservation_list.append(P("ไม่มีประวัติการจอง"))
        
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
    
    # รวมทั้ง Search Form และ Reservation History ในหน้าเดียวกัน
    return Container(
        Style("""
            html, body {
                height: 100%;
                font-family: 'Roboto', sans-serif;
                margin: 0;
                padding: 0;
                background: linear-gradient(135deg, #0052d4, #4364f7, #6fb1fc);
                background-size: cover;
            }
            .header {
                text-align: center;
            }
            .content {
                max-width: 800px;
                margin: 20px auto;
                background: #fff;
                border-radius: 10px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.2);
            }
        """),
        search_section,
        Body(
            search_form,
            reservation_section,
            style="padding: 20px; min-height: 100vh; margin-top: 80px;"
        )
    )

@rt('/reservation/rate', methods=["POST"])
def rate_car(reservation_id: str, rating: float, comment: str):
    # ค้นหา Reservation ตาม reservation_id แล้วเพิ่ม rating และ comment ให้กับรถ
    for res in company.get_reservations():
        if res.get_id() == reservation_id:
            car = res.get_car()
            car.add_rating_car(float(rating))
            car.add_review_car(BackEnd.Review(comment, time.strftime("%Y-%m-%d")))
            # Redirect กลับไปที่หน้า /search หลังจากให้คะแนนแล้ว
            return RedirectResponse("/search", status_code=302)
    return Container(
         Style("body { font-family: Arial; background: #F5F5F5; padding: 20px; }"),
         H1("ไม่พบ Reservation ที่ต้องการให้ Rate")
    )

@rt('/cal', methods=["GET", "POST"])
def cal_data(model: str, start_date: str, end_date: str):
    # Redirect ไปยัง showcar พร้อม query parameters
    return RedirectResponse(f"/showcar/{model}/{start_date}/{end_date}")

serve()
