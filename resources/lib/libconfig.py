# -*- coding: utf-8 -*-
# Copyright (C) 2015 enen92
#
# This program is free software; you can redistribute it and/or modify it under the terms 
# of the GNU General Public License as published by the Free Software Foundation; 
# either version 2 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; 
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program; 
# if not, see <http://www.gnu.org/licenses/>.

import xbmc,xbmcgui,xbmcaddon,xbmcplugin
import urllib,re,os,sys
import thesportsdb
from centerutils.common_variables import *
from centerutils.iofile import *

dialog = xbmcgui.Dialog()

def start(data_list):
	window = dialog_libconfig('DialogLibConfig.xml',addonpath,'Default',str(data_list))
	window.doModal()
	
class dialog_libconfig(xbmcgui.WindowXMLDialog):
	def __init__( self, *args, **kwargs ):
		xbmcgui.WindowXML.__init__(self)
		self.sport = urllib.quote(eval(args[3])[0]).lower()
		self.sport_img = os.path.join(addonpath,art,self.sport.lower() + '.png')
		
		self.options = ['leagues/seasons(or year)/events','season(or year)/leagues/events','All events on the same folder']
		
		#define configuration files for sport library
		if self.sport == 'soccer' or self.sport == 'football': self.lib_config_file = football_library
		elif self.sport == 'rugby': self.lib_config_file = rugby_library
		elif self.sport == 'motorsport': self.lib_config_file = motorsport_library
		elif self.sport == 'basketball': self.lib_config_file = basketball_library
		elif self.sport == 'american%20football': self.lib_config_file = amfootball_library
		elif self.sport == 'ice%20hockey': self.lib_config_file = icehockey_library
		elif self.sport == 'baseball': self.lib_config_file = baseball_library
		elif self.sport == 'golf': self.lib_config_file = golf_library

	def onInit(self):
		self.getControl(2).setLabel(self.sport.replace('%2520',' '))
		self.getControl(3).setImage(self.sport_img)
		self.setInfo()
		
	def setInfo(self,):
		if os.path.isfile(self.lib_config_file):
			info = eval(readfile(self.lib_config_file))
			self.getControl(13).setLabel(self.options[int(info['mode'])])
			self.getControl(15).setLabel(info['folder'])
		return
			
	def onClick(self,controlId):
	
		if controlId == 10:
			choose = xbmcgui.Dialog().select('',self.options)
			if choose > -1:
				self.getControl(13).setLabel(self.options[choose])
				
		elif controlId == 11:
			pasta = dialog.browse(0, 'Select your main folder', 'myprograms')
			if pasta:
				self.getControl(15).setLabel(pasta)
	
		elif controlId == 9025:
			self.mode_label = self.getControl(13).getLabel()
			if self.mode_label:
				for i in xrange(0,len(self.options)-1):
					if self.options[i] == self.mode_label: self.mode = i
					else: pass
			else:
				mensagemok('SportsCenter','Please define a library organization method and try again!')
				sys.exit(0)
			self.libfolder = self.getControl(15).getLabel()
			if not self.libfolder:
				mensagemok('SportsCenter','Please define a library folder and try again!')
				sys.exit(0)
			#save stuff
			info = { 'mode':str(self.mode),'folder':self.libfolder }
			save(self.lib_config_file,str(info))
			xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Sports Center', 'Info saved!', 1,os.path.join(addonpath,"icon.png")))

			

	
		
