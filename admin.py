from fasthtml.common import *
from routing import app, rt
import BackEnd, time
company = BackEnd.company

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
            # สร้าง Reservation id โดยใช้ timestamp ให้ unique
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
                        Button("Approve", type="button", onclick=f"window.location.href='{approve_link}'"),
                        Button("Reject", type="button", onclick=f"window.location.href='{reject_link}'"),
                        Style("display: flex; gap: 10px;")
                    ),
                    Style("border: 1px solid #ddd; padding: 10px; margin-bottom: 10px;")
                )
            )
    else:
        reservation_list.append(P("ไม่มีรายการจองที่รอการอนุมัติ"))
    
    return Container(
        Style("""
            body { font-family: Arial, sans-serif; background: #AEEEEE; padding: 20px; }
            .header { width: 100%; background: #4682B4; padding: 25px; text-align: center; }
            .content { max-width: 800px; margin: 80px auto; background: #fff; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.2); }
        """),
        Div(
            H2("DRIVY Admin Dashboard", style="color: #fff; margin: 0;"),
            _class="header"
        ),
        Div(
            H3("Welcome, " + admin_instance.get_username()),
            P(payment_msg),
            P("นี่คือรายการจองที่รอการอนุมัติจาก Admin:"),
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
                Style("body { font-family: Arial; background: #F5F5F5; padding: 20px; }"),
                H1("อนุมัติการจอง (Admin) สำเร็จ"),
                P("Reservation ID: " + reservation_id)
            )
    return Container(
        Style("body { font-family: Arial; background: #F5F5F5; padding: 20px; }"),
        H1("ไม่พบ Reservation ที่ต้องการอนุมัติ")
    )

@rt('/reservation/reject/admin', methods=["GET"])
def reject_reservation_admin(reservation_id: str):
    reservations = company.get_reservations()
    for i, res in enumerate(reservations):
        if res.get_id() == reservation_id:
            del reservations[i]
            return Container(
                Style("body { font-family: Arial; background: #F5F5F5; padding: 20px; }"),
                H1("Reject Reservation สำเร็จ"),
                P("Reservation ID: " + reservation_id)
            )
    return Container(
        Style("body { font-family: Arial; background: #F5F5F5; padding: 20px; }"),
        H1("ไม่พบ Reservation ที่ต้องการ Reject")
    )

serve()
