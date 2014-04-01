from cssclean import *
from flask import Flask, render_template, request, flash, redirect, url_for


app = Flask(__name__)
app.secret_key = "shhhhthisisasecret"

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

    if 'http' not in html_to_parse or 'http' not in css_to_parse:
        flash("Don't forget 'http://'")
        return redirect(url_for("index"))
    else:
        # instantiate the parser and feed it some HTML
        parser = MyHTMLParser()
        parser.feed(compile_html(html_to_parse))
        # parser.feed(compile_css(html_to_parse))
        parser.close()

        # Run delete_rules function to delete unused rules and get new stylesheet
        sheet = cssutils.CSSParser().parseString(compile_css(css_to_parse))
        deleted_selectors = delete_selectors(sheet, parser)[2]
        deleted_rules = del_dupes(delete_selectors(sheet, parser)[1])
        new_stylesheet = delete_rules(delete_selectors, sheet, parser)

        deleted_rules.sort()

        return render_template("results.html", deleted_selectors=deleted_selectors,
                                               deleted_rules=deleted_rules,
                                               new_stylesheet=new_stylesheet )

if __name__ == "__main__":
    app.run(debug=True)
