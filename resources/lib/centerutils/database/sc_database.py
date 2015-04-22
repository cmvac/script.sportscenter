# -*- coding: utf-8 -*-
import thesportsdb
import sqlite3 as lite
import os
#command line use only!
sc_database = 'sc_database.db'
templatefolder =  os.path.join(os.path.dirname(os.path.abspath(__file__)),'templates')

class Creator:
	#variables
	def __init__(self,):
		self.team_template = os.path.join(templatefolder,'team.txt')
		self.league_template = os.path.join(templatefolder,'league.txt')
		self.event_template = os.path.join(templatefolder,'event.txt')
		return

	#all
	def create_table_all(self,):
		self.create_table_league()
		self.create_table_team()
		self.create_table_event()
		return
	
	def drop_and_create_table_all(self,):
		self.drop_and_create_table_league()
		self.drop_and_create_table_team()
		self.drop_and_create_table_event()
		return
	
	#league
	def create_table_league(self,):
		con = lite.connect(sc_database)
		lines = []
		with open(self.league_template) as f:
			lines = f.readlines()
		query_string = ''
		for line in lines:
			query_string = query_string + line
		cur = con.cursor() 
		cur.execute("CREATE TABLE League("+query_string+")")
		if con:
			print "SportsCenter: Table League created successfully!"
			con.close()
		return
	
	def drop_table_league(self,):
		con = lite.connect(sc_database)
		cur = con.cursor()
		cur.execute("DROP TABLE IF EXISTS League")
		if con:
			print "SportsCenter: Table League dropped successfully!"
			con.close()
		return
		
		
	def drop_and_create_table_league(self,):
		self.drop_table_league()
		self.create_table_league()
		return
		
	#team
	def create_table_team(self,):
		con = lite.connect(sc_database)
		lines = []
		with open(self.team_template) as f:
			lines = f.readlines()
		query_string = ''
		for line in lines:
			query_string = query_string + line
		cur = con.cursor() 
		cur.execute("CREATE TABLE Team("+query_string+")")
		if con:
			print "SportsCenter: Table Team created successfully!"
			con.close()
		return
	
	def drop_table_team(self,):
		con = lite.connect(sc_database)
		cur = con.cursor()
		cur.execute("DROP TABLE IF EXISTS Team")
		if con:
			print "SportsCenter: Table Team dropped successfully!"
			con.close()
		return
		
	def drop_and_create_table_team(self,):
		self.drop_table_team()
		self.create_table_team()
		return
		
	#event
	def create_table_event(self,):
		con = lite.connect(sc_database)
		lines = []
		with open(self.event_template) as f:
			lines = f.readlines()
		query_string = ''
		for line in lines:
			query_string = query_string + line
		cur = con.cursor() 
		cur.execute("CREATE TABLE Event("+query_string+")")
		if con:
			print "SportsCenter: Table Event created successfully!"
			con.close()
		return
		
	def drop_table_event(self,):
		con = lite.connect(sc_database)
		cur = con.cursor()
		cur.execute("DROP TABLE IF EXISTS Event")
		if con:
			print "SportsCenter: Table Event dropped successfully!"
			con.close()
		return
		
	def drop_and_create_table_event(self,):
		self.drop_table_event()
		self.create_table_event()
		return
		
class Checker:
	def check_if_table_exists(self,table):
		con = lite.connect(sc_database)
		cur = con.cursor()		
		try:
			cur.execute("SELECT * FROM "+table)
			con.close()
			return True
		except: 
			con.close()
			return False

		
	def create_table_if_not_exists(self,table):
		if table == 'League': pass
		elif table == 'Team': pass
		elif table == 'Event': pass
		else: return
		check = self.check_if_table_exists(table)
		if not check:
			if table == 'League': Creator().create_table_league()
			elif table == 'Team': Creator().create_table_team()
			elif table == 'Event': Creator().create_table_event()
		return


class Inserter:
	def __init__(self,):
		pass
		
	def global_inserter(self,table,dictionary):
		con = lite.connect(sc_database)
		cur = con.cursor()
		cur.execute('select * from '+table)
		colums = list(map(lambda x: x[0], cur.description))
		totalcolums = len(colums)
		totalitems = len(cur.fetchall())
		next = totalitems + 1
		key_array = '('
		key_array_add = ''
		i=0
		for key in colums:
			if i != (totalcolums-1): key_array_add  = key_array_add + key.replace('"','').replace("'","") + ','
			else: key_array_add  = key_array_add + key.replace('"','').replace("'","") + ')'
			i+=1
			
		key_array = key_array + key_array_add
		
		values_array_tmp = []
		for key in sorted(dictionary.keys()):
			if key in colums:
				if dictionary[key] == None or dictionary[key] == '': values_array_tmp.append('null')
				else: values_array_tmp.append(dictionary[key].replace('"','').replace("'",""))
		
		values_array = '('+str(next)+','
		i=0
		for key in values_array_tmp:
			if i != (len(values_array_tmp)-1): values_array = values_array + "'"+key +"'"+ ','
			else: values_array = values_array +"'"+ key +"'"+')'
			i+=1
				
		sql_string = "INSERT INTO "+table+" "+key_array+" VALUES "+values_array+";"
		cur.execute(sql_string)
		if con:
			con.commit()
			con.close()
			print "SportsCenter: added to " + table + "!"
		return	
		
		
	def insert_team(self,_team_id_or_dict_):
		if type(_team_id_or_dict_) == str:
			team_dictionary = thesportsdb.Lookups().lookupteam(_team_id_or_dict_)["teams"][0]
		elif type(_team_id_or_dict_) == dict: 
			team_dictionary = _team_id_or_dict_
		else: team_dictionary = None
		if team_dictionary:
			#here we check if the table exists if not we create it
			Checker().create_table_if_not_exists('Team')
			#send the dictionary to global inserter
			self.global_inserter('Team',team_dictionary)
		return
		
		
	def insert_league(self,_league_id_or_dict_):
		if type(_league_id_or_dict_) == str:
			league_dictionary = thesportsdb.Lookups().lookupleague(_league_id_or_dict_)["leagues"][0]
		elif type(_league_id_or_dict_) == dict: 
			league_dictionary = _league_id_or_dict_
		else: league_dictionary = None
		if league_dictionary:
			#here we check if the table exists if not we create it
			Checker().create_table_if_not_exists('League')
			#send the dictionary to global inserter
			self.global_inserter('League',league_dictionary)
		return
		
	def insert_event(self,_event_id_or_dict_):
		if type(_event_id_or_dict_) == str:
			event_dictionary = thesportsdb.Lookups().lookupevent(_event_id_or_dict_)["events"][0]
		elif type(_event_id_or_dict_) == dict: 
			event_dictionary = _event_id_or_dict_
		else: event_dictionary = None
		if event_dictionary:
			#here we check if the table exists if not we create it
			Checker().create_table_if_not_exists('Event')
			#send the dictionary to global inserter
			self.global_inserter('Event',event_dictionary)
		return
		
class Remover:
	def __init__(self,):
		pass
		
	def global_remover(self,table,db_key,sc_id):
		con = lite.connect(sc_database)
		cur = con.cursor()
		cur.execute("delete from "+table+" where "+db_key+" = '%s' " % sc_id)
		print "SportsCenter: "+db_key+" = "+sc_id+" removed from " + table +"!"
		if con:
			con.commit()
			con.close()
		return		
		
	def remove_team(self,_team_id_or_dict_):
		if type(_team_id_or_dict_) == str:
			sc_id = _team_id_or_dict_
		elif type(_event_id_or_dict_) == dict: 
			sc_id = thesportsdb.Teams().get_id(_team_id_or_dict_)
		else: sc_id = None
		if sc_id:
			self.global_remover('Team','idTeam',sc_id)
		return
		
	def remove_league(self,_league_id_or_dict_):
		if type(_league_id_or_dict_) == str:
			sc_id = _league_id_or_dict_
		elif type(_league_id_or_dict_) == dict: 
			sc_id = thesportsdb.Leagues().get_id(_league_id_or_dict_)
		else: sc_id = None
		if sc_id:
			self.global_remover('League','idLeague',sc_id)
		return
		
	def remove_event(self,_event_id_or_dict_):
		if type(_event_id_or_dict_) == str:
			sc_id = _event_id_or_dict_
		elif type(_event_id_or_dict_) == dict: 
			sc_id = thesportsdb.Events().get_eventid(_event_id_or_dict_)
		else: sc_id = None
		if sc_id:
			self.global_remover('Event','idEvent',sc_id)
		return
		
class Updater:
	def __init__(self,):
		pass
		
	def update_team(self,_team_id_or_dict_):
		Remover().remove_team(_team_id_or_dict_)
		Inserter().insert_team(_team_id_or_dict_)
		return
		
	def update_league(self,_league_id_or_dict_):
		Remover().remove_league(_league_id_or_dict_)
		Inserter().insert_league(_league_id_or_dict_)
		return
		
	def update_event(self,_event_id_or_dict_):
		Remover().remove_event(_event_id_or_dict_)
		Inserter().insert_event(_event_id_or_dict_)
		return
		
class Converter:
	def row_to_dict(self, table,tsdb_id_or_dict):
		pass
	
		
	
