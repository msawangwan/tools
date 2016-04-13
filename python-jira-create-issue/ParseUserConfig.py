import ConfigParser

class UserConfigParser(object):
	''' 
		Parses an associated .ini file 
	
		This script expects the sections:
		'user', 'fields', 'ios', 'android', and 'template' 
		 -- this module has not been tested to handle NULL values!
		 
		 Note that: (0 = 'iOS') and (1 = 'Android')
		 
		 TODO: Implement exception handling ...
	'''

	def __init__(self, config_ini):                      # config_ini = filename
		self.CONFIG      = ConfigParser.ConfigParser()   # from the python stdlib
		self.CONFIG_FILE = config_ini                    # expected config.ini file
		self.USER        = []                            # holds login (user/pw combo)
		self.FIELDS      = []                            # holds fields populated by ...
		self.iOS         = []                            # ... either ios device info ...
		self.ANDROID     = []                            # ... or droid device info ...
		self.TEMPLATE    = []                            # and a blank to multi-line description template
	
	def __get_values_as_list(self, config_section):
		value_list = []
		for config_value in self.CONFIG.options(config_section):
			value_list.append(self.CONFIG.get(config_section, config_value))
		return value_list
	
	def __format_header(self, platform_code=0):
		formatted_header = []
		if platform_code == 0:                           # platform_code of 0 is 'iOS'
			for field, value in zip(self.FIELDS, self.iOS):
				formatted_field = field.replace('_', ':')
				field_with_value = formatted_field.strip() + " " + value.strip()
				formatted_header.append(field_with_value)
		elif platform_code == 1:                         # platform_code of 1 is 'Android'
			for field, value in zip(self.FIELDS, self.ANDROID):
				formatted_field = field.replace('_', ':')
				field_with_value = formatted_field.strip() + " " + value.strip()
				formatted_header.append(field_with_value)
		return formatted_header
	
	def __format_template(self):
		formatted_template = []
		for line in self.TEMPLATE:
			formatted_line = line.replace('_', ':').strip().replace('%', '\n')
			formatted_template.append(formatted_line )
		return formatted_template

	def parse_config_data(self):
		self.CONFIG.read(self.CONFIG_FILE)
		for section in self.CONFIG.sections():
			if section == 'user':
				self.USER = self.__get_values_as_list(section)
			elif section == 'fields':
				self.FIELDS = self.__get_values_as_list(section)
			elif section == 'ios':
				self.iOS = self.__get_values_as_list(section)
			elif section == 'android':
				self.ANDROID = self.__get_values_as_list(section)
			elif section == 'template':
				self.TEMPLATE = self.__get_values_as_list(section)

	def create_template(self, platform_code=0):		
		if platform_code == 0:                           # platform_code of 0 is 'iOS'
			header_as_list = self.__format_header(0)
		elif platform_code == 1:                         # platform_code of 1 is 'Android'
			header_as_list = self.__format_header(1)
		template_as_list = self.__format_template()

		template = header_as_list + template_as_list
		
		formatted_template_str = ""
		for line in template:
			formatted_template_str += line + "\n"

		return formatted_template_str

if __name__ == '__main__':
	''' Example usage '''
	print "[TEST INSTANCE] ... Creating a test instance of UserConfigParser ... "

	test_config_file = "userconfig.ini"                  # define the config file
	test_instance = UserConfigParser(test_config_file)   # create a config parser object
	test_instance.parse_config_data()                    # parse the file
	test_template = test_instance.create_template(1)     # create a template out of the parsed data
	
	print "[TEST INSTANCE] ... Printing Test Instance Template ... "
	print test_template