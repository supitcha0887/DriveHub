from fasthtml.common import *
from routing import app, rt
import BackEnd
company = BackEnd.company

@rt('/showcar',methods=["GET"])
def showcar(allcar: str = "All"):
    # กรองรายชื่อรถตามรุ่นที่เลือก ถ้าเลือก "All" ให้แสดงทุกคัน
    if allcar == "All":
        filtered_cars = company.get_cars()
    else:
        filtered_cars = [car for car in company.get_cars() if car.get_model() == allcar]
    return Container(
        Style("""
            /* กำหนด style สำหรับทั้งหน้า */
            body {
                font-family: Arial, sans-serif;
                background: #AEEEEE;
                padding: 20px;
            }
            .header {
                width: 100%;
                background: #4682B4;
                padding: 25px;
                border-bottom: 2px solid #502314;
                position: fixed;
                top: 0;
                left: 0;
                z-index: 1000;
            }
            .header h2 {
                color: #B0E0E6;
                margin: 0;
            }
            .content {
                margin-top: 80px;
                max-width: 800px;
                margin-left: auto;
                margin-right: auto;
                background: #fff;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0px 2px 4px rgba(0,0,0,0.2);
            }
            h3 {
                text-align: center;
                color: #1C1C3B;
                font-size: 36px;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }
            th, td {
                padding: 8px;
                border: 1px solid #ddd;
                text-align: center;
            }
            th {
                background-color: #f2f2f2;
            }
            tr:hover {
                background-color: #f9f9f9;
            }
            button {
                background: #4CAF50;
                color: white;
                padding: 5px 10px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
            }
            button:hover {
                background: #45a049;
            }
            img {
                width: 100px;
                height: auto;
                border-radius: 5px;
            }
        """),

        # Header Bar
        Div(
            Div(
                Div(
                    H2("DRIVY", style="color: #fff; margin: 0;"),
                    style="display: flex; align-items: center; gap: 0px;"
                ),
                style="display: flex; justify-content: space-between; align-items: center; width: 100%;"
            ),
            _class="header"
        ),
        # Body Content

        Body(
            Div(
                H3("Car Details"),
                Table(
                    # Header ของตาราง
                    Tr(
                        Th("ID"),
                        Th("Model"),
                        Th("License"),
                        Th("Price"),
                        Th("Status"),
                        Th("Color"),
                        Th("Select")
                    ),
                     # สร้างแถวข้อมูลรถจาก backend
                    *[
                        Tr(
                            Td(car._Car__id),
                            Td(car.get_model()),
                            Td(car._Car__licensecar),
                            Td(str(car._Car__price)),
                            Td(car.get_status()),
                            Td(car._Car__color),
                            Td(Form(
                                Input(type="hidden", name="car_id", value=car._Car__id),
                                Input(type="hidden", name="start_date", value="2025-03-12"),
                                Input(type="hidden", name="end_date", value="2025-03-13"),
                                Button("Select", type="submit"),
                                action="/reservation", method="POST"
                            ))
                        ) for car in filtered_cars
                    ],
                    {"style": "width: 100%;"}
                ),
                _class="content"
            ),
            style="background: #AEEEEE; padding: 20px; min-height: 100vh;"
        )
    )

serve()