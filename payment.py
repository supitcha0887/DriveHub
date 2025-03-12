from fasthtml.common import *
from routing import app, rt
import BackEnd

company = BackEnd.company

@rt('/payment', methods=["GET"])
def payment_page(reservation_id: str):
    # ค้นหา Reservation ที่ตรงกับ reservation_id
    reservation = None
    for res in company.get_reservations():
        if res.get_id() == reservation_id:
            reservation = res
            break

    if reservation:
        insurance_cost = reservation.get_insurance().get_price() if reservation.get_insurance() else 0
        total_cost = reservation.get_price()  # ราคาที่คำนวณแล้วรวมส่วนลดและเบี้ยประกัน
    else:
        insurance_cost = 0
        total_cost = 0

    return Container(
        Style("""
            html, body {
                height: 100%;
                font-family: 'Roboto', sans-serif;
                margin: 0;
                padding: 0;
                background: linear-gradient(135deg, #2196F3, #21CBF3);
                background-size: cover;
            }
            .header {
                width: 100%;
                background: rgba(0,0,0,0.5);
                padding: 25px;
                border-bottom: 2px solid rgba(0,0,0,0.3);
                text-align: center;
                box-shadow: 0 2px 8px rgba(0,0,0,0.5);
            }
            .header h2 {
                color: #fff;
                margin: 0;
                font-size: 42px;
                letter-spacing: 2px;
            }
            .content {
                max-width: 600px;
                margin: 0 auto;  /* ลบ margin-top ที่เป็น 100px ออก */
                background: rgba(255,255,255,0.95);
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            }
            label { font-weight: bold; }
            .payment-option { margin-bottom: 10px; }
            button {
                background: linear-gradient(45deg, #2196F3, #21CBF3);
                color: #fff;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
                transition: background 0.3s;
            }
            button:hover {
                background: linear-gradient(45deg, #1976D2, #1E88E5);
            }
        """),
        Div(
            Img(src="/static/images/logo.png", alt="Drivy Logo", style="width: 70px; height: auto; margin-right: 10px;"),
            H2("DRIVY Payment Dashboard", style="color: #fff; margin: 0;"),
            style="display: flex; align-items: center;",
            _class="header"
        ),
        Body(
            Div(
                H3("Payment Details", style="margin-bottom:15px;"),
                P("Reservation ID: " + reservation_id, style="font-size:18px;"),
                P("Insurance Cost: $" + str(insurance_cost), style="font-size:18px;"),
                P("Total Cost: $" + str(total_cost), style="font-size:18px; font-weight:bold;"),
                Form(
                    Div(
                        Label("เลือกวิธีการชำระเงิน:"), 
                        Div(
                            Input(type="radio", name="payment_method", value="qrcode", required=True, _class="payment-option"),
                            Label("ชำระผ่านคิวอาร์โค้ด")
                        ),
                        Div(
                            Input(type="radio", name="payment_method", value="cash", required=True, _class="payment-option"),
                            Label("ชำระเงินสด")
                        )
                    ),
                    Input(type="hidden", name="reservation_id", value=reservation_id),
                    Button("ชำระเงิน", type="submit"),
                    action="/payment/process", method="POST"
                ),
                _class="content"
            ),
            style="padding: 20px; min-height: 100vh;"
        )
    )

@rt('/payment/process', methods=["POST"])
def process_payment(reservation_id: str, payment_method: str):
    if payment_method == "qrcode":
         payment_instance = BackEnd.Payment("Pay" + reservation_id, qrcode="QRCodeData")
    elif payment_method == "cash":
         payment_instance = BackEnd.Payment("Pay" + reservation_id, credit="Cash")
    else:
         payment_instance = BackEnd.Payment("Pay" + reservation_id)
    
    company.add_payment(payment_instance)
    
    for res in company.get_reservations():
         if res.get_id() == reservation_id:
              res.mark_paid()
              break
    return RedirectResponse("/reservation/status?reservation_id=" + reservation_id, status_code=302)

serve()