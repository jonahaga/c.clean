import cssutils
import urllib


# Parse css and get a list of rules
# css = u'''
# body { font-family: serif; }
# div.header , div.content, div.footer { padding: 0; margin: 0; }'''
opener = urllib.FancyURLopener({})
f = opener.open('/Users/Jona/Dropbox/Python/Hackbright/Project/dev/test_files/test3.css')
css = f.read()
f.close()


sheet = cssutils.parseString(css)
# ruleList = sheet.cssRules

# Let's remove a rule!
print "sheet.cssRules: ", len(sheet.cssRules)
sheet.deleteRule(0)
# del sheet.cssRules[0]
print "sheet.cssRules: ", len(sheet.cssRules)


# divRule = sheet.cssRules[0]
print "\nsheet.cssRules[0]: ", sheet.cssRules[0]

# selectors = sheet.cssRules[0].selectorList

# Let's remove a selector!
print "\n\nsheet.cssRules[0].selectorList: ", sheet.cssRules[0].selectorList
del sheet.cssRules[0].selectorList[1]
print "\nsheet.cssRules[0].selectorList: ", sheet.cssRules[0].selectorList

print "\n\nselector.element", sheet.cssRules[0].selectorList[0].element


print "\n\nsheet:\n", sheet.cssText