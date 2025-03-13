from fasthtml.common import *
from routing import app, rt
import BackEnd

company = BackEnd.company

@rt('/showcar/{model}/{start_date}/{end_date}', methods=["GET"])
def showcar(model: str, start_date: str, end_date: str):
    print()
    if model == "All":
        filtered_cars = [car for car in company.find_available_car(start_date,end_date) if car.get_status() == "available"]
    else:
        filtered_cars = [car for car in company.find_available_car_type(model,start_date,end_date) if car.get_model() == model and car.get_status() == "available"]
    return Container(
        Style(f"""
html, body {{
    height: 100%;
    font-family: 'Roboto', sans-serif;
    margin: 0;
    padding: 0;
    background: linear-gradient(135deg, #bbdefb, #e3f2fd);
    background-size: cover;
}}
.header {{
    width: 100%;
    background: #e3f2fd;
    padding: 25px;
    position: fixed;
    top: 0;
    left: 0;
    z-index: 1000;
    text-align: center;
    border-bottom: 2px solid #90caf9;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}}
.header h2 {{
    color: #0d47a1;
    margin: 0;
    font-size: 42px;
    letter-spacing: 2px;
}}
.content {{
    margin-top: 120px;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 25px;
    padding: 20px;
}}
.card {{
    background: #fff;
    
    border-radius: 10px;
    overflow: hidden;
    flex-direction: row;
    padding: 15px;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}}
.card:hover {{
    transform: scale(1.03);
    box-shadow: 0 8px 16px rgba(0,0,0,0.2);
}}
.card-img {{
    flex: 0 0 auto;
    margin-right: 15px;
}}
.card-img img {{
    width: 20%;
    height: auto;
    display: block;
    border-radius: 5px;
    border: 2px solid #90caf9;
    transition: opacity 0.3s ease;
}}
.card-img img:hover {{
    opacity: 0.9;
}}
.card-details {{
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    text-align: center;
}}
.card-details h3 {{
    margin: 0 0 10px;
    font-size: 24px;
    color: #0d47a1;
    font-weight: 600;
}}
.card-details p {{
    margin: 3px 0;
    font-size: 16px;
    color: #333;
}}
.select-container {{
    flex: 0 0 auto;
    margin-left: 15px;
}}
.select-btn {{
    background: linear-gradient(45deg, #0052d4, #4364f7);
    color: #fff;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background 0.3s ease, transform 0.3s;
    margin-top: 10px;
}}
.select-btn:hover {{
    background: linear-gradient(45deg, #003bb5, #345ecb);
    transform: translateY(-2px);
}}
.reviews {{
    margin-top: 10px;
    background: #f1f8ff;
    border-radius: 5px;
    padding: 10px;
    text-align: left;
    animation: fadeIn 1s ease;
}}
.reviews h4 {{
    margin: 0 0 5px;
    font-size: 16px;
    color: #0052d4;
    border-bottom: 1px solid #ccc;
    padding-bottom: 3px;
}}
.review-item {{
    margin-bottom: 5px;
    padding-bottom: 5px;
    border-bottom: 1px dashed #ddd;
}}
.review-item:last-child {{
    border-bottom: none;
    margin-bottom: 0;
    padding-bottom: 0;
}}
.review-item p {{
    margin: 2px 0;
    font-size: 14px;
    color: #555;
}}
@keyframes fadeIn {{
    from {{ opacity: 0; transform: translateY(10px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}
"""),
        Div(
            Div(
                Img(src="/static/images/logo.png", alt="Drivy Logo", style="width: 70px; height: auto; margin-right: 10px;"),
                H2("DRIVY", style="margin: 0;"),
                style="display: flex; align-items: center;",
                _class="header"
            ),
            Div(
                *[ 
                    Div(
                        Div(
                            Img(src=car.get_image(), alt="Car Image", _class="card-img")
                        ),
                        Div(
                            Div(
                                H3(car.get_model()),
                                P("License: " + car.get_licensecar()),
                                P("Price: " + str(car.get_price())+"bath"),
                                P("Status: " + car.get_status()),
                                P("Color: " + car.get_color()),
                                P("Seats: " + car.get_seat_count())
                            ),
                            Div(
                                Form(
                                    Input(type="hidden", name="car_id", value=car.get_id()),
                                    Input(type="hidden", name="start_date", value=start_date),
                                    Input(type="hidden", name="end_date", value=end_date),
                                    Button("Select", type="submit", _class="select-btn"),
                                    action="/reservation/form", method="GET"
                                ),
                                _class="select-container"
                            ),
                            Div(
                                H4("Reviews:"),
                                *[
                                    Div(
                                        _class="review-item",
                                        *[
                                            P("Rating: " + (str(round(car.cal_rating(),1)) if car.get_ratings() else "No ratings")),
                                            P("Comment: " + rev.get_comment()),
                                            P("Date: " + rev.get_date())
                                        ]
                                    )
                                    for rev in car.get_reviews()
                                ],
                                _class="reviews"
                            ),
                            _class="card-details"
                        ),
                        _class="card"
                    ) for car in filtered_cars
                ],
                _class="content"
            )
        )

    )

serve()
