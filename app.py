from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("login_page.html")

app.run()

"""
nom societe : MGO SA GROUP
MGO S.A group, specialize in agrifood and perfumery products, with 2000
people in the world.
The group has 4 main suppliers of raw materials and 10 outlets including 6
in France and 4 in Belgium. The Company has just bought two production
sites in Asia for the Asian market and two production sites in Africa for the
African market.
"""