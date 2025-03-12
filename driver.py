from fasthtml.common import *
from routing import app, rt
import BackEnd
company = BackEnd.company

@rt('/driver', methods=["GET"])
def driver_dashboard():
    driver_instance = BackEnd.Driver(2001, "driver1", "pass1", "driver", "L-123")
    
    # ดึงรายการ Reservation ที่ยังไม่ได้อนุมัติโดย Driver
    pending_reservations = [res for res in company.get_reservations() if not res.is_driver_approved()]
    
    reservation_list = []
    if pending_reservations:
        for res in pending_reservations:
            approve_link = "/reservation/approve/driver?reservation_id=" + res.get_id()
            reservation_list.append(
                Div(
                    P("Reservation ID: " + res.get_id()),
                    P("Renter: " + res.get_renter().get_username()),
                    P("Car Model: " + res.get_car().get_model()),
                    P("Start Date: " + res.get_start_date()),
                    P("End Date: " + res.get_end_date()),
                    Button("Approve", type="button", onclick=f"window.location.href='{approve_link}'"),
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
            H2("DRIVY Driver Dashboard", style="color: #fff; margin: 0;"),
            _class="header"
        ),
        Div(
            H3("Welcome, " + driver_instance.get_username()),
            P("นี่คือรายการจองที่รอการอนุมัติจาก Driver:"),
            *reservation_list,
            _class="content"
        )
    )

@rt('/reservation/approve/driver', methods=["GET"])
def approve_reservation_driver(reservation_id: str):
    for res in company.get_reservations():
        if res.get_id() == reservation_id:
            res.approve_driver()
            return Container(
                Style("body { font-family: Arial; background: #F5F5F5; padding: 20px; }"),
                H1("อนุมัติการจอง (Driver) สำเร็จ"),
                P("Reservation ID: " + reservation_id)
            )
    return Container(
        Style("body { font-family: Arial; background: #F5F5F5; padding: 20px; }"),
        H1("ไม่พบ Reservation ที่ต้องการอนุมัติ")
    )

serve()
