from fasthtml.common import *
from routing import app, rt
import BackEnd

company = BackEnd.company

@rt('/payment', methods=["GET"])
def payment_page(reservation_id: str):
    # สร้าง instance ของ Payment (ในระบบจริงคุณอาจดึงข้อมูลเพิ่มเติมจาก reservation_id)
    payment_instance = BackEnd.Payment("Pay1", credit="1234567890")
    payment_id = payment_instance.get_id()
    payment_method = payment_instance.check_method_payment()
    
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
            h2, h3, p {
                margin: 0 0 15px 0;
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
                P("Payment ID: " + payment_id),
                P("Payment Method: " + payment_method),
                # ฟอร์มชำระเงินส่ง reservation_id ไปด้วย
                Form(
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
def process_payment(reservation_id: str):
    # ที่นี่คุณสามารถเพิ่มโค้ดประมวลผลการชำระเงินหรืออัพเดตสถานะการจองได้
    # หลังจากชำระเงินสำเร็จ Redirect ไปที่หน้า search (ประวัติการเช่า)
    return RedirectResponse("/search", status_code=302)

serve()
