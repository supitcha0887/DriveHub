from fasthtml.common import *
from routing import app, rt
import BackEnd

company = BackEnd.company

@rt('/showcar/{model}/{start_date}/{end_date}', methods=["GET"])
def showcar(model: str, start_date: str, end_date: str):
    if model == "All":
        filtered_cars = company.get_cars()
        grid_template = "repeat(auto-fit, minmax(320px, 1fr))"
    else:
        filtered_cars = [car for car in company.get_cars() if car.get_model() == model]
        grid_template = "repeat(auto-fit, minmax(300px, 1fr))"
    
    return Container(
        Style(f"""
            html, body {{
                height: 100%;
                font-family: 'Roboto', sans-serif;
                margin: 0;
                padding: 0;
                background: linear-gradient(135deg, #2196F3, #21CBF3);
                background-size: cover;
                animation: bgAnimation 10s infinite alternate;
            }}
            @keyframes bgAnimation {{
                from {{ filter: brightness(1); }}
                to {{ filter: brightness(1.1); }}
            }}
            .header {{
                width: 100%;
                background: rgba(0,0,0,0.6);
                padding: 10px 20px;
                position: fixed;
                top: 0;
                left: 0;
                z-index: 1000;
                text-align: center;
                box-shadow: 0 2px 8px rgba(0,0,0,0.5);
            }}
            .header h2 {{
                color: #fff;
                margin: 0;
                font-size: 42px;
                letter-spacing: 2px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
            }}
            .content {{
                margin-top: 120px;
                display: grid;
                grid-template-columns: {grid_template};
                gap: 25px;
                padding: 20px;
            }}
            .card {{
                background: #fff;
                border-radius: 10px;
                overflow: hidden;
                display: flex;
                flex-direction: column;
                transition: transform 0.3s ease, box-shadow 0.3s ease;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }}
            .card:hover {{
                transform: scale(1.03);
                box-shadow: 0 8px 16px rgba(0,0,0,0.2);
            }}
            .card img {{
                width: 100%;
                height: auto;
                display: block;
                transition: opacity 0.3s ease;
            }}
            .card img:hover {{
                opacity: 0.9;
            }}
            .card-details {{
                padding: 20px;
                text-align: center;
                flex-grow: 1;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
            }}
            .card-details h3 {{
                margin: 0 0 10px;
                font-size: 26px;
                color: #004e92;
            }}
            .card-details p {{
                margin: 5px 0;
                font-size: 15px;
                color: #333;
            }}
            .select-btn {{
                margin-top: 15px;
                background: linear-gradient(45deg, #2196F3, #21CBF3);
                color: #fff;
                padding: 12px 20px;
                border: none;
                border-radius: 5px;
                font-size: 16px;
                cursor: pointer;
                transition: background 0.3s ease, transform 0.3s;
            }}
            .select-btn:hover {{
                background: linear-gradient(45deg, #1976D2, #1E88E5);
                transform: translateY(-2px);
            }}
            .reviews {{
                margin-top: 20px;
                background: #f0f8ff;
                border-radius: 5px;
                padding: 15px;
                text-align: left;
                animation: fadeIn 1s ease;
            }}
            .reviews h4 {{
                margin: 0 0 10px;
                font-size: 18px;
                color: #0052d4;
                border-bottom: 1px solid #ccc;
                padding-bottom: 5px;
            }}
            .review-item {{
                margin-bottom: 10px;
                padding-bottom: 10px;
                border-bottom: 1px dashed #ddd;
            }}
            .review-item:last-child {{
                border-bottom: none;
                margin-bottom: 0;
                padding-bottom: 0;
            }}
            .review-item p {{
                margin: 3px 0;
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
                        Img(src=car.get_image(), alt="Car Image"),
                        Div(
                            H3(car.get_model()),
                            P("License: " + car.get_licensecar()),
                            P("Price: $" + str(car.get_price())),
                            P("Status: " + car.get_status()),
                            P("Color: " + car.get_color()),
                            P("Seats: " + car.get_seat_count()),
                            P("Start: " + start_date),
                            P("End: " + end_date),
                            Form(
                                Input(type="hidden", name="car_id", value=car.get_id()),
                                Input(type="hidden", name="start_date", value=start_date),
                                Input(type="hidden", name="end_date", value=end_date),
                                Button("Select", type="submit", _class="select-btn"),
                                action="/reservation/form", method="GET"
                            ),
                            Div(
                                H4("Reviews:"),
                                *[
                                    Div(
                                        _class="review-item",
                                        children=[
                                            P("Rating: " + (str(round(sum(car.get_ratings())/len(car.get_ratings()),1)) if car.get_ratings() else "No ratings")),
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