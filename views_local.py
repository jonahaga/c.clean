from cssclean import *
from flask import Flask, render_template, request


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
    phantom = request.form.get("phantom")

    # instantiate the parser and feed it some HTML
    parser = MyHTMLParser()

    if phantom == "without_phantom":
        parser.feed(compile_files(html_to_parse))
        parser.close()

        # Run delete_rules function to delete unused rules and get new stylesheet
        orig_stylesheet = cssutils.CSSParser().parseString(compile_files(css_to_parse)).cssText
        sheet = cssutils.CSSParser().parseString(compile_files(css_to_parse))
        deleted_selectors = delete_selectors(sheet, parser)[2]
        deleted_rules = del_dupes(delete_selectors(sheet, parser)[1])
        new_stylesheet = delete_rules(delete_selectors, sheet, parser)
        sheet_diff = diff(orig_stylesheet, new_stylesheet)

        deleted_rules.sort()

        return render_template("results.html", deleted_selectors=deleted_selectors,
                                               deleted_rules=deleted_rules,
                                               new_stylesheet=new_stylesheet,
                                               sheet_diff=sheet_diff )
    else:
        parser.feed(compile_phantom(html_to_parse))
        parser.close()

        # Run delete_rules function to delete unused rules and get new stylesheet
        orig_stylesheet = cssutils.CSSParser().parseString(compile_files(css_to_parse)).cssText
        sheet = cssutils.CSSParser().parseString(compile_files(css_to_parse))
        deleted_selectors = delete_selectors(sheet, parser)[2]
        deleted_rules = del_dupes(delete_selectors(sheet, parser)[1])
        new_stylesheet = delete_rules(delete_selectors, sheet, parser)
        sheet_diff = diff(orig_stylesheet, new_stylesheet)

        deleted_rules.sort()

        return render_template("results.html", deleted_selectors=deleted_selectors,
                                               deleted_rules=deleted_rules,
                                               new_stylesheet=new_stylesheet,
                                               sheet_diff=sheet_diff )

if __name__ == "__main__":
    app.run(debug=True, port=5001)
