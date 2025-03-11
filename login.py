from fasthtml.common import *
from routing import app, rt
import BackEnd
from BackEnd import Admin
from BackEnd import User
from BackEnd import Driver
company = BackEnd.company

@rt('/')
def get(success_message=None, error_message=None):
    return Title("DRIVY"), Container(
        Style(""" 
            .tab-btn { 
                color: #1C1C3B; 
                font-size: 18px; 
                font-weight: bold; 
                background: transparent; 
                border: none;
                outline: none; 
                padding: 10px 20px; 
                cursor: pointer; 
                transition: background 0.3s;
            }
            .tab-btn:hover { background: #D3D3D3; }
            .tab-btn.active { border-bottom: 2px solid #1C1C3B; }
            .form-section { 
                display: none; 
                background: #fff; 
                padding: 20px; 
                border-radius: 10px; 
                border: 1px solid #1C1C3B; 
                box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.2); 
                margin-top: 20px;
                transition: opacity 0.5s ease;
            }
            .form-section.active { display: block; opacity: 1; }
            .success-message {
                color: green;
                font-size: 20px;
                text-align: center;
                margin-top: 20px;
            }
            .error-message {
                color: red;
                font-size: 20px;
                text-align: center;
                margin-top: 20px;
            }
        """),
        Div(
            Div(H2("DRIVY", style="color: #B0E0E6; margin: 0;")),
            style="width: 100%; background: #4682B4; padding: 25px; border-bottom: 2px solid #502314; position: fixed; top: 0; left: 0; z-index: 1000;"
        ),
        Body(
            Div(
                H3("LOGIN / REGISTER", style="font-size: 36px; text-align: center; color: #1C1C3B;"),
                Div(
                    Button("Login", type="button", id="loginBtn", _class="tab-btn active"),
                    Button("Register", type="button", id="registerBtn", _class="tab-btn"),
                    style="text-align: center; margin-bottom: 10px;"
                ),
                # แสดงข้อความสำเร็จหรือผิดพลาด ถ้ามี
                success_message and Div(H3(success_message, _class="success-message")),
                error_message and Div(H3(error_message, _class="error-message")),
                # ฟอร์มสำหรับ Login
                Form(
                    Div(
                        Div(Label("Username"), Input(type="text", id="login_username", name="login_username", required=True)),
                        Div(Label("Password"), Input(type="password", id="login_password", name="login_password", required=True))
                    ),
                    Button("LOG IN", type="submit"),
                    method="POST",  # ต้องใช้ POST
                    action="/login",
                    style="background: #AEEEEE; padding: 20px; min-height: 100vh; margin-top: 80px;",
                    id="login-section",
                    _class="form-section active"
                ),

                # ฟอร์มสำหรับ Register
                Form(
                    Div(
                        Div(Label("Username"), Input(type="text", id="register_username", name="register_username", required=True)),
                        Div(Label("Password"), Input(type="password", id="register_password", name="register_password", required=True)),
                        Div(
                            Label(Input(type="radio", name="register_role", value="driver", required=True, checked=True), "driver"),
                            Label(Input(type="radio", name="register_role", value="renter", required=True), "renter")
                        )
                    ),
                    Button("REGISTER", type="submit"),
                    method="POST",  # ต้องใช้ POST
                    action="/register",
                    style="background: #AEEEEE; padding: 20px; min-height: 100vh; margin-top: 80px;",
                    id="register-section",
                    _class="form-section"
                ),

                Script("""
                    // เมื่อกดปุ่ม Login ให้แสดงแบบฟอร์ม Login
                    document.getElementById('loginBtn').addEventListener('click', function() {
                        document.getElementById('loginBtn').classList.add('active');
                        document.getElementById('registerBtn').classList.remove('active');
                        document.getElementById('login-section').classList.add('active');
                        document.getElementById('register-section').classList.remove('active');
                    });
                    // เมื่อกดปุ่ม Register ให้แสดงแบบฟอร์ม Register
                    document.getElementById('registerBtn').addEventListener('click', function() {
                        document.getElementById('registerBtn').classList.add('active');
                        document.getElementById('loginBtn').classList.remove('active');
                        document.getElementById('register-section').classList.add('active');
                        document.getElementById('login-section').classList.remove('active');
                    });
                """)
            )
        )
    )

@rt('/register', methods=["POST"])
def register(register_username, register_password, register_role):

    print("DEBUG: register_username:", register_username)
    print("DEBUG: register_password:", register_password)
    print("DEBUG: role:", register_role)

    if not (register_username and register_password and register_role):
        return get(error_message="กรุณากรอกข้อมูลให้ครบถ้วนสำหรับการสมัครสมาชิก")
    
    username = register_username.strip()
    password = register_password.strip()
    user_role = register_role.strip()
    
    success, msg = company.register(username, password, user_role)
    if success:
        return get(success_message="การสมัครสมาชิกสำเร็จ กรุณาเข้าสู่ระบบ")
    else:
        return get(error_message=f"การสมัครสมาชิกล้มเหลว: {msg}")




@rt('/login', methods=["POST"])
def login(login_username: str, login_password: str):
    username = login_username.strip()
    password = login_password.strip()
    
    if not username or not password:
        return get(error_message="กรุณากรอกข้อมูลให้ครบถ้วนในการเข้าสู่ระบบ")
    
    # ฟังก์ชัน login จะคืนค่าเป็น role (string) ถ้าหาก login สำเร็จ
    role = company.login(username, password)
    
    if role in ["user", "renter"]:
        return RedirectResponse("/search" , status_code=302)
    elif role == "driver":
        return RedirectResponse("/driver")
    elif role == "admin":
        return RedirectResponse("/admin")
    else:
        return get(error_message="ข้อมูลเข้าสู่ระบบผิดพลาด กรุณาลองใหม่อีกครั้ง")


# เริ่มต้นเซิร์ฟเวอร์
serve()
