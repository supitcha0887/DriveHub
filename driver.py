from fasthtml.common import *
from routing import app, rt
import BackEnd

company = BackEnd.company

THEME_STYLE = """
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
* { box-sizing: border-box; }
html, body {
    height: 100%;
    margin: 0;
    padding: 0;
    font-family: 'Roboto', sans-serif;
    background: linear-gradient(135deg, #bbdefb, #e3f2fd);
    background-size: cover;
}
.header {
    width: 100%;
    background: #e3f2fd;
    padding: 25px;
    position: fixed;
    top: 0;
    left: 0;
    z-index: 1000;
    text-align: center;
    border-bottom: 2px solid #90caf9;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
.header h2 {
    color: #0d47a1;
    margin: 0;
    font-size: 42px;
    letter-spacing: 2px;
}
.content {
    max-width: 800px;
    margin: 120px auto;
    background: rgba(255,255,255,0.95);
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}
.card {
    background: #fff;
    border-radius: 10px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}
.card:hover {
    transform: scale(1.03);
    box-shadow: 0 8px 16px rgba(0,0,0,0.2);
}
.select-btn {
    background: linear-gradient(45deg, #0052d4, #4364f7);
    color: #fff;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    cursor: pointer;
    transition: background 0.3s;
    margin-top: 10px;
}
.select-btn:hover {
    background: linear-gradient(45deg, #003bb5, #345ecb);
    transform: translateY(-2px);
}
"""

@rt('/driver', methods=["GET"])
def driver_dashboard():
    pending_reservations = [res for res in company.get_reservations() if not res.is_driver_approved()]
    reservation_list = []
    if pending_reservations:
        for res in pending_reservations:
            approve_link = "/reservation/approve/driver?reservation_id=" + res.get_id()
            reservation_list.append(
                Div(
                    P("Reservation ID: " + res.get_id(), style="font-size:18px;"),
                    P("Car Model: " + res.get_car().get_model(), style="font-size:18px;"),
                    P("Start Date: " + res.get_start_date(), style="font-size:18px;"),
                    P("End Date: " + res.get_end_date(), style="font-size:18px;"),
                    Button("Approve", type="button", onclick=f"window.location.href='{approve_link}'", _class="select-btn"),
                    Style("background: #fff; border: 1px solid #ddd; padding: 15px; margin-bottom: 15px; border-radius: 10px;")
                )
            )
    else:
        reservation_list.append(P("No pending reservations", style="color: black; text-align: center; font-size:20px;"))
    
    return Container(
        Style(THEME_STYLE + """
body { padding: 20px; }
.header {
    width: 100%;
    background: linear-gradient(135deg, #bbdefb, #e3f2fd);
    padding: 25px;
    text-align: center;
    border-bottom: 2px solid #90caf9;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
.header h2 {
    color: #0d47a1;
    margin: 0;
    font-size: 42px;
    letter-spacing: 2px;
}
.content {
    max-width: 800px;
    margin: 80px auto;
    background: rgba(255,255,255,0.95);
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}
.select-btn {
    background: linear-gradient(45deg, #2196F3, #21CBF3);
    color: #fff;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    cursor: pointer;
    transition: background 0.3s;
}
.select-btn:hover {
    background: linear-gradient(45deg, #1976D2, #1E88E5);
}
"""),
        Div(
            H2("DRIVY Driver ", style="color: #0d47a1; margin: 0;"),
            _class="header"
        ),
        Div(
            H3("Welcome, " , style="color: #333;"),
            P("Pending reservations for driver:", style="font-weight:bold;"),
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
                H1("Driver approval successful", style="color: #fff;"),
                P("Reservation ID: " + reservation_id, style="color: #fff;")
            )
    return Container(
        Style(THEME_STYLE + "body { padding: 20px; }"),
        H1("Reservation not found", style="color: #fff;")
    )

serve()
