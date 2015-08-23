#!/usr/local/bin/python

'''
+ exception handling is not done as it must be.
+ doctypes are not written.
+ constants are not stored as global variables.
'''

import urllib2
import sys
from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint

url = 'https://en.wikipedia.org/wiki/'

def giveStopWords():
	stopWords = []
	try:
		myFile = open('terrier-stop.txt', 'r')
	except(IOError):
		print 'The file does not exist'
	else:
		word = myFile.readline()
		while(word != ''):
			if word[-1] == '\n':
				word = word[:-1]
			if word[-1] == '\r':
				word = word[:-1]
			if word[0] != '#':	
				stopWords.append(word)
			word = myFile.readline()
		myFile.close()

	try:
		myFile = open('myWords.txt', 'r')
	except(IOError):
		print 'The file does not exist'
	else:
		word = myFile.readline()
		while(word != ''):
			if word[-1] == '\n':
				word = word[:-1]
			if word[-1] == '\r':
				word = word[:-1]
			if word[0] != '#':	
				stopWords.append(word)
			word = myFile.readline()
		myFile.close()

	return stopWords

def giveWordsFrequencies(word, stopWords):
	'''
	Returns a sorted list containg the words and their frequencies in the wikipedia page.
	input: str to be searched on Wikipedia.

	word: (str) a word to start with
	stopWords: (list) list of stop words

	return: a sorted list of tuples containing a word and its frequency.
	'''
	giveWordsFrequencies.phrase = ''
	class myHTMLParser(HTMLParser):
		pFlag = False
		def handle_starttag(self, tag, attrs):
			if tag == 'p':
				self.pFlag = True
		def handle_endtag(self, tag):
			if tag == 'p':
				self.pFlag = False
		def handle_data(self, data):
			global phrase
			if self.pFlag:
				giveWordsFrequencies.phrase += data

	try:
		myHTMLParser().feed(urllib2.urlopen(url + str(word)).read())
	except(UnicodeDecodeError):
		pass

	words = []
	for word in giveWordsFrequencies.phrase.split(' '):
		if len(word) > 0:
			if word[-1] == '.' or word[-1] == ',' or word[-1] == ')' or word[-1] == "'" or word[-1] == '"' or word[-1] == ':':
				word = word[:-1]
		if len(word) > 0:
			if word[0] == '(' or word[0] == "'" or word[0] == '"':
				word = word[1:]
		if len(word) > 0:
			if word[-2:] == 's':
				word = word[:-2]
			word = word.lower()
		if len(word) > 0:
			if (not any((letter in '1234567890-') for letter in word)) and (word not in stopWords) and bool(len(word)):
				words.append(word.lower())
	myDict = {}
	for word in words:
		if word in myDict:
			myDict[word] += 1
		else:
			myDict[word] = 1
	myList = list(tuple([word, freq]) for word, freq in myDict.items())
	myList.sort(key = lambda wordTuple: wordTuple[1], reverse = True)
	return myList

def crawl(word, num):
	crawl.crawled.append(word)
	if num != 0:
		myList = giveWordsFrequencies(word, crawl.stopWords)[:100]
		for word, freq in myList:
			if word not in crawl.crawled:
				print str(num) + ': ' + word + ' : ' + str(freq)
				try:
					crawl(word, num - 1)
				except(urllib2.HTTPError):
					continue
				break
			

if __name__ == '__main__':
	crawl.crawled = []
	crawl.stopWords = giveStopWords()
	crawl(sys.argv[1], int(sys.argv[2]))
