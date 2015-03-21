#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Author: AJ Reynolds
Date: 03-19-2015
Purpose:
Base API for TRAKT, provides common routines.
"""
from __future__ import division
from urllib2 import Request, urlopen, HTTPError
import logging
import json
import sys


__pgmname__ = 'trakt'
__version__ = '@version: $Rev$'

__author__ = "@author: AJ Reynolds"
__copyright__ = "@copyright: Copyright 2015, AJ Reynolds"
__status__ = "@status: Development"
__license__ = "@license: GPL"

__maintainer__ = "@organization: AJ Reynolds"
__credits__ = []

log = logging.getLogger(__pgmname__)

client_id = '54d65f67401b045bc720ef109d4d05a107c0f5e28badf2f413f89f9bee514ae7'
client_secret = '85f06b5b6d29265a8be4fa113bbaefb0dd58826cbfd4b85da9a709459a0cb9b1'
authorization = 'Bearer 23ce6843ef4296053b117ec9e37f4dc9b124cc4ed05c50556812014cc17effa6'
userid = 'stampedeboss'


def getBase(url, userid=userid, authorization=authorization, rtn=dict):

	from library.series import Series
	from library.movie import Movie

	headers = {
	  'Content-Type': 'application/json',
	  'trakt-api-version': '2',
	  'trakt-api-key': client_id,
	  'Authorization': authorization
	}

	request = Request(url, headers=headers)
	try:
		response_body = urlopen(request).read()
	except HTTPError, e:
#		an_error = traceback.format_exc()
#		log.error(traceback.format_exception_only(type(an_error), an_error)[-1])
		return e

	data = json.loads(response_body.decode('UTF-8', 'ignore'))

	if rtn is dict:
		_list = {}
	else:
		_list = []

	for entry in data:
		if 'type' in entry:
			if entry['type'] == u'show':
				_object = Series(**entry)
			elif entry['type'] == u'movie':
				_object = Movie(**entry)
			else:
				sys.exit(99)

		if 'show' in entry:
			_object = Series(**entry)
		elif 'movie' in entry:
			_object = Movie(**entry['movie'])
		else:
			_object = Series(**data)
			if rtn is dict:
				_list[_object.title] = _object
			else:
				_list.append(_object)

			return _list

		if rtn is dict:
			_list[_object.title] = _object
		else:
			_list.append(_object)

	return _list

def postBase(_url, userid=userid, authorization=authorization, entries=None):

	from library.series import Series

	if entries is None:
		return 'No Data'

	_list = {'shows': [], 'movies': []}
	for entry in entries:
		if hasattr(entry, 'ids'):
			show_entry = entry.ids
		else:
			show_entry = {}
			if hasattr(entry, entry.imdb_id):
				show_entry['imdb'] = entry.imdb_id
			if hasattr(entry, entry.tmdb_id):
				show_entry['tmdb'] = entry.tmdb_id
			if hasattr(entry, entry.trakt_id):
				show_entry['trakt'] = entry.trakt_id

		if type(entry) is Series:
			_list['shows'].append({'ids': show_entry})
		else:
			_list['movies'].append({'ids': entry.ids})

	if len(_list['shows']) == 0:
		del _list['shows']

	if len(_list['movies']) == 0:
		del _list['movies']

	json_data = json.dumps(_list)
	clen = len(json_data)

	headers = {
				'Content-Type': 'application/json',
				'trakt-api-version': '2',
				'trakt-api-key': client_id,
				'Authorization': authorization,
				'Content-Length': clen
			}

	request = Request(_url, data=json_data, headers=headers)
	response_body = urlopen(request).read()
	data = json.loads(response_body.decode('UTF-8', 'ignore'))

	return data

def modifyBase(url, userid=userid, authorization=authorization, entries=None, entrytype=None):

	from library.series import Series
	from library.movie import Movie

	if entries is None:
		return 'No Data'

	if entrytype is None:
		entrytype = type(entries[0])
		if entrytype == Movie:
			entrytype = 'movies'
		elif entrytype == Series:
			entrytype = 'shows'

	_list = []
	for entry in entries:
		if hasattr(entry, 'ids'):
			_list.append({'ids': entry.ids})
		else:
			show_entry = {}
			if entry.imdb_id:
				show_entry['imdb'] = entry.imdb_id
			if entry.tmdb_id:
				show_entry['tmdb'] = entry.tmdb_id
			if entry.tvdb_id:
				show_entry['tvdb'] = entry.tvdb_id
			if entry.tvrage_id:
				show_entry['tvrage'] = entry.tvrage_id
			_list.append({'ids': show_entry})

	if entrytype == 'shows':
		json_data = json.dumps({'shows': _list})
	else:
		json_data = json.dumps({'movies': _list})

	clen = len(json_data)

	headers = {
				'Content-Type': 'application/json',
				'trakt-api-version': '2',
				'trakt-api-key': client_id,
				'Authorization': authorization,
				'Content-Length': clen
			}

	request = Request(url, data=json_data, headers=headers)
	response_body = urlopen(request).read()
	data = json.loads(response_body.decode('UTF-8', 'ignore'))

	return data