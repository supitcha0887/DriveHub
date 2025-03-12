from fasthtml.common import *
from routing import app, rt
import BackEnd
import time

company = BackEnd.company

# กำหนด Theme สำหรับหน้าจอ
THEME_STYLE = """
    html, body {
        height: 100%;
        font-family: 'Roboto', sans-serif;
        margin: 0;
        padding: 0;
        background: linear-gradient(135deg, #0052d4, #4364f7, #6fb1fc);
        background-size: cover;
    }
"""

# หน้าจอสำหรับกรอกข้อมูลจองรถ รวมถึงช่องกรอกรหัสโปรโมชั่น
@rt('/reservation/form', methods=["GET"])
def reservation_form(car_id: str = "", start_date: str = "", end_date: str = ""):
    return Container(
        Style(
            THEME_STYLE + """
            body { padding: 20px; }
            .form-container {
                max-width: 500px;
                margin: 40px auto;
                background: #FFF;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.2);
            }
            label {
                display: block;
                margin-top: 10px;
                font-weight: bold;
            }
            input {
                width: 100%;
                padding: 8px;
                margin-top: 5px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            button {
                margin-top: 20px;
                background: #0052d4;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
            }
            button:hover {
                background: #003bb5;
            }
            """
        ),
        Div(
            H2("จองรถ", style="text-align: center;"),
            Form(
                Input(name="car_id", value=car_id, type="hidden"),
                Label("วันที่เริ่มเช่า:"),
                Input(name="start_date", type="date", value=start_date),
                Label("วันที่สิ้นสุดเช่า:"),
                Input(name="end_date", type="date", value=end_date),
                # ช่องกรอกรหัสโปรโมชั่น
                Label("รหัสโปรโมชั่น (ถ้ามี):"),
                Input(name="promotion_code", type="text", placeholder="ระบุรหัสโปรโมชั่น"),
                Button("จองรถ", type="submit"),
                action="/reservation", method="POST"
            ),
            _class="form-container"
        )
    )

# บันทึกการจองรถ พร้อมคำนวณราคาจากโปรโมชั่น
@rt('/reservation', methods=["POST"])
def save_reservation(car_id: str, start_date: str, end_date: str,
                     promotion_code: str = ""):
    # ค้นหารถที่ต้องการจอง
    selected_car = None
    for car in company.get_cars():
        if car.get_id() == car_id:
            selected_car = car
            break
    if not selected_car:
        return Container(
            Style(THEME_STYLE + "body { padding: 20px; }"),
            H1("ไม่พบข้อมูลรถที่ต้องการจอง")
        )
    
    # กำหนดข้อมูลผู้เช่า (ในระบบจริงควรดึงจาก session)
    renter = BackEnd.User(3001, "user1", "pass1", "renter", "U-111")
    
    # คำนวณราคาจากโปรโมชั่น (ถ้ามี)
    base_price = selected_car.get_price()
    price = base_price
    promotion_instance = None
    promotion_info = "ไม่มีโปรโมชั่น"
    
    if promotion_code.strip() != "":
        try:
            percent = float(promotion_code.strip())
        except ValueError:
            percent = 0.0
        discount = base_price * (percent / 100)
        price = base_price - discount
        promotion_info = f"ลด {percent}%"

    reservation_id = "R" + car_id + "_" + str(int(time.time()))
    reservation = BackEnd.Reservation(
        reservation_id, 
        renter, 
        selected_car, 
        start_date, 
        end_date, 
        price,
        driver=None, 
        promotion=None, 
        insurance=None
    )
    company.add_reservation(reservation)
    
    # แสดงรายละเอียดการจอง พร้อมแจ้งให้รอการอนุมัติจาก Admin และ Driver
    reservation_details = Div(
        H3("รายละเอียดการจอง"),
        P("Reservation ID: " + reservation.get_id()),
        P("Renter: " + reservation.get_renter().get_username()),
        P("วันที่เริ่มเช่า: " + start_date),
        P("วันที่สิ้นสุดเช่า: " + end_date),
        P("ราคาที่คำนวณ: " + str(reservation.get_price())),
        P("โปรโมชั่น: " + promotion_info)
    )
    
    info_message = Div(
        P("ระบบกำลังรอการอนุมัติจาก Admin และ Driver..."),
        P("เมื่อได้รับการอนุมัติแล้ว กรุณาตรวจสอบสถานะ "),
        A("ตรวจสอบสถานะ", href="/reservation/status?reservation_id=" + reservation.get_id())
    )
    
    return Container(
        Style(THEME_STYLE + """
            body { padding: 20px; }
            .message {
                max-width: 600px;
                margin: 40px auto;
                background: #FFF;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.2);
                text-align: center;
            }
            a {
                color: #0052d4;
                text-decoration: underline;
                cursor: pointer;
            }
            """
        ),
        Div(
            reservation_details,
            info_message,
            _class="message"
        )
    )

# ตรวจสอบสถานะ Reservation ถ้าอนุมัติครบแล้ว Redirect ไปยัง Payment
@rt('/reservation/status', methods=["GET"])
def reservation_status(reservation_id: str):
    for res in company.get_reservations():
        if res.get_id() == reservation_id:
            if res.is_admin_approved() and res.is_driver_approved():
                return RedirectResponse("/payment?reservation_id=" + reservation_id, status_code=302)
            else:
                admin_status = "Approved" if res.is_admin_approved() else "ยังไม่อนุมัติ"
                driver_status = "Approved" if res.is_driver_approved() else "ยังไม่อนุมัติ"
                return Container(
                    Style(THEME_STYLE + "body { padding: 20px; }"),
                    H2("สถานะการจอง"),
                    P("Reservation ID: " + reservation_id),
                    P("สถานะอนุมัติจาก Admin: " + admin_status),
                    P("สถานะอนุมัติจาก Driver: " + driver_status),
                    P("กรุณาตรวจสอบใหม่ภายหลังเมื่อได้รับการอนุมัติ")
                )
    return Container(
        Style(THEME_STYLE + "body { padding: 20px; }"),
        H1("ไม่พบข้อมูล Reservation")
    )

serve()
