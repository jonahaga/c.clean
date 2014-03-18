import cssutils
# from cssutils import css, stylesheets


def main():
    f = open('/Users/Jona/Dropbox/Python/Hackbright/TechTalk/styles.css', 'r')
    c = f.read()
    f.close()

    css_file = cssutils.CSSParser().parseString(c)

    for i in css_file.cssRules:
        
        if not isinstance(i, cssutils.css.CSSComment):
            for j in i.selectorList:
                print j.selectorText

if __name__ == '__main__':
    main()