from flask import Flask, render_template, g, session, url_for, flash, request
from cssclean import *

app = Flask(__name__)

@app.route("/", methods=["POST"])
def process():

    return render_template("results.html")

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/results", methods=["POST"])
def results():
    html_to_parse = request.form.get("html")
    css_to_parse = request.form.get("css")

    # instantiate the parser and feed it some HTML
    parser = MyHTMLParser()
    parser.feed(compile_files(html_to_parse))
    parser.close()

    sheet = cssutils.CSSParser().parseString(compile_files(css_to_parse))
    
    # Run delete_rules function to delete unused rules and get new stylesheet
    deleted_selectors = delete_selectors(sheet, parser)[1]
    deleted_rules = delete_selectors(sheet, parser)[2]
    new_stylesheet = delete_rules(delete_selectors, sheet, parser)

    deleted_selectors.sort()
    deleted_rules.sort()

    return render_template("results.html", deleted_selectors=deleted_selectors, 
                                           deleted_rules=deleted_rules,
                                           new_stylesheet=new_stylesheet)

if __name__ == "__main__":
    app.run(debug=True)
