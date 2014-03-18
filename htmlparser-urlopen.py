from HTMLParser import HTMLParser
import urllib
import cssutils


opener = urllib.FancyURLopener({})
html_to_parse = raw_input('> HTML to Parse: ')
css_to_parse = raw_input('> CSS to Parse: ')


# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    selectors = []
    def handle_starttag(self, tag, attrs):
        ignore = ['html', 'head', 'title', 'link', 'style', 'script', 'meta']
        if tag not in ignore:
            if attrs and attrs[0][0] != 'href' and attrs[0][0] == 'class':
                if attrs and ' ' in attrs[0][1]:
                    split_attrs = attrs[0][1].split()
                    self.selectors.append(tag + '.' + split_attrs[0])
                    self.selectors.append(tag + '.' + split_attrs[1])
                    self.selectors.append(tag + '.' + split_attrs[0] + '.' + split_attrs[1])
                    self.selectors.append('.' + split_attrs[0])
                    self.selectors.append('.' + split_attrs[1])
                    self.selectors.append('.' + split_attrs[0] + '.' + split_attrs[1])
                else:
                    self.selectors.append('.' + attrs[0][1])
                    self.selectors.append(tag + '.' + attrs[0][1])
            elif attrs and attrs[0][0] != 'href' and attrs[0][0] == 'id':
                if attrs and ' ' in attrs[0][1]:
                    split_attrs = attrs[0][1].split()
                    self.selectors.append(tag + '#' + split_attrs[0])
                    self.selectors.append(tag + '#' + split_attrs[1])
                    self.selectors.append(tag + '#' + split_attrs[0] + '#' + split_attrs[1])
                    self.selectors.append('#' + split_attrs[0])
                    self.selectors.append('#' + split_attrs[1])
                    self.selectors.append('#' + split_attrs[0] + '#' + split_attrs[1])
                else:
                    self.selectors.append('#' + attrs[0][1])
                    self.selectors.append(tag + '#' + attrs[0][1])
            else:
                self.selectors.append(tag)

def compile_files(files_to_parse):
    file_list = files_to_parse.split(',')
    new_file = ''

    for i in file_list:
        stripped = i.strip()
        f = opener.open(stripped, 'r')
        h = f.read()

        new_file += h

        f.close()

    return new_file

def css_parser(files_to_parse):
    css_selectors = []
    css_file = cssutils.CSSParser().parseString(compile_files(files_to_parse))

    for i in css_file.cssRules:
        if not isinstance(i, cssutils.css.CSSComment) and not isinstance(i, cssutils.css.CSSImportRule):
            for j in i.selectorList:
                if ' ' in j.selectorText:
                    combinator = str(j.selectorText)
                    split_combinator = combinator.split()
                    for k in split_combinator:
                        if k != '>':
                            css_selectors.append(k)
                else:
                    css_selectors.append(str(j.selectorText))

    return css_selectors

def split_pseudo(l):
    css_selectors = []

    for i in l:
        if ':' in i:
            split_pseudo = i.split(':')
            if '[' not in split_pseudo[0]:
                css_selectors.append(split_pseudo[0])
            else:
                attribute_selector = split_pseudo[0].split('[')
                css_selectors.append(attribute_selector[0])
        else:
            css_selectors.append(i)

    return css_selectors

def del_dupes(l):
    n = []

    for i in l:
        if i not in n:
            n.append(i)
    return n

def compare_selectors():
    for i in css_selectors:
        if i not in del_dupes(parser.selectors):
            print i, 'is not used'

# instantiate the parser and fed it some HTML
parser = MyHTMLParser()
parser.feed(compile_files(html_to_parse))
css_selectors = del_dupes(split_pseudo(css_parser(css_to_parse)))
# print del_dupes(parser.selectors)
print compare_selectors()
parser.close()

