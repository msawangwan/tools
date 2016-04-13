from jira import JIRA
import webbrowser as wb
import ParseUserConfig as parseCFG

class JiraTicket(object):
	'''
		Create a ticket in the Jira DB, based on MFQA bug formatting.
		
		To be used with the 'ParseUserConfig.py' script and an
		associated 'userconfig.ini' file that contains the 
		template and formatting information.
		
		*Execution Flow*
		- Call parsing script on config file
		- Populate field values from config file
		- Create a new JIRA ticket in the DB
		- Opens ticket in a new browser tab for editing
		
		Has not been tested for NULL or UNKNOWN values!
		
		TODO: Implement exception handling ...
	'''

	def __init__(self, summary_text, platform=0):
		self.USER_CONFIG_FILE     = "userconfig.ini"                # config file, filepath is hardcoded
		self.USER_NAME            = ""
		self.USER_PW              = ""
		self.SUMMARY_TEMPLATE     = summary_text
		self.DESCRIPTION_TEMPLATE = ""
		self.PLATFORM_CODE        = platform
		self.JIRA_SERVER          = "http://your.jira.server:9000"
		self.JIRA_OPTIONS         = { 'server' : self.JIRA_SERVER }		
		self.PROJECT_KEY          = { 'key'  : 'your-project-key' }
		self.PROJECT_ID           = { 'id'   : 'your-project-id'  }
		self.ISSUE_TYPE           = { 'name' : 'Bug' }
		self.ISSUE_FIELDS         = {                }

	def __populate_fields(self):
		cfg = parseCFG.UserConfigParser(self.USER_CONFIG_FILE)
		cfg.parse_config_data()
		
		if self.PLATFORM_CODE == 0:                                 # platform_code of 0 is 'iOS'
			self.DESCRIPTION_TEMPLATE = cfg.create_template(0)
			print "[+] Using iOS template ... "
		elif self.PLATFORM_CODE == 1:                               # platform_code of 1 is 'Android'
			self.DESCRIPTION_TEMPLATE = cfg.create_template(1)
			print "[+] Using Android template ... "
		
		self.ISSUE_FIELDS = {                                       # define the required fields for the issue form
			'project'     : self.PROJECT_KEY,
			'summary'     : self.SUMMARY_TEMPLATE,
			'description' : self.DESCRIPTION_TEMPLATE,
			'issuetype'   : self.ISSUE_TYPE
		}
		
		if len(cfg.USER) > 0:
			self.USER_NAME = cfg.USER[0]
			self.USER_PW   = cfg.USER[1]
			print '[+] User:', self.USER_NAME
		
	def create_issue(self, blank_issue=False):
		self.__populate_fields()
		
		if blank_issue: 
			self.DESCRIPTION_TEMPLATE = ""
		
		jira = JIRA(options=self.JIRA_OPTIONS, basic_auth=(self.USER_NAME, self.USER_PW))  # jira-python API
		new_issue = jira.create_issue(fields=self.ISSUE_FIELDS)
		issue_url = self.JIRA_SERVER + "browse/" + new_issue.key
		wb.open_new_tab(issue_url)
		
		print '[+] Created a new ticket: ', self.SUMMARY_TEMPLATE
		print '[+] Issue:', new_issue.key
		print '---------------------------------------------------'
		print ' +++++++++++++++++++++++++++++++++++++++++++++++++ '
		print '---------------------------------------------------'
		print '[+] Template used:' 
		print self.DESCRIPTION_TEMPLATE
		
if __name__ == '__main__':
	''' Example Usage '''
	print "[TEST INSTANCE] ... Creating a test instance of JiraTicket ... "
	
	test_instance = JiraTicket('[TEST] test summary', 1)            # create a ticket object, pass in a summary and platform code
	test_instance.create_issue()                                    # create an issue -- pass True to create an empty issue, leave blank to use a platform specific template (or pass False)
