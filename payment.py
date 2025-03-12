from fasthtml.common import *
from routing import app, rt
import BackEnd
company = BackEnd.company

@rt('/payment')
def payment_page():
    # สร้าง instance ของ Payment แบบ static สำหรับตัวอย่าง
    payment_instance = BackEnd.Payment("Pay1", credit="1234567890")
    
    # ดึงข้อมูลจาก instance
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
            /* Header ด้านบน */
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
            /* ส่วนเนื้อหาหลัก */
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
            .info {
                font-size: 18px;
                color: #333;
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
        # Header Bar
        Div(
            H2("DRIVY Payment Dashboard", style="color: #fff; margin: 0;"),
            _class="header"
        ),
        # Main Content
        Body(
            Div(
                H3("Payment Details"),
                P("Payment ID: " + payment_id, _class="info"),
                P("Payment Method: " + payment_method, _class="info"),
                Button("Process Payment", type="button"),
                _class="content"
            ),
            style="padding: 20px; min-height: 100vh;"
        )
    )

serve()
