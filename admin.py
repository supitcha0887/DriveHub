from fasthtml.common import *
from routing import app, rt
import BackEnd
company = BackEnd.company

@rt('/admin')
def admin_dashboard():
    admin_instance = BackEnd.Admin(1001, "admin1", "pass1", "admin")
    payment_instance = BackEnd.Payment("Pay1", credit="1234567890")
    
    # ดึงรายการ Reservation ที่ยังไม่ได้อนุมัติโดย Admin
    pending_reservations = [res for res in company.get_reservations() if not res.is_admin_approved()]
    
    reservation_list = Div()
    if pending_reservations:
        for res in pending_reservations:
            # สร้างปุ่มสำหรับอนุมัติแต่ละรายการ
            approve_link = "/reservation/approve/admin?reservation_id=" + res.get_id()
            reservation_list += Div(
                P("Reservation ID: " + res.get_id()),
                P("Renter: " + res.get_renter().get_username()),
                P("Car Model: " + res.get_car().get_model()),
                P("Start Date: " + res.get_start_date()),
                P("End Date: " + res.get_end_date()),
                Button("Approve", type="button", onclick="window.location.href='" + approve_link + "'"),
                Style("border: 1px solid #ddd; padding: 10px; margin-bottom: 10px;")
            )
    else:
        reservation_list = P("ไม่มีรายการจองที่รอการอนุมัติ")
    
    return Container(
        Style("""
            body { font-family: Arial, sans-serif; background: #AEEEEE; padding: 20px; }
            .header { width: 100%; background: #4682B4; padding: 25px; border-bottom: 2px solid #000; text-align: center; }
            .content { max-width: 800px; margin: 80px auto; background: #fff; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.2); }
        """),
        Div(
            H2("DRIVY Admin Dashboard", style="color: #fff; margin: 0;"),
            _class="header"
        ),
        Div(
            H3("Welcome, " + admin_instance.get_username()),
            P("นี่คือรายการจองที่รอการอนุมัติจาก Admin:"),
            reservation_list,
            _class="content"
        )
    )

serve()
