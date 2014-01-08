import json

class Configuration():
	"""This class reads and writes the files configurations .json
		for example: ratings of levels, language, etcetera
	"""
	def __init__(self):
		pass

	def open_json(self, file_):
		_file = open(file_)
		_json = json.load(_file)
		_file.close()

		return _json
		
	def configuration_json(self):
		return self.open_json('configuration/configuration.json')

	def language_json(self):
		return self.open_json('configuration/language.json')

	def levels_rating_json(self):
		return self.open_json('configuration/levels_rating.json')

	def override_rating_json(self, data):
		_file  = open('configuration/levels_rating.json', 'w')
		json.dump(data, _file, sort_keys=True, indent=4)

	def level_name_json(self, language, continent, level):
		return self.open_json('configuration/levels_names.json')[language][continent][str(level)]
       