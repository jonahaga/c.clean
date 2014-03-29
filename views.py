from flask import Flask, render_template, request
from cssclean import *
from rq import Queue
from worker import conn


app = Flask(__name__)
q = Queue(connection-conn)

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
    q.enqueue(parser.feed(compile_html(html_to_parse)))
    parser.close()
    
    # Run delete_rules function to delete unused rules and get new stylesheet
    sheet = cssutils.CSSParser().parseString(compile_css(css_to_parse))
    deleted_selectors = del_dupes(delete_selectors(sheet, parser)[1])
    deleted_rules = del_dupes(delete_selectors(sheet, parser)[2])
    new_stylesheet = delete_rules(delete_selectors, sheet, parser)

    deleted_selectors.sort()
    deleted_rules.sort()

    return render_template("results.html", deleted_selectors=deleted_selectors, 
                                           deleted_rules=deleted_rules,
                                           new_stylesheet=new_stylesheet )

if __name__ == "__main__":
    app.run(debug=True)
