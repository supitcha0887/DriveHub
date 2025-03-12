from fasthtml.common import *
from routing import app, rt
import BackEnd

company = BackEnd.company

@rt('/payment', methods=["GET"])
def payment_page(reservation_id: str):
    return Container(
        Style("""
            html, body {
                height: 100%;
                font-family: 'Roboto', sans-serif;
                margin: 0;
                padding: 0;
                background: linear-gradient(135deg, #0052d4, #4364f7, #6fb1fc);
                background-size: cover;
            }
            .header {
                width: 100%;
                background: rgba(0,0,0,0.5);
                padding: 25px;
                border-bottom: 2px solid rgba(0,0,0,0.3);
                text-align: center;
            }
            .header h2 {
                color: #fff;
                margin: 0;
                font-size: 42px;
                letter-spacing: 2px;
            }
            .content {
                max-width: 600px;
                margin: 100px auto 40px auto;
                background: #fff;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.2);
            }
            label {
                font-weight: bold;
            }
            .payment-option {
                margin-bottom: 10px;
            }
            button {
                background: #0052d4;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
                transition: background 0.3s;
            }
            button:hover {
                background: #003bb5;
            }
        """),
        Div(
            H2("DRIVY Payment Dashboard", style="color: #fff; margin: 0;"),
            _class="header"
        ),
        Body(
            Div(
                H3("Payment Details"),
                P("Reservation ID: " + reservation_id),
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
    # สร้าง Payment instance ตามวิธีการชำระเงินที่เลือก
    if payment_method == "qrcode":
         payment_instance = BackEnd.Payment("Pay" + reservation_id, qrcode="QRCodeData")
    elif payment_method == "cash":
         payment_instance = BackEnd.Payment("Pay" + reservation_id, credit="Cash")
    else:
         payment_instance = BackEnd.Payment("Pay" + reservation_id)
    
    company.add_payment(payment_instance)
    
    # ทำเครื่องหมาย Reservation ว่าชำระเงินแล้ว
    for res in company.get_reservations():
         if res.get_id() == reservation_id:
              res.mark_paid()
              break
    # หลังจากชำระเงินแล้ว Redirect ไปที่หน้า status เพื่อแสดงสถานะการอนุมัติ
    return RedirectResponse("/reservation/status?reservation_id=" + reservation_id, status_code=302)

serve()
