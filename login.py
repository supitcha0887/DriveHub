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
    margin: 0;
    padding: 0;
    font-family: 'Roboto', sans-serif;
    background: linear-gradient(135deg, #bbdefb, #e3f2fd);
}
.header {
    width: 100%;
    background: #e3f2fd;
    padding: 25px 40px;
    position: fixed;
    top: 0;
    left: 0;
    border-bottom: 2px solid #90caf9;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    display: flex;
    align-items: center;
    justify-content: center;
}
.header h2 {
    margin: 0;
    font-size: 42px;
    color: #0d47a1;
}
.main-container {
    margin-top: 120px;
    display: flex;
    flex-direction: column;
    align-items: center;
}
.tab-btn {
    color: #555;
    font-size: 18px;
    font-weight: 600;
    background: none;
    border: none;
    outline: none;
    padding: 10px 20px;
    cursor: pointer;
    transition: color 0.3s, border-bottom 0.3s;
    border-bottom: 2px solid transparent;
}
.tab-btn:hover {
    color: #000;
}
.tab-btn.active {
    border-bottom: 2px solid #0d47a1;
    color: #0d47a1;
}
.form-section {
    background: #f1f8ff;
    padding: 40px;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    width: 100%;
    max-width: 400px;
    display: none;
    margin-top: 20px;
    transition: opacity 0.3s ease;
}
.form-section.active {
    display: block;
    opacity: 1;
}
.form-section label {
    display: block;
    margin-bottom: 5px;
    font-weight: 700;
    color: #0d47a1;
}
.form-section input {
    width: 100%;
    padding: 10px;
    margin-bottom: 15px;
    border: 1px solid #90caf9;
    border-radius: 4px;
}
.form-section button {
    width: 100%;
    padding: 12px;
    border: none;
    border-radius: 4px;
    background: #42a5f5;
    color: #fff;
    font-size: 16px;
    cursor: pointer;
    transition: background 0.3s;
}
.form-section button:hover {
    background: #1e88e5;
}
.message-container {
    padding: 15px;
    border-radius: 4px;
    margin-bottom: 20px;
    text-align: center;
    font-size: 16px;
    font-weight: 600;
}
.message-container.success {
    background: #d4edda;
    color: #155724;
}
.message-container.error {
    background: #f8d7da;
    color: #721c24;
}
"""),
        Div(
            Div(
                Img(src="/static/images/logo.png", alt="Drivy Logo", style="width: 70px; height: auto; margin-right: 10px;"),
                H2("DRIVY", style="margin: 0;"),
                _class="header"
            ),
            Body(
                Div(
                    success_message and Div(success_message, _class="message-container success"),
                    error_message and Div(error_message, _class="message-container error"),
                    H3("LOGIN / REGISTER", style="font-size: 28px; text-align: center; margin-bottom: 20px; color: #0d47a1;"),
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
        return get(error_message="Please fill in all required fields for registration.")
    username = register_username.strip()
    password = register_password.strip()
    user_role = register_role.strip()
    success, msg = company.register(username, password, user_role)
    if success:
        return get(success_message="Registration successful. Please log in.")
    else:
        return get(error_message=f"Registration failed: {msg}")

@rt('/login', methods=["GET"])
def login_get():
    return RedirectResponse("/", status_code=302)

@rt('/login', methods=["POST"])
def login(login_username: str, login_password: str):
    username = login_username.strip()
    password = login_password.strip()
    if not username or not password:
        return get(error_message="Please fill in all required fields for login.")
    role = company.login(username, password)
    if role in ["user", "renter"]:
        return RedirectResponse("/search", status_code=302)
    elif role == "driver":
        return RedirectResponse("/driver", status_code=302)
    elif role == "admin":
        return RedirectResponse("/admin", status_code=302)
    else:
        return get(error_message="Login failed. Please try again.")

serve()
