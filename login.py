from fasthtml.common import *
from routing import app, rt
import BackEnd
from BackEnd import Admin, User, Driver
company = BackEnd.company

@rt('/')
def get(success_message=None, error_message=None):
    return Title("DRIVY"), Container(
        Style("""
            @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
            * { box-sizing: border-box; }
            html, body {
                height: 100%;
                font-family: 'Roboto', sans-serif;
                margin: 0;
                padding: 0;
                background: linear-gradient(135deg, #2196F3, #21CBF3);
                background-size: cover;
                animation: bgAnimation 8s infinite alternate;
            }
            @keyframes bgAnimation {
                from { filter: brightness(1); }
                to { filter: brightness(1.1); }
            }
            .header {
                width: 100%;
                background: rgba(0,0,0,0.5);
                padding: 20px 40px;
                position: fixed;
                top: 0;
                left: 0;
                z-index: 1000;
                display: flex;
                align-items: center;
                justify-content: center;
                box-shadow: 0 2px 8px rgba(0,0,0,0.5);
            }
            .header h2 {
                color: #fff;
                margin: 0;
                font-size: 42px;
                letter-spacing: 2px;
            }
            .tab-btn {
                color: #fff;
                font-size: 18px;
                font-weight: bold;
                background: transparent;
                border: 2px solid transparent;
                border-radius: 5px;
                outline: none;
                padding: 10px 20px;
                cursor: pointer;
                transition: background 0.3s, border-color 0.3s;
            }
            .tab-btn:hover {
                background: rgba(255,255,255,0.2);
            }
            .tab-btn.active {
                border-color: #fff;
            }
            .form-section {
                display: none;
                background: rgba(255,255,255,0.95);
                padding: 40px;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                max-width: 400px;
                width: 90%;
                transition: opacity 0.5s ease;
                margin: auto;
            }
            .form-section.active {
                display: block;
                opacity: 1;
            }
            .form-section label {
                display: block;
                margin-bottom: 5px;
                font-weight: 700;
            }
            .form-section input {
                width: 100%;
                padding: 10px;
                margin-bottom: 15px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            .form-section button {
                width: 100%;
                padding: 12px;
                border: none;
                border-radius: 5px;
                background: linear-gradient(45deg, #2196F3, #21CBF3);
                color: #fff;
                font-size: 16px;
                cursor: pointer;
                transition: background 0.3s;
            }
            .form-section button:hover {
                background: linear-gradient(45deg, #1976D2, #1E88E5);
            }
            .message-container {
                background: rgba(0, 0, 0, 0.7);
                color: #fff;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                margin-bottom: 20px;
                font-size: 24px;
                font-weight: bold;
            }
            .main-container {
                display: flex;
                flex-direction: column;
                align-items: center;
                padding-top: 120px;
            }
        """),
        Div(
            Div(
                H2("DRIVY", style="margin: 0;"),
                _class="header"
            ),
            Body(
                Div(
                    success_message and Div(success_message, _class="message-container"),
                    error_message and Div(error_message, _class="message-container"),
                    H3("LOGIN / REGISTER", style="font-size: 32px; text-align: center; margin-bottom: 20px; color: #fff;"),
                    Div(
                        Button("Login", type="button", id="loginBtn", _class="tab-btn active"),
                        Button("Register", type="button", id="registerBtn", _class="tab-btn"),
                        style="text-align: center; margin-bottom: 20px;"
                    ),
                    Form(
                        Div(
                            Div(Label("Username"), Input(type="text", id="login_username", name="login_username", required=True)),
                            Div(Label("Password"), Input(type="password", id="login_password", name="login_password", required=True))
                        ),
                        Button("LOG IN", type="submit"),
                        method="POST",
                        action="/login",
                        _class="form-section active",
                        id="login-section"
                    ),
                    Form(
                        Div(
                            Div(Label("Username"), Input(type="text", id="register_username", name="register_username", required=True)),
                            Div(Label("Password"), Input(type="password", id="register_password", name="register_password", required=True)),
                            Div(
                                Div(
                                    Input(type="radio", name="register_role", value="driver", required=True, checked=True),
                                    Label("Driver")
                                ),
                                Div(
                                    Input(type="radio", name="register_role", value="renter", required=True),
                                    Label("Renter")
                                ),
                                style="display: flex; justify-content: space-around; margin-bottom: 15px;"
                            )
                        ),
                        Button("REGISTER", type="submit"),
                        method="POST",
                        action="/register",
                        _class="form-section",
                        id="register-section"
                    ),
                    _class="main-container"
                )
            )
        ),
        Script("""
            document.getElementById('loginBtn').addEventListener('click', function() {
                document.getElementById('loginBtn').classList.add('active');
                document.getElementById('registerBtn').classList.remove('active');
                document.getElementById('login-section').classList.add('active');
                document.getElementById('register-section').classList.remove('active');
            });
            document.getElementById('registerBtn').addEventListener('click', function() {
                document.getElementById('registerBtn').classList.add('active');
                document.getElementById('loginBtn').classList.remove('active');
                document.getElementById('register-section').classList.add('active');
                document.getElementById('login-section').classList.remove('active');
            });
        """)
    )

@rt('/register', methods=["GET"])
def register_get() -> Response:
    return RedirectResponse("/", status_code=302)

@rt('/register', methods=["POST"])
def register(register_username: str, register_password: str, register_role: str):
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

@rt('/login', methods=["GET"])
def login_get():
    return RedirectResponse("/", status_code=302)

@rt('/login', methods=["POST"])
def login(login_username: str, login_password: str):
    username = login_username.strip()
    password = login_password.strip()
    
    if not username or not password:
        return get(error_message="กรุณากรอกข้อมูลให้ครบถ้วนในการเข้าสู่ระบบ")
    
    role = company.login(username, password)
    
    if role in ["user", "renter"]:
        return RedirectResponse("/search", status_code=302)
    elif role == "driver":
        return RedirectResponse("/driver", status_code=302)
    elif role == "admin":
        return RedirectResponse("/admin", status_code=302)
    else:
        return get(error_message="ข้อมูลเข้าสู่ระบบผิดพลาด กรุณาลองใหม่อีกครั้ง")

serve()
