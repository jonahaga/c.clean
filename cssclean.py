import cssutils
import re
from HTMLParser import HTMLParser
from urllib2 import urlopen


# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    selectors = []
    def handle_starttag(self, tag, attrs):
        ignore = ['head', 'title', 'link', 'style', 'script', 'meta']
        if tag not in ignore:
            if attrs:
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
            else:
                self.selectors.append(tag)

def compile_files(files_to_parse):
    file_list = files_to_parse.split(',')
    new_file = ''

    for i in file_list:
        stripped = i.strip()
        f = urlopen(stripped)
        n = f.read()

        new_file += n

        f.close()

    return new_file

def css_parser(sheet):
    css_dict = []

    for i_idx, i in enumerate(sheet.cssRules):
        if not isinstance(i, cssutils.css.CSSComment) and not isinstance(i, cssutils.css.CSSImportRule):
            for idx, j in enumerate(i.selectorList):
                css_dict.append((str(j.selectorText), [i, i_idx, i.selectorList, j, idx]))

    return css_dict

def split_combinator(l, sheet):
    css_dict = []

    for i in l:
        p = re.compile('\.\w+(-|\w)+\.\w+(-|\w)+')

        if p.search(i[0]) and ' ' not in i[0]:
            dot_combinator = re.split('(\.\w+(-|\w)+)(\.\w+(-|\w)+)', i[0])

            for j in dot_combinator:
                if j == '' or len(j) <= 1:
                    pass
                else:
                    css_dict.append((j, i[1]))

            css_dict.append((i[0], i[1]))

        elif ' ' in i[0]:

            split_combinator = i[0].split()

            for j in split_combinator:
                if j == '>' or j == '+' or j == '~' or j == "*":
                    pass
                elif p.search(j):
                    dot_split = re.split('(\.\w+(-|\w)+)(\.\w+(-|\w)+)', j)

                    for s in dot_split:
                        if s == '' or len(s) <= 1:
                            pass
                        else:
                            css_dict.append((s, i[1]))
                else:
                    css_dict.append((j, i[1]))

        else:
            css_dict.append((i[0], i[1]))

    return css_dict

def split_pseudo(l, sheet):
    css_dict = []

    for i in l:
        if ':' in i[0]:
            split_pseudo = i[0].split(':')

            if '[' not in split_pseudo[0]:
                css_dict.append((split_pseudo[0], i[1]))
            else:
                attribute_selector = split_pseudo[0].split('[')
                css_dict.append((attribute_selector[0], i[1]))

        else:
            css_dict.append((i[0], i[1]))

    return css_dict

def del_dupes(l):
    h = []

    for i in l:
        if i not in h:
            h.append(i)
    return h

def delete_selectors(sheet, parser):
    rules_to_delete_index = []
    rules_to_delete_text = [] 
    selectors_deleted = []
    ignore = ['body', 'div']

    for i in split_pseudo(split_combinator(css_parser(sheet), sheet), sheet):
        if i[0] not in del_dupes(parser.selectors) and i[0] not in ignore:
            if len(i[1][2]) > 1:
                rule_idx = i[1][1]

                for idx, data in enumerate(sheet.cssRules[rule_idx].selectorList):
                    if idx != len(sheet.cssRules[rule_idx].selectorList) - 1:
                        pass
                    else:
                        selectors_deleted.append(str(i[0]) + ' from ' + str(i[1][2].selectorText))
                        del sheet.cssRules[rule_idx].selectorList[idx]
            else:
                rules_to_delete_text.append(str(i[1][2].selectorText))
                rules_to_delete_index.append(i[1][1])

    return (rules_to_delete_index, selectors_deleted, rules_to_delete_text)

def delete_rules(rules, sheet, parser):
    rules = del_dupes(delete_selectors(sheet, parser)[0])

    rules.sort()
    rules.reverse()
    
    for i in rules:
        del sheet.cssRules[i]

    return sheet.cssText