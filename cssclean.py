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

sheet = cssutils.CSSParser().parseString(compile_files(css_to_parse))

def css_parser(files_to_parse):
    css_dict = {}

    for i_idx, i in enumerate(sheet.cssRules):
        if not isinstance(i, cssutils.css.CSSComment) and not isinstance(i, cssutils.css.CSSImportRule):
            for idx, j in enumerate(i.selectorList):
                p = re.compile('\.\w*(\.)\w*')

                if p.match(str(j.selectorText)) and ' ' not in j.selectorText:
                    dot_combinator = re.split(('(\.\w*)(\.\w*)', str(j.selectorText)))
                    
                    for m in dot_combinator:
                        if m == '':
                            pass
                        else:
                            css_dict.update({m:[i, i_idx, i.selectorList, j, idx]})

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
                                    css_dict.update({s:[i, i_idx, i.selectorList, j, idx]})
                        else:
                            css_dict.update({k:[i, i_idx, i.selectorList, j, idx]})               
                
                elif '*' in j.selectorText:
                    pass
                else:
                    css_dict.update({str(j.selectorText):[i, i_idx, i.selectorList, j, idx]})

    return css_dict

def split_pseudo(d):
    css_dict = {}

    for key in d:
        if ':' in key:
            split_pseudo = key.split(':')
            if '[' not in split_pseudo[0]:
                css_dict.update({split_pseudo[0]: css_parser(sheet).get(key)})
            else:
                attribute_selector = split_pseudo[0].split('[')
                css_dict.update({attribute_selector[0]: css_parser(sheet).get(key)})
        else:
            css_dict.update({key: css_parser(sheet).get(key)})

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

def delete_selectors():
    rules_to_delete = []

    for key, value in del_dupes(split_pseudo(css_parser(sheet))).iteritems():
        if key not in del_dupes(parser.selectors):
            if len(value[2]) > 1:
                rule_idx = value[1]

                for idx, data in enumerate(sheet.cssRules[rule_idx].selectorList):
                    if idx != len(sheet.cssRules[rule_idx].selectorList) - 1:
                        print 'This is not the last item.\n\tData: ', data,'\n\t', 'Index:', idx
                        pass
                    else:
                        print 'This is the last item.\n\tData: ', data,'\n\t', 'Index:', idx
                        del sheet.cssRules[rule_idx].selectorList[idx]
            else:
                rules_to_delete.append(value[0])

    # print 'NEW CSS\n', sheet.cssText
    return rules_to_delete

def delete_rules():
    


# instantiate the parser and feed it some HTML
parser = MyHTMLParser()
parser.feed(compile_files(html_to_parse))
parser.close()

# instantiate the css parser and feed it some CSS
print delete_selectors()

