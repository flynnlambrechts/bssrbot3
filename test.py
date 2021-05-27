import hyperlink

url = hyperlink.parse(u'http://github.com/python-hyper/hyperlink?utm_source=readthedocs')

better_url = url.replace(scheme=u'https', port=443)
org_url = better_url.click(u'.')

print(org_url.to_text())
# prints: https://github.com/python-hyper/

print(better_url.get(u'utm_source')[0])
# prints: readthedocs
