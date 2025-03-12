from fasthtml.common import *
from routing import app, rt
import BackEnd
company = BackEnd.company

@rt('/showcar', methods=["GET"])
def showcar(allcar: str = "All"):
    # กรองรายชื่อรถตามรุ่นที่เลือก ถ้าเลือก "All" ให้แสดงทุกคัน
    if allcar == "All":
        filtered_cars = company.get_cars()
    else:
        filtered_cars = [car for car in company.get_cars() if car.get_model() == allcar]
    
    return Container(
        Style("""
            body {
                font-family: Arial, sans-serif;
                background: #AEEEEE;
                padding: 20px;
            }
            /* แถบ header ด้านบน */
            .header {
                width: 100%;
                background: #4682B4;
                padding: 25px;
                border-bottom: 2px solid #502314;
                position: fixed;
                top: 0;
                left: 0;
                z-index: 1000;
            }
            .header h2 {
                color: #B0E0E6;
                margin: 0;
            }
            /* ส่วนเนื้อหาหลัก */
            .content {
                margin-top: 80px; /* ให้มีระยะห่างจาก header */
            }
            /* Card สำหรับแต่ละรถ */
            .card {
                background: #fff;
                border-radius: 10px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.2);
                margin-bottom: 20px;
                overflow: hidden;
            }
            .card img {
                width: 300px;      /* กำหนดขนาดภาพให้เล็กลง */
                height: auto;
                display: block;
                margin: auto;
            }
            .card-details {
                padding: 20px;
                text-align: center;
            }
            .card-details h3 {
                margin: 0 0 10px;
                font-size: 28px;
            }
            .card-details p {
                margin: 5px 0;
                font-size: 18px;
            }
            .select-btn {
                margin-top: 15px;
                background: #1C1C3B;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                outline: none;
            }
            .select-btn:hover {
                background: #45a049;
            }
            .select-btn:active {
                background: #1C1C3B;
            }
        """),
        Div(
            # แถบ header ด้านบน
            Div(
                H2("DRIVY", style="color: #fff; margin: 0;"),
                _class="header"
            ),
            # ส่วนเนื้อหาหลัก แสดง card รถ
            Div(
                *[
                    Div(
                        # ภาพรถ (ปรับขนาดให้เล็กลง)
                        Img(src=car.get_image(), alt="Car Image"),
                        # รายละเอียดรถ
                        Div(
                            H3(car.get_model()),
                            P("License: " + car.get_licensecar()),
                            P("Price: " + str(car.get_price())),
                            P("Status: " + car.get_status()),
                            P("Color: " + car.get_color()),
                            P("Seat Count: " + car.get_seat_count()),
                            # Form สำหรับปุ่ม Select ที่จะนำไปหน้า reservation
                            Form(
                                Input(type="hidden", name="car_id", value=car.get_id()),
                                Input(type="hidden", name="start_date", value="2025-03-12"),
                                Input(type="hidden", name="end_date", value="2025-03-13"),
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
