from fasthtml.common import *
from routing import app, rt
import BackEnd, time
import datetime 

company = BackEnd.company

THEME_STYLE = """
html, body {
    height: 100%;
    font-family: 'Roboto', sans-serif;
    margin: 0;
    padding: 0;
    background: linear-gradient(135deg, #2196F3, #21CBF3);
    background-size: cover;
}
"""

@rt('/reservation/form', methods=["GET"])
def reservation_form(car_id: str = "", start_date: str = "", end_date: str = ""):
    return Container(
        Style(THEME_STYLE + """
            body { padding: 20px; }
            .form-container {
                max-width: 500px;
                margin: 100px auto 20px auto;
                background: rgba(255,255,255,0.95);
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            }
            label { display: block; margin-top: 10px; font-weight: bold; }
            input {
                width: 100%;
                padding: 8px;
                margin-top: 5px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            button {
                margin-top: 20px;
                background: linear-gradient(45deg, #2196F3, #21CBF3);
                color: #fff;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
                transition: background 0.3s;
            }
            button:hover { background: linear-gradient(45deg, #1976D2, #1E88E5); }
            .header {
                width: 100%;
                background: rgba(0,0,0,0.6);
                padding: 10px 20px;
                position: fixed;
                top: 0;
                left: 0;
                z-index: 1000;
                text-align: center;
                box-shadow: 0 2px 8px rgba(0,0,0,0.5);
            }
            .header h2 {
                color: #fff;
                margin: 0;
                font-size: 42px;
                letter-spacing: 2px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
            }
            .header img {
                width: 70px;
                height: auto;
                margin-right: 10px;
            }
        """),
        
        Div(
            Div(
                Img(src="/static/images/logo.png", alt="Drivy Logo", style="width: 70px; height: auto; margin-right: 10px;"),
                H2("DRIVY", style="margin: 0;"),
                style="display: flex; align-items: center;",
                _class="header"
            ),
            Div(
                H2("จองรถ", style="text-align: center;"),
                Form(
                    Input(name="car_id", value=car_id, type="hidden"),
                    Input(name="start_date", type="hidden", value=start_date),
                    P("วันที่เริ่มเช่า: " + start_date, style="font-size:18px;"),
                    Input(name="end_date", type="hidden", value=end_date),
                    P("วันที่สิ้นสุดเช่า: " + end_date, style="font-size:18px;"),
                    Label("รหัสโปรโมชั่น (ถ้ามี):"),
                    Input(name="promotion_code", type="text", placeholder="ระบุรหัสโปรโมชั่น"),
                    Label("ต้องการประกันรถหรือไม่:"),
                    Select(
                        Option("No", value="No"),
                        Option("Yes", value="Yes"),
                        name="insurance_option",
                        required=True
                    ),
                    Label("ต้องการคนขับหรือไม่:"),
                    Select(
                        Option("No", value="No"),
                        Option("Yes", value="Yes"),
                        name="driver_option",
                        required=True
                    ),
                    Button("จองรถ", type="submit"),
                    action="/reservation", method="POST"
                ),
                _class="form-container"
            )
        )
    )

@rt('/reservation', methods=["POST"])
def save_reservation(car_id: str, start_date: str, end_date: str,
                     promotion_code: str = "", insurance_option: str = "No", driver_option: str = "No"):
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
    
    renter = BackEnd.User(3001, "user1", "pass1", "renter", "U-111")
    
    # แปลงวันที่และคำนวณจำนวนวันที่เช่า
    try:
        start_dt = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    except Exception as e:
        return Container(
            Style(THEME_STYLE + "body { padding: 20px; }"),
            H1("รูปแบบวันที่ไม่ถูกต้อง")
        )
    
    days = (end_dt - start_dt).days
    if days <= 0:
        return Container(
            Style(THEME_STYLE + "body { padding: 20px; }"),
            H1("วันที่เริ่มเช่าต้องน้อยกว่าวันที่สิ้นสุดเช่า")
        )
    
    # คำนวณราคาเบื้องต้น = ราคา base * จำนวนวัน
    base_price = selected_car.get_price()
    price = base_price * days

    promotion_instance = None
    promotion_info = "ไม่มีโปรโมชั่น"
    discount_percent = 0
    promo_code = promotion_code.strip().upper()
    if promo_code == "ABC":
        discount_percent = 10
    elif promo_code == "DEF":
        discount_percent = 20
    elif promo_code == "GHI":
        discount_percent = 50
    if discount_percent > 0:
        discount = price * (discount_percent / 100)
        price = price - discount
        promotion_info = f"ลด {discount_percent}%"

    # กำหนดประกันรถ (ถ้าเลือก Yes)
    insurance_instance = None
    if insurance_option == "Yes":
        # ตัวอย่าง: เบี้ยประกัน 200 ต่อการจอง (ไม่คูณวัน)
        insurance_instance = BackEnd.Insurance("I1", "Basic Insurance", "Standard coverage", 200)
        price += insurance_instance.get_price()
    
    # กำหนดคนขับ (ถ้าเลือก Yes)
    driver_assigned = None
    if driver_option == "Yes":
        for user in company.get_users():
            if user.get_role() == "driver":
                driver_assigned = user
                break
    
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

# ตรวจสอบสถานะ Reservation (ตรวจสอบเฉพาะ admin approval)
@rt('/reservation/status', methods=["GET"])
def reservation_status(reservation_id: str):
    for res in company.get_reservations():
        if res.get_id() == reservation_id:
            # หากไม่มี driver ถูกกำหนด (หมายความว่าไม่ได้ต้องการ driver)
            driver_approved = res.get_driver() is None or res.is_driver_approved()
            if res.is_admin_approved() and driver_approved:
                if not res.is_paid():
                    return RedirectResponse("/payment?reservation_id=" + reservation_id, status_code=302)
                else:
                    return Container(
                        Style(THEME_STYLE + "body { padding: 20px; }"),
                        H2("จองสำเร็จ", style="color: green;"),
                        P("Reservation ID: " + reservation_id)
                    )
            else:
                admin_status = "Approved" if res.is_admin_approved() else "ยังไม่อนุมัติ"
                # แสดงข้อความว่า driver ไม่จำเป็นถ้าไม่มีการกำหนด driver
                driver_status = "Not required" if res.get_driver() is None else ("Approved" if res.is_driver_approved() else "ยังไม่อนุมัติ")
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