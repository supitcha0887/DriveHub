from fasthtml.common import *
from routing import app, rt
import BackEnd
import time

company = BackEnd.company

# ส่วน Theme CSS สำหรับทุกหน้าจอ (ใช้ gradient น้ำเงินไล่สี)
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

# Endpoint สำหรับแสดงฟอร์มจองรถ
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
                Label("รหัสโปรโมชั่น (ถ้ามี):"),
                Input(name="promotion_code", type="text", placeholder="ระบุรหัสโปรโมชั่น"),
                Button("จองรถ", type="submit"),
                action="/reservation", method="POST"
            ),
            _class="form-container"
        )
    )

# Endpoint สำหรับบันทึก Reservation
@rt('/reservation', methods=["POST"])
def save_reservation(car_id: str, start_date: str, end_date: str,
                     promotion_code: str = ""):
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
    
    # กำหนดข้อมูลผู้เช่า (ในระบบจริงควรดึงมาจาก session)
    renter = BackEnd.User(3001, "user1", "pass1", "renter", "U-111")
    base_price = selected_car.get_price()
    price = base_price
    promotion_instance = None
    promotion_info = "ไม่มีโปรโมชั่น"
    
    if promotion_code != "":
        for promo in company.get_promotions():
            if promo.check_promotion(promotion_code):
                promotion_instance = promo
                discount = base_price * (promo.get_percent() / 100)
                price = base_price - discount
                promotion_info = "ลด " + str(promo.get_percent()) + "%"
                break

    reservation_id = "R" + car_id + "_" + str(int(time.time()))
    reservation = BackEnd.Reservation(reservation_id, renter, selected_car, start_date, end_date, price,
                                      driver=None, promotion=promotion_instance, insurance=None)
    company.add_reservation(reservation)
    
    admin_status = "Approved" if reservation.is_admin_approved() else "ยังไม่อนุมัติ"
    driver_status = "Approved" if reservation.is_driver_approved() else "ยังไม่อนุมัติ"
    can_pay = reservation.is_admin_approved() and reservation.is_driver_approved()
    
    reservation_details = Div(
        H3("รายละเอียดการจอง"),
        P("Reservation ID: " + reservation.get_id()),
        P("Renter: " + reservation.get_renter().get_username()),
        P("วันที่เริ่มเช่า: " + start_date),
        P("วันที่สิ้นสุดเช่า: " + end_date),
        P("ราคารถ: " + str(reservation.get_price())),
        P("โปรโมชั่น: " + promotion_info),
        P("สถานะอนุมัติจาก Admin: " + admin_status),
        P("สถานะอนุมัติจาก Driver: " + driver_status)
    )
    
    if can_pay:
        promo_button = Button(
            "ใส่รหัสโปรโมชั่น", type="button",
            onclick="window.location.href='/reservation/promotion?reservation_id=" + reservation.get_id() + "'"
        )
    else:
        promo_button = Button(
            "รอการอนุมัติจาก Admin และ Driver", type="button",
            disabled="disabled"
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
            button {
                background: #0052d4;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
                margin: 10px;
            }
            button:disabled {
                background: #ccc;
                cursor: not-allowed;
            }
            button:hover:enabled {
                background: #003bb5;
            }
        """),
        Div(
            reservation_details,
            P("โปรดจดจำ Reservation ID: " + reservation.get_id()),
            promo_button,
            _class="message"
        )
    )

# Endpoint สำหรับกรอกรหัสโปรโมชั่น
@rt('/reservation/promotion', methods=["GET", "POST"])
def reservation_promotion(reservation_id: str, promotion_code: str = ""):
    target = None
    for res in company.get_reservations():
        if res.get_id() == reservation_id:
            target = res
            break
    if target is None:
        return Container(
            Style(THEME_STYLE + "body { padding: 20px; }"),
            H1("ไม่พบ Reservation")
        )
    
    if not (target.is_admin_approved() and target.is_driver_approved()):
        return Container(
            Style(THEME_STYLE + "body { padding: 20px; }"),
            H1("ยังไม่ผ่านการอนุมัติทั้งหมด")
        )
    
    if promotion_code == "":
        return Container(
            Style(THEME_STYLE + """
                body { padding: 20px; }
                .form-container {
                    max-width: 500px;
                    margin: 40px auto;
                    background: #FFF;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
                }
                label { display: block; margin-top: 10px; font-weight: bold; }
                input { width: 100%; padding: 8px; margin-top: 5px; }
                button {
                    margin-top: 20px;
                    background: #0052d4;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 5px;
                    cursor: pointer;
                }
                button:hover { background: #003bb5; }
            """),
            Div(
                H2("กรอกรหัสโปรโมชั่น"),
                Form(
                    Input(name="reservation_id", value=reservation_id, type="hidden"),
                    Label("รหัสโปรโมชั่น:"),
                    Input(name="promotion_code", type="text", placeholder="ระบุรหัสโปรโมชั่น"),
                    Button("ยืนยัน", type="submit"),
                    action="/reservation/promotion", method="POST"
                ),
                _class="form-container"
            )
        )
    else:
        for promo in company.get_promotions():
            if promo.check_promotion(promotion_code):
                target.apply_promotion(promo)
                break
        return RedirectResponse("/payment?reservation_id=" + reservation_id, status_code=302)

# Endpoint สำหรับอนุมัติ Reservation โดย Admin
@rt('/reservation/approve/admin', methods=["GET"])
def approve_reservation_admin(reservation_id: str):
    for res in company.get_reservations():
        if res.get_id() == reservation_id:
            res.approve_admin()
            return Container(
                Style(THEME_STYLE + "body { padding: 20px; }"),
                H1("อนุมัติการจอง (Admin) สำเร็จ"),
                P("Reservation ID: " + reservation_id)
            )
    return Container(
        Style(THEME_STYLE + "body { padding: 20px; }"),
        H1("ไม่พบ Reservation ที่ต้องการอนุมัติ")
    )

# Endpoint สำหรับอนุมัติ Reservation โดย Driver
@rt('/reservation/approve/driver', methods=["GET"])
def approve_reservation_driver(reservation_id: str):
    for res in company.get_reservations():
        if res.get_id() == reservation_id:
            res.approve_driver()
            return Container(
                Style(THEME_STYLE + "body { padding: 20px; }"),
                H1("อนุมัติการจอง (Driver) สำเร็จ"),
                P("Reservation ID: " + reservation_id)
            )
    return Container(
        Style(THEME_STYLE + "body { padding: 20px; }"),
        H1("ไม่พบ Reservation ที่ต้องการอนุมัติ")
    )

# Endpoint สำหรับตรวจสอบสถานะของ Reservation
@rt('/reservation/status', methods=["GET"])
def reservation_status(reservation_id: str):
    for res in company.get_reservations():
        if res.get_id() == reservation_id:
            admin_status = "Approved" if res.is_admin_approved() else "ยังไม่อนุมัติ"
            driver_status = "Approved" if res.is_driver_approved() else "ยังไม่อนุมัติ"
            return Container(
                Style(THEME_STYLE + "body { padding: 20px; }"),
                H2("สถานะการจอง"),
                P("Reservation ID: " + reservation_id),
                P("สถานะอนุมัติจาก Admin: " + admin_status),
                P("สถานะอนุมัติจาก Driver: " + driver_status)
            )
    return Container(
        Style(THEME_STYLE + "body { padding: 20px; }"),
        H1("ไม่พบข้อมูล Reservation")
    )

serve()
