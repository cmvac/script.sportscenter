import xbmc,xbmcgui,xbmcaddon,xbmcplugin
import urllib,re,os
import thesportsdb
from centerutils.common_variables import *
from centerutils.iofile import *
import competlist as competlist
import teamview

def start(data_list):
	window = dialog_context('DialogContext.xml',addonpath,'Default',str(data_list))
	window.doModal()
	
class dialog_context(xbmcgui.WindowXMLDialog):
	def __init__( self, *args, **kwargs ):
		xbmcgui.WindowXML.__init__(self)
		self.mode = eval(args[3])[0]
		self.specific_id = eval(args[3])[1]
		print self.mode,self.specific_id

	def onInit(self):
		#different menu items list goes here
		if self.mode == 'leaguelist':
			menu_items = [('Ignore League','ignoreleague')]
			fav_leagues = os.listdir(favleaguesfolder)
			if (self.specific_id + '.txt') not in fav_leagues:
				menu_items.append(('Add league to Favourites','addleaguefavourite'))
			else:
				menu_items.append(('Remove league from Favourites','rmleaguefavourite'))
			ign_calendar = os.listdir(ignoreleaguecalendar)
			if (self.specific_id + '.txt') in ign_calendar:
				menu_items.append(('Add to calendar','addleaguecalendar'))
			else:
				menu_items.append(('Remove from calendar','rmleaguecalendar'))
			ign_livescores = os.listdir(ignoreleaguelivescores)
			if (self.specific_id + '.txt') in ign_livescores:
				menu_items.append(('Add to livescores listing','addleaguelivescores'))
			else:
				menu_items.append(('Remove from livescores listing','rmleaguelivescores'))
			menu_items.append(('Add to widgets','addtowidgets'))
		elif self.mode == 'calendaritem':
			menu_items = []
			self.event_dict = thesportsdb.Lookups().lookupevent(self.specific_id)["events"][0]
			if not thesportsdb.Events().get_racelocation(self.event_dict):
				menu_items.append(('View home team details','hometeamdetails'))
				menu_items.append(('Navigate to home team','hometeammain'))
				menu_items.append(('View away team details','awayteamdetails'))
				menu_items.append(('Navigate to away team','awayteammain'))
			menu_items.append(('Ignore competition from calendar','rmleaguecalendar'))
			
		
		#set menu dimensions according to the number of menu items
		totalitems = len(menu_items)
		print "total",totalitems
		if totalitems > 1:
		#	#get dimensions of controlID 994 and 995, increment by 30px * nb of items
			height_background = self.getControl(994).getHeight()
			y_background = self.getControl(994).getY()
			x_background = self.getControl(994).getX()
			height_container = self.getControl(995).getHeight()
			y_container = self.getControl(995).getY()
			x_container = self.getControl(995).getX()
			x_panel = self.getControl(996).getX()
			y_panel = self.getControl(996).getY()
			self.getControl(994).setHeight(height_background + 2*30*(totalitems-1))
			self.getControl(995).setHeight(height_container + 2*30*(totalitems-1))
			self.getControl(994).setPosition(x_background,y_background - 2*30*(totalitems-1))
			self.getControl(995).setPosition(x_container,y_container - 2*30*(totalitems-1))
			self.getControl(996).setPosition(x_panel,y_panel - 2*30*(totalitems-1))

		for itemlabel,itemident in menu_items:
			submenuitem = xbmcgui.ListItem(itemlabel)
			submenuitem.setProperty('identifier',itemident)
			self.getControl(996).addItem(submenuitem)
			
			
		#xbmc.sleep(200)
		self.setFocusId(996)
		self.getControl(996).selectItem(0)
			
	def onClick(self,controlId):

		if controlId == 996:
			self.identifier = self.getControl(996).getSelectedItem().getProperty('identifier')
			if self.identifier == 'ignoreleague':
				self.close()
				ignore_league(self.specific_id)
			
			elif self.identifier == 'addleaguefavourite':
				self.close()
				add_leaguetofavs(self.specific_id)
			
			elif self.identifier == 'rmleaguefavourite':
				self.close()
				rm_leaguefrmfavs(self.specific_id)
				
			elif self.identifier == 'rmleaguecalendar':
				self.close()
				rm_leaguecalendar(self.specific_id)
				
			elif self.identifier == 'addleaguecalendar':
				self.close()
				add_leaguecalendar(self.specific_id)
				
			elif self.identifier == 'rmleaguelivescores':
				self.close()
				rm_leaguelivescores(self.specific_id)
				
			elif self.identifier == 'addleaguelivescores':
				self.close()
				add_leaguelivescores(self.specific_id)
				
			elif self.identifier == 'hometeamdetails':
				self.team_id = thesportsdb.Events().get_hometeamid(self.event_dict)
				teamview.teamdetails(self.team_id)
				
			elif self.identifier == 'awayteamdetails':
				self.team_id = thesportsdb.Events().get_awayteamid(self.event_dict)
				teamview.teamdetails(self.team_id)
				
			elif self.identifier == 'hometeammain':
				self.close()
				self.team_id = thesportsdb.Events().get_hometeamid(self.event_dict)
				self.sport = thesportsdb.Events().get_sport(self.event_dict)
				teamview.start([self.team_id,self.sport,'',''])
				
				
			elif self.identifier == 'awayteammain':
				self.close()
				self.team_id = thesportsdb.Events().get_awayteamid(self.event_dict)
				self.sport = thesportsdb.Events().get_sport(self.event_dict)
				teamview.start([self.team_id,self.sport,'',''])
			
			
						
# Specific functions called by context menu go here	
#TO-DO threads are needed to restart stuff

def ignore_league(league_id):
	ficheiro = os.path.join(ignoredleaguesfolder,str(league_id)+'.txt')
	save(ficheiro,'')
	xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Sports Center', 'League has been ignored!', 1,os.path.join(addonpath,"icon.png")))
	
def add_leaguetofavs(league_id):
	ficheiro = os.path.join(favleaguesfolder,str(league_id)+'.txt')
	save(ficheiro,'')
	xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Sports Center', 'League added to favourites!', 1,os.path.join(addonpath,"icon.png")))
	
def rm_leaguefrmfavs(league_id):
	ficheiro = os.path.join(favleaguesfolder,str(league_id)+'.txt')
	os.remove(ficheiro)
	xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Sports Center', 'League removed from favourites!', 1,os.path.join(addonpath,"icon.png")))
	
def rm_leaguecalendar(league_id):
	ficheiro = os.path.join(ignoreleaguecalendar,str(league_id)+'.txt')
	save(ficheiro,'')
	xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Sports Center', 'League removed from calendar!', 1,os.path.join(addonpath,"icon.png")))
	
def add_leaguecalendar(league_id):
	ficheiro = os.path.join(ignoreleaguecalendar,str(league_id)+'.txt')
	os.remove(ficheiro)
	xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Sports Center', 'League added back to calendar!', 1,os.path.join(addonpath,"icon.png")))
	
def rm_leaguelivescores(league_id):
	ficheiro = os.path.join(ignoreleaguecalendar,str(league_id)+'.txt')
	save(ficheiro,'')
	xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Sports Center', 'League removed from livescores!', 1,os.path.join(addonpath,"icon.png")))
	
def add_leaguelivescores(league_id):
	ficheiro = os.path.join(ignoreleaguecalendar,str(league_id)+'.txt')
	os.remove(ficheiro)
	xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Sports Center', 'League added back to livescores!', 1,os.path.join(addonpath,"icon.png")))

	
	
	

