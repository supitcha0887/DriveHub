from fasthtml.common import *
from routing import app, rt
import BackEnd
company = BackEnd.company

# สไตล์พื้นฐานของธีม
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
                    Button("Approve", type="button", onclick=f"window.location.href='{approve_link}'", 
                           _class="select-btn"),
                    Style("background: #fff; border: 1px solid #ddd; padding: 15px; margin-bottom: 10px; border-radius: 10px;")
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
                Style(THEME_STYLE + "body { padding: 20px; }"),
                H1("อนุมัติการจอง (Driver) สำเร็จ", style="color: #fff;"),
                P("Reservation ID: " + reservation_id, style="color: #fff;")
            )
    return Container(
        Style(THEME_STYLE + "body { padding: 20px; }"),
        H1("ไม่พบ Reservation ที่ต้องการอนุมัติ", style="color: #fff;")
    )

serve()
