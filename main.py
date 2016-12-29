#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-12-25 23:03:20
# @Author  : Xingfan Xia (xiax@carleton.edu)
# @Link    : http://xiax.tech
# @Version : $Id$

import os, re, time, urllib2, urllib, sys, requests
from cookielib import CookieJar
from lxml import html, etree
reload(sys) 
sys.setdefaultencoding('utf-8')

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
	   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	   'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
	   'Accept-Encoding': 'none',
	   'Accept-Language': 'en-US,en;q=0.8',
	   'Connection': 'keep-alive'}

def torrent_lookup(key):
	global hdr
	count = 0
	tor_dict = dict()
	query = urllib.urlencode( {'q' : key } )
	url = "https://btso.pw/search/" + query[2:]
	req = urllib2.Request(url, headers=hdr)
	try:
		page = urllib2.urlopen(req)
	except urllib2.HTTPError, e:
		print e.fp.read()
	source = page.read()
	doc = html.fromstring(source)
	torrent_urls = doc.cssselect(".data-list>.row")
	for torrent in torrent_urls:
		try:
			title = torrent.cssselect("a")[0].attrib['title']
			addr = torrent.cssselect("a")[0].attrib['href']
			size = torrent.cssselect(".size")[0].text
			date = torrent.cssselect(".date")[0].text
			# hash_no = str(re.findall(r'hash\/(.+)', addr)[0])
			# print title, addr, size, date, hash_no
			count += 1
			data_ls = [title, size, date, addr]
			tor_dict[count] = data_ls
		except:
			pass
	return tor_dict

def retrieve_mag(url):
	global hdr
	req = urllib2.Request(url, headers=hdr)
	try:
		page = urllib2.urlopen(req)
	except urllib2.HTTPError, e:
		print e.fp.read()
	source = page.read()
	doc = html.fromstring(source)
	magnet = doc.cssselect("#magnetLink")[0].text
	return magnet

if __name__ == '__main__':
	query = str(raw_ input("Please enter search keyword: \n"))
	result = torrent_lookup(query)
	print "Here is a List of the Movies:"
	print "================================================="	
	for i in range(1, len(result)+1):
		print "Movie {num}:".format(num=i)
		for items in result[i]:
			print items
		print "***********************************************"

	choice = int(input("Please enter your Choice: \n"))
	tor_link = result[choice][3]
	print retrieve_mag(tor_link)