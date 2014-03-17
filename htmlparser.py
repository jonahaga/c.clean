from HTMLParser import HTMLParser
from cssselect import GenericTranslator, SelectorError

files_to_parse = raw_input('> ')

# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    selectors = []
    css_files = []
    def handle_starttag(self, tag, attrs):
        ignore = ['html', 'head', 'title', 'link', 'style', 'script']

        if tag not in ignore:
            if attrs and attrs[0][0] != 'href' and attrs[0][0] == 'class':
                if attrs and ' ' in attrs[0][1]:
                    split_attrs = attrs[0][1].split()
                    self.selectors.append('.' + split_attrs[0])
                    self.selectors.append('.' + split_attrs[1])
                    self.selectors.append('.' + split_attrs[0] + '.' + split_attrs[1])
                else:
                    self.selectors.append('.' + attrs[0][1])
            elif attrs and attrs[0][0] != 'href' and attrs[0][0] == 'id':
                if attrs and ' ' in attrs[0][1]:
                    split_attrs = attrs[0][1].split()
                    self.selectors.append('#' + split_attrs[0])
                    self.selectors.append('#' + split_attrs[1])
                    self.selectors.append('#' + split_attrs[0] + '#' + split_attrs[1])
                else:
                    self.selectors.append('#' + attrs[0][1])
        elif tag == 'link':
            if attrs[0][0] == 'href':
                self.css_files.append(attrs[0][1])

def del_dupes(l):
    n = []

    for i in l:
        if i not in n:
            n.append(i)
    return n

def compile_html(files_to_parse):
    file_list = files_to_parse.split(',')
    new_file = ''

    for i in file_list:
        stripped = i.strip()
        f = open(stripped, 'r')
        h = f.read()

        new_file += h

        f.close()

    return new_file

def compile_css(css_files):
    file_list = css_files.split(',')
    new_file = ''

    for i in file_list:
        stripped = i.strip()
        f = open(stripped, 'r')
        h = f.read()

        new_file += h

        f.close()

    return new_file

# instantiate the parser and fed it some HTML
parser = MyHTMLParser()
parser.feed(compile_html(files_to_parse))
print del_dupes(parser.selectors)
parser.close()

# Read more about how cssselect is supposed to work 
# cssselect.parse(compile_css(parser.css_files))