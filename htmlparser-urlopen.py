from HTMLParser import HTMLParser
import urllib
import cssutils
import re


opener = urllib.FancyURLopener({})
html_to_parse = raw_input('> HTML to Parse: ')
css_to_parse = raw_input('> CSS to Parse: ')


# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    selectors = []
    def handle_starttag(self, tag, attrs):
        ignore = ['html', 'head', 'title', 'link', 'style', 'script', 'meta']
        if tag not in ignore:
            for i in attrs:
                if i[0] == 'class':
                    class_index = attrs.index(i)
                    
                    if attrs and attrs[class_index][0] == 'class': #or attrs[1][0]:
                        if attrs and ' ' in attrs[class_index][1]:
                            split_attrs = attrs[class_index][1].split()
                            self.selectors.append(tag + '.' + split_attrs[0])
                            self.selectors.append(tag + '.' + split_attrs[1])
                            self.selectors.append(tag + '.' + split_attrs[0] + '.' + split_attrs[1])
                            self.selectors.append('.' + split_attrs[0])
                            self.selectors.append('.' + split_attrs[1])
                            self.selectors.append('.' + split_attrs[0] + '.' + split_attrs[1])
                        else:
                            self.selectors.append('.' + attrs[class_index][1])
                            self.selectors.append(tag + '.' + attrs[class_index][1])

                elif i[0] == 'id':
                    id_index = attrs.index(i)
                    
                    if attrs and attrs[id_index][0] == 'id':
                        if attrs and ' ' in attrs[id_index][1]:
                            split_attrs = attrs[id_index][1].split()
                            self.selectors.append(tag + '#' + split_attrs[0])
                            self.selectors.append(tag + '#' + split_attrs[1])
                            self.selectors.append(tag + '#' + split_attrs[0] + '#' + split_attrs[1])
                            self.selectors.append('#' + split_attrs[0])
                            self.selectors.append('#' + split_attrs[1])
                            self.selectors.append('#' + split_attrs[0] + '#' + split_attrs[1])
                        else:
                            self.selectors.append('#' + attrs[id_index][1])
                            self.selectors.append(tag + '#' + attrs[id_index][1])
                else:
                    self.selectors.append(tag)

def compile_files(files_to_parse):
    file_list = files_to_parse.split(',')
    new_file = ''

    for i in file_list:
        stripped = i.strip()
        f = opener.open(stripped, 'r')
        n = f.read()

        new_file += n

        f.close()

    return new_file

css_file = cssutils.CSSParser().parseString(compile_files(css_to_parse))

def css_parser(files_to_parse):
    css_dict = {}

    for i in css_file.cssRules:
        if not isinstance(i, cssutils.css.CSSComment) and not isinstance(i, cssutils.css.CSSImportRule):
            for j in i.selectorList:
                p = re.compile('\.\w*(\.)\w*')

                if p.match(str(j.selectorText)) and ' ' not in j.selectorText:
                    dot_combinator = re.split(('(\.\w*)(\.\w*)', str(j.selectorText)))
                    
                    for m in dot_combinator:
                        if m == '':
                            pass
                        else:
                            css_dict.update({m:[i, i.selectorList, j]})

                elif ' ' in j.selectorText:
                    combinator = str(j.selectorText)
                    split_combinator = combinator.split()

                    for k in split_combinator:
                        if k == '>' or k == '+' or k == '~':
                            pass
                        elif p.match(k):
                            dot_split = re.split('(\.\w*)(\.\w*)', k)
                            for s in dot_split:
                                if s == '':
                                    pass
                                else:
                                    css_dict.update({s:[i, i.selectorList, j]})
                        else:
                            css_dict.update({k:[i, i.selectorList, j]})               
                
                elif '*' in j.selectorText:
                    pass
                else:
                    css_dict.update({str(j.selectorText):[i, i.selectorList, j]})

    return css_dict

def split_pseudo(d):
    css_dict = {}

    for key in d:
        if ':' in key:
            split_pseudo = key.split(':')
            if '[' not in split_pseudo[0]:
                css_dict.update({split_pseudo[0]: css_parser(css_file).get(key)})
            else:
                attribute_selector = split_pseudo[0].split('[')
                css_dict.update({attribute_selector[0]: css_parser(css_file).get(key)})
        else:
            css_dict.update({key: css_parser(css_file).get(key)})

    return css_dict

def del_dupes(l):
    c = {}
    h = []

    if type(l) is dict:
        for key in l:
            if key not in c:
                c.update({key: l.get(key)})
        return c
    else:
        for i in l:
            if i not in h:
                h.append(i)
        return h

def compare_selectors():
    selectors_to_delete = []

    for key, value in del_dupes(split_pseudo(css_parser(css_file))).iteritems():
        if key not in del_dupes(parser.selectors):
            if len(value[1]) > 1:
                pass
            else:
                print value[0]
                css_file.deleteRule(value[0])
            # print key, 'is not used'
            # print key, value
            # rules_to_delete.append(value[1])


    print 'NEW CSS\n', css_file.cssText


# instantiate the parser and feed it some HTML
parser = MyHTMLParser()
parser.feed(compile_files(html_to_parse))
parser.close()

# instantiate the css parser and feed it some CSS
print compare_selectors()

