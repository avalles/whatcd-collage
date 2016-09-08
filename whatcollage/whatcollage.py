#!/usr/bin/env python
import sys
import requests
import itertools
from random import shuffle
from StringIO import StringIO
from PIL import Image

class WhatCollage:
	def __init__(self, username, password):
		"""
		Set the username and password, and start
		the requests session since we want to use
		the same credentials.
		"""
		self.session = requests.Session()
		self.username = username
		self.password = password
		self.authkey = None
		self.passkey = None
		try:
			self.login()
		except Exception:
			print "Couldn't login...Check user and password"
			sys.exit()

	def auth(self):
		"""
		Gets authorization key from the server.
		"""
		accountinfo = self.request("index")
		self.authkey = accountinfo["response"]["authkey"]
		self.passkey = accountinfo["response"]["passkey"]

	def login(self):
		"""
		Performs login using the username and password 
		that are provided.
		"""
		page = 'https://what.cd/login.php'
		data = {'username': self.username,
				'password': self.password
		}
		try:
			r = self.session.post(page, data = data, allow_redirects = False)
		except Exception as e:
			print e
		self.auth()

	def logout(self):
		"""
		Properly log out user.
		"""
		logoutpage = 'https://ssl.what.cd/logout.php'
		params = {'auth': self.authkey}
		self.session.get(logoutpage, allow_redirects = False)

	def request(self, action, id = None):
		"""
		Makes the proper request.
		"""
		ajaxpage = 'https://ssl.what.cd/ajax.php'
		params = {'action': action, 'id': id}
		if self.authkey:
			params['auth'] = self.authkey
		if id:
			params['id'] = id
		r = self.session.get(ajaxpage, params = params, allow_redirects = False)
		response = r.json()
		return response

	def collage(self, id, size, random = False, thumbnail = None, fname = None):
		"""
		Get the collage images, and paste them together.
		If an image link is broken, it skips that particular release.
		"""
		collages = self.request("collage", id)
		wikiImages = [i['wikiImage'] for i in collages['response']['torrentgroups']]
		if random == True:
			shuffle(wikiImages)
		if not thumbnail:
			thumbnail = 100
		elif thumbnail % 100 != 0 or thumbnail > 300 or thumbnail <= 0:
			print "The thumbnail size should be a multiple of 100, and should not exceed 300 pixels."
			return
		if not fname:
			fname = 'collage.png'
		new_collage = Image.new('RGB', size)
		progress = itertools.cycle(['/', '-', '\\', '|'])
		x = 0
		for j in range(0, size[1], thumbnail):
			for i in range(0, size[0], thumbnail):
				sys.stdout.write("Building collage " + next(progress) + '\r')
				sys.stdout.flush()
				try:
					r = requests.get(wikiImages[x])
					image = Image.open(StringIO(r.content))
				except requests.exceptions.RequestException:
					x = (x + 1) % len(wikiImages)
					continue
				except IOError:
					x = (x + 1) % len(wikiImages)
					continue
				image.thumbnail((thumbnail,thumbnail), Image.LANCZOS)
				new_collage.paste(image, (i,j))
				x = (x + 1) % len(wikiImages)
		new_collage.save(fname)