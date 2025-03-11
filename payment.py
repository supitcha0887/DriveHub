from fasthtml.common import *
from routing import app
from routing import rt
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
            body {
                font-family: Arial, sans-serif;
                background: #AEEEEE; /* พื้นหลังสีฟ้าเหมือนหน้า login */
                padding: 20px;
            }
            .header {
                width: 100%;
                background: #4682B4; /* สีฟ้าเข้ม */
                padding: 25px;
                border-bottom: 2px solid #000; /* เส้นขอบด้านล่างเป็นสีดำ */
                text-align: center;
            }
            .content {
                max-width: 600px;
                margin: 80px auto;
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
                background: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
            }
            button:hover {
                background: #45a049;
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
            style="background: #AEEEEE; padding: 20px; min-height: 100vh;"
        )
    )

serve()
