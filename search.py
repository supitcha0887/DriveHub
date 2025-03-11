from fasthtml.common import *
from routing import app, rt
import BackEnd
company = BackEnd.company

@rt('/search', methods=["GET"])
def search():
    return Container(
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
                background: #fff; 
                padding: 20px; 
                border-radius: 10px; 
                border: 1px solid #1C1C3B; 
                box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.2); 
                display: none; 
                margin-top: 20px;
                transition: opacity 0.5s ease;
            }
            .form-section.active { display: block; opacity: 1; }
        """),
        Div(
            Div(
                Div(
                    H2("DRIVY", style="color: #FFF; margin: 0;"),
                    style="display: flex; align-items: center; gap: 0px;"
                ),
                style="display: flex; justify-content: space-between; align-items: center; width: 100%;"
            ),
            style=""" 
                width: 100%; 
                background: #4682B4; 
                padding: 25px; 
                border-bottom: 2px solid #502314; 
                position: fixed; 
                top: 0; 
                left: 0; 
                z-index: 1000;
            """
        ),
        Body(
            H5("SEARCH CAR FOR", style="font-size: 36px; text-align: center; color: #1C1C3B;"),
            Div(
                Form(
                    Div(
                        Label("model", style="color: #1C1C3B; font-size: 18px; font-weight: bold;"),
                        Select(
                            Option("All"),
                            *[Option(car.get_model(), value=car.get_model()) for car in company.get_cars()],
                            id="allcar",
                            name="allcar",
                            style="background: #fff; padding: 8px; border-radius: 15px; border: 1px solid #1C1C3B; width: 100%;"
                        ),
                    ),
                    Button("Search", type="submit", style="background: #1C1C3B; color: white; font-weight: bold; padding: 10px 20px; border: none; border-radius: 20px; cursor: pointer; margin-top: 20px; width: 100%;"),
                    method="get",
                    action="/showcar",
                    _class="search-form",
                    style="max-width: 500px; margin: auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.2);"
                ),
                # ลบส่วนที่เกี่ยวกับการเลือกวันที่ออกไป
            ),
            style="background: #AEEEEE; padding: 20px; min-height: 100vh; margin-top: 80px;"
        )
    )

serve()
