# {c.lean}
CSS Clean, or **{c.lean}**, is a tool that compares your webpages to the CSS files styling those webpages, deletes any unused rules or selectors and returns a new, clean and lean stylesheet.

## Why {c.lean} Your Stylesheets?
When you visit a website, your browser downloads all the linked stylesheets, Javascript files and images and loads them. Once the stylesheet is loaded, the browsers's CSS engine analyzes each style rule in the stylesheet and determines if the rule is implemented by the current page. If there are a lot of unused rules in the stylesheet, latency is increased and user experience is affected. Using **{c.lean}** on your stylesheets allows you to minimize latency by reducing the amount of data sent in each server response.

## Scraping HTML
To parse the HTML, I use the Python module [HTMLParser](https://docs.python.org/2/library/htmlparser.html). Because most webpages use Javascript to manipulate the DOM and add classes/IDs, I use a headless browser to open the webpages with Javascript loaded to catch those Javascript-injected attributes. I also load the webpages at both a desktop and mobile window size to catch any responsive styles. Because loading webpages with the headless browser takes a much longer time than just opening the plain HTML file on the server, users of {c.lean} have the option of loading the pages without Javascript loaded.

Once all the webpages are loaded into the HTML parser, I build a list of all the HTML tags and their attributes. This list will be used later to compare the parsed CSS selectors to and identify which rules and selectors aren't being used. 

## Parsing the CSS
For stylesheet parsing, I used [cssutils](https://pypi.python.org/pypi/cssutils/1.0). As the stylesheet is being parsed, I build a list of tuples containing the selector text of the rule, as well as the rule's place in the stylesheet. I pass that list to another function that breaks the selector text down even further to split dot combined selectors. For example, ```.sidebar.featured``` would be stored in the CSS selector list as ```.sidebar``` and ```.featured```. 

Since, as the name implies, pseudo selectors don't actually live in the DOM and wouldn't exist in the list of HTML tags and attributes created when parsing the HTML, the CSS selector list is passed to another function that splits pseudo selectors and strips away their pseudo attribute. So ```li:first-child``` would be stored in the CSS selector list as ```li```. 

## Cleaning Up the Stylesheet
Once the CSS selectors list is complete, it is passed into another function that deletes individual (unused) selectors from a style rule. 

For example, if in our stylesheet we have:
    
    h1, h2, h3, h4, h5, h6 {
        font-weight: bold
    }

If our HTML only uses ```h1```, ```h2```, and ```h3```, this function will delete ```h4```, ```h5```, and ```h6``` since they aren't being used. The new, cleaned rule will be:

    h1, h2, h3 {
        font-weight: bold
    }

After the unused selectors are deleted from the stylesheet, another function deletes entire rules that aren't being used and returns the new, clean and lean stylesheet.