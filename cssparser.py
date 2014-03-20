import cssutils
import urllib
import re
# from cssutils import css, stylesheets


# def main():
#     f = open('/Users/Jona/Dropbox/Python/Hackbright/Project/test2.css', 'r')
#     c = f.read()
#     f.close()

#     css_file = cssutils.CSSParser().parseString(c)

#     for i in css_file.cssRules:
        
#         if not isinstance(i, cssutils.css.CSSComment) and not isinstance(i, cssutils.css.CSSImportRule):
#             for j in i.selectorList:
#                 print j.selectorText,'\n\t', i.selectorList

# if __name__ == '__main__':
#     main()
opener = urllib.FancyURLopener({})
f = opener.open('/Users/Jona/Dropbox/Python/Hackbright/Project/test_files/test3.css')
c = f.read()
f.close()

css_file = cssutils.CSSParser().parseString(c)


def css_parser(files_to_parse):
    css_dict = {}

    for i in css_file.cssRules:
        if not isinstance(i, cssutils.css.CSSComment) and not isinstance(i, cssutils.css.CSSImportRule):
            for j in i.selectorList:
                print j
                p = re.compile('\.\w*(\.)\w*')

                if p.match(str(j.selectorText)) and ' ' not in j.selectorText:
                    dot_combinator = re.split(('(\.\w*)(\.\w*)', str(j.selectorText)))
                    
                    for m in dot_combinator:
                        if m == '':
                            pass
                        else:
                            css_dict.update({m:j})

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
                                    css_dict.update({s:j})
                        else:
                            css_dict.update({k:j})               
                
                elif '*' in j.selectorText:
                    pass
                else:
                    css_dict.update({str(j.selectorText):j})

    # return css_dict

print css_parser(css_file)

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

# print split_pseudo(css_parser(css_file))

def del_dupes(d):
    n = {}

    for key in d:
        if key not in n:
            n.update({key: d.get(key)})
    
    return n

# print del_dupes(split_pseudo(css_parser(css_file)))

def delete_unused(d):
    styles_to_delete = []

    for key in css_parser(css_file):
        if key == 'h5':
            styles_to_delete.append(css_parser(css_file).get(key))

    return styles_to_delete


print '\n\n',delete_unused(css_parser(css_file))