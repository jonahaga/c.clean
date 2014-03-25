import cssutils
import re
from HTMLParser import HTMLParser
from urllib2 import urlopen


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
        f = urlopen(stripped)
        n = f.read()

        new_file += n

        f.close()

    return new_file

def css_parser(sheet):
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

def split_pseudo(d, sheet):
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

def delete_selectors(sheet, parser):
    rules_to_delete_index = []
    rules_to_delete_text = [] 
    selectors_deleted = []
    ignore = ['body', 'div']

    for key, value in del_dupes(split_pseudo(css_parser(sheet), sheet)).iteritems():
        if key not in del_dupes(parser.selectors) and key not in ignore:
            if len(value[2]) > 1:
                rule_idx = value[1]

                for idx, data in enumerate(sheet.cssRules[rule_idx].selectorList):
                    if idx != len(sheet.cssRules[rule_idx].selectorList) - 1:
                        pass
                    else:
                        selectors_deleted.append(str(key) + ' from ' + str(value[2].selectorText))
                        del sheet.cssRules[rule_idx].selectorList[idx]
            else:
                rules_to_delete_text.append(str(value[2].selectorText))
                rules_to_delete_index.append(value[1])

    return (rules_to_delete_index, selectors_deleted, rules_to_delete_text)

def delete_rules(rules, sheet, parser):
    rules = delete_selectors(sheet, parser)[0]

    rules.sort()
    rules.reverse()
    
    for i in rules:
        sheet.deleteRule(i)

    return sheet.cssText 