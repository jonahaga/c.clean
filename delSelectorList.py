import cssutils
import urllib


# Parse css and get a list of rules
# css = u'''
# body { font-family: serif; }
# div.header , div.content, div.footer { padding: 0; margin: 0; }'''
opener = urllib.FancyURLopener({})
f = opener.open('/Users/Jona/Dropbox/Python/Hackbright/Project/test_files/test3.css')
css = f.read()
f.close()


sheet = cssutils.parseString(css)
ruleList = sheet.cssRules

# Let's remove a rule!
print "ruleList: ", len(ruleList)
sheet.deleteRule(0)
print "ruleList: ", len(ruleList)


divRule = ruleList[0]
print "divRule: ", divRule

selectors = divRule.selectorList

# Let's remove a selector!
print "selectors: ", selectors
del selectors[1]
print "selectors: ", selectors

print "selector.element", selectors[0].element


print "sheet:\n", sheet.cssText