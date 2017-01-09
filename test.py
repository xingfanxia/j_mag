import urllib2
def req(url):
    proxy_support = urllib2.ProxyHandler({"http" : "127.0.0.1:8118"})
    opener = urllib2.build_opener(proxy_support) 
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    return opener.open(url).read()

print req('http://google.com')