from fasthtml.common import *
app, rt = fast_app(live=True)
import BackEnd
import admin
import driver
import login
import search
import showcar
import reservation
import payment

if __name__ == "__routing__":
    rt.run()
