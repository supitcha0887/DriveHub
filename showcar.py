from fasthtml.common import *
from routing import app, rt
import BackEnd
company = BackEnd.company

@rt('/showcar/{model}/{start_date}/{end_date}', methods=["GET"])
def showcar(model: str, start_date: str, end_date: str):
    # กรองรายชื่อรถตามรุ่นที่เลือก ถ้าเลือก "All" ให้แสดงทุกคัน
    if model == "All":
        filtered_cars = company.get_cars()
    else:
        filtered_cars = [car for car in company.get_cars() if car.get_model() == model]
    
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
            /* Header ด้านบน */
            .header {
                width: 100%;
                background: rgba(0,0,0,0.5);
                padding: 25px;
                position: fixed;
                top: 0;
                left: 0;
                z-index: 1000;
                text-align: center;
            }
            .header h2 {
                color: #fff;
                margin: 0;
                font-size: 42px;
                letter-spacing: 2px;
            }
            /* ส่วนเนื้อหาหลัก */
            .content {
                margin-top: 100px;
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
                padding: 20px;
            }
            /* Card สำหรับแต่ละรถ */
            .card {
                background: #fff;
                border-radius: 10px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.2);
                overflow: hidden;
                display: flex;
                flex-direction: column;
            }
            .card img {
                width: 100%;
                height: auto;
                display: block;
            }
            .card-details {
                padding: 20px;
                text-align: center;
                flex-grow: 1;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
            }
            .card-details h3 {
                margin: 0 0 10px;
                font-size: 28px;
                color: #0052d4;
            }
            .card-details p {
                margin: 5px 0;
                font-size: 16px;
            }
            .review-section {
                max-height: 100px;
                overflow-y: auto;
                text-align: left;
                margin-top: 10px;
                font-size: 14px;
            }
            .select-btn {
                margin-top: 15px;
                background: #0052d4;
                color: #fff;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                outline: none;
                transition: background 0.3s;
            }
            .select-btn:hover {
                background: #003bb5;
            }
            .select-btn:active {
                background: #0052d4;
            }
            /* Form ภายใน card */
            form {
                margin-top: 10px;
            }
        """),
        Div(
            # Header ด้านบน
            Div(
                H2("DRIVY", style="margin: 0;"),
                _class="header"
            ),
            # ส่วนเนื้อหาหลัก แสดง card รถ
            Div(
                *[ 
                    Div(
                        # ภาพรถ
                        Img(src=car.get_image(), alt="Car Image"),
                        # รายละเอียดรถ
                        Div(
                            H3(car.get_model()),
                            P("License: " + car.get_licensecar()),
                            P("Price: " + str(car.get_price())),
                            P("Status: " + car.get_status()),
                            P("Color: " + car.get_color()),
                            P("Seat Count: " + car.get_seat_count()),
                            P("Start: " + start_date),
                            P("End: " + end_date),
                            P("Average Rating: " + str(round(car.cal_rating(), 1))),
                            Div(
                                *[P("Review: " + rev.get_comment() + " (Date: " + rev.get_date() + ")", style="margin: 2px 0;")
                                  for rev in car.get_reviews()],
                                _class="review-section"
                            ),
                            # Form สำหรับเลือกรถ (ส่งไปหน้า /reservation)
                            Form(
                                Input(type="hidden", name="car_id", value=car.get_id()),
                                Input(type="hidden", name="start_date", value=start_date),
                                Input(type="hidden", name="end_date", value=end_date),
                                Button("Select", type="submit", _class="select-btn"),
                                action="/reservation", method="POST"
                            ),
                            _class="card-details"
                        ),
                        _class="card"
                    ) for car in filtered_cars
                ],
                _class="content"
            )
        )
    )

serve()
