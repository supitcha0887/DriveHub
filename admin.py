from fasthtml.common import *
from routing import app, rt
import BackEnd, time
company = BackEnd.company

# ตัวแปรสำหรับสไตล์พื้นฐาน (Theme)
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

@rt('/admin', methods=["GET"])
def admin_dashboard():
    # สร้าง instance ของ Admin และ Payment
    admin_instance = BackEnd.Admin(1001, "admin1", "pass1", "admin")
    payment_instance = BackEnd.Payment("Pay1", credit="1234567890")
    payment_msg = admin_instance.accept_payment(payment_instance)
    
    # สำหรับทดสอบ: หากไม่มี Reservation ในระบบ ให้สร้าง dummy reservation
    if not company.get_reservations():
        dummy_renter = BackEnd.User(3001, "user1", "pass1", "renter", "U-111")
        cars = company.get_cars()
        if cars:
            dummy_car = cars[0]
            reservation_id = "R" + dummy_car.get_id() + "_" + str(int(time.time()))
            dummy_reservation = BackEnd.Reservation(
                reservation_id,
                dummy_renter,
                dummy_car,
                "2025-03-12",
                "2025-03-13",
                dummy_car.get_price()
            )
            company.add_reservation(dummy_reservation)
    
    # ดึงรายการ Reservation ที่ยังไม่ได้อนุมัติโดย Admin
    pending_reservations = [res for res in company.get_reservations() if not res.is_admin_approved()]
    
    reservation_list = []
    if pending_reservations:
        for res in pending_reservations:
            approve_link = "/reservation/approve/admin?reservation_id=" + res.get_id()
            reject_link = "/reservation/reject/admin?reservation_id=" + res.get_id()
            reservation_list.append(
                Div(
                    P("Reservation ID: " + res.get_id()),
                    P("Renter: " + res.get_renter().get_username()),
                    P("Car Model: " + res.get_car().get_model()),
                    P("Start Date: " + res.get_start_date()),
                    P("End Date: " + res.get_end_date()),
                    Div(
                        Button("Approve", type="button", onclick=f"window.location.href='{approve_link}'", _class="select-btn"),
                        Button("Reject", type="button", onclick=f"window.location.href='{reject_link}'", _class="select-btn"),
                        _style="display: flex; gap: 20px;"
                    ),
                    Style("background: #fff; border: 1px solid #ddd; padding: 10px; margin-bottom: 10px; border-radius: 10px;")
                )
            )
    else:
        reservation_list.append(P("ไม่มีรายการจองที่รอการอนุมัติ", style="color: #fff; text-align: center;"))
    
    return Container(
        Style(THEME_STYLE + """
            body { padding: 20px; }
            .header {
                width: 100%;
                background: rgba(0,0,0,0.5);
                padding: 25px;
                text-align: center;
                border-bottom: 2px solid rgba(0,0,0,0.3);
            }
            .header h2 {
                color: #fff;
                margin: 0;
                font-size: 42px;
                letter-spacing: 2px;
            }
            .content {
                max-width: 800px;
                margin: 80px auto;
                background: #fff;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.2);
            }
            p { font-size: 18px; margin-bottom: 10px; }
            h3 { margin-bottom: 15px; }
            /* สไตล์ปุ่มแบบเดียวกับหน้า Driver */
            .select-btn {
                background: #0052d4;
                color: #fff;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
                transition: background 0.3s;
            }
            .select-btn:hover {
                background: #003bb5;
            }
        """),
        Div(
            H2("DRIVY Admin Dashboard", style="color: #fff; margin: 0;"),
            _class="header"
        ),
        Div(
            H3("Welcome, " + admin_instance.get_username()),
            P(payment_msg, style="color: #333;"),
            P("นี่คือรายการจองที่รอการอนุมัติจาก Admin:", style="color: #333;"),
            *reservation_list,
            _class="content"
        )
    )

@rt('/reservation/approve/admin', methods=["GET"])
def approve_reservation_admin(reservation_id: str):
    for res in company.get_reservations():
        if res.get_id() == reservation_id:
            res.approve_admin()
            return Container(
                Style(THEME_STYLE + "body { padding: 20px; }"),
                H1("อนุมัติการจอง (Admin) สำเร็จ", style="color: #fff;"),
                P("Reservation ID: " + reservation_id, style="color: #fff;")
            )
    return Container(
        Style(THEME_STYLE + "body { padding: 20px; }"),
        H1("ไม่พบ Reservation ที่ต้องการอนุมัติ", style="color: #fff;")
    )

@rt('/reservation/reject/admin', methods=["GET"])
def reject_reservation_admin(reservation_id: str):
    reservations = company.get_reservations()
    for i, res in enumerate(reservations):
        if res.get_id() == reservation_id:
            del reservations[i]
            return Container(
                Style(THEME_STYLE + "body { padding: 20px; }"),
                H1("Reject Reservation สำเร็จ", style="color: #fff;"),
                P("Reservation ID: " + reservation_id, style="color: #fff;")
            )
    return Container(
        Style(THEME_STYLE + "body { padding: 20px; }"),
        H1("ไม่พบ Reservation ที่ต้องการ Reject", style="color: #fff;")
    )

serve()
