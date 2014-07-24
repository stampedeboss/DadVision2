# -*- coding: UTF-8 -*-
'''
	Initialization Routine for common

	Routine is call on any import of a module in the library

'''
from common.settings import Settings
from common.cmdoptions import CmdOptions
import sys

__pgmname__ = 'getnew.__init__'
__version__ = '@version: $Rev: 231 $'

__author__ = "@author: AJ Reynolds"
__copyright__ = "@copyright: Copyright 2011, AJ Reynolds"
__license__ = "@license: GPL"

__maintainer__ = "@organization: AJ Reynolds"
__status__ = "@status: Development"
__credits__ = []


class Common(object):
	settings = Settings()
	options = CmdOptions()
	args = {}

	def __init__(self):
		pass