from Tkinter import *
import CreateNewIssue as NewJiraTicket

class Jira_Tasker_GUI:
	''' 
		Simple GUI to accomodate the quick-creation of JIRA tickets with 
		or without a pre-defined user template.
		
		Has not been tested extensively for null or unknown values/input.
		
		TODO: Implement exception handling ...
	'''
	
	def __init__(self, master):
		main_frame = self.frame = Frame(master)
		main_frame.grid()
		
		Label(main_frame, text='Bug Summary').grid(row=0, column=0, sticky=W+E)                          # SUMMARY text entry field label

		text_entry = self.text_entry = Entry(main_frame, width=400)                                      # SUMMARY text entry field
		text_entry.grid(row=1, column=0, columnspan=16)

		self.cancel = Button(main_frame, text="CANCEL", fg="red", command=main_frame.quit)               # CANCEL button
		self.create_new = Button(main_frame, text="CREATE", command=self.__create_new_issue_callback)    # CREATE ISSUE button
		
		self.cancel.grid(row=3, column=0, sticky=W+E)
		self.create_new.grid(row=2, column=0, sticky=W+E)
		
		self.platform_toggle_var = IntVar()
		self.platform_toggle = Checkbutton(main_frame, text="Use Android template? (default is iOS)", variable=self.platform_toggle_var) # TOGGLE for android or iOS
		self.platform_toggle.grid(row=4, column=0, sticky=W)
		
		self.empty_ticket_toggle_var = IntVar()
		self.empty_ticket_toggle = Checkbutton(main_frame, text="Create blank ticket?", variable=self.empty_ticket_toggle_var)           # TOGGLE for blank issue (no template)
		self.empty_ticket_toggle.grid(row=5, column=0, sticky=W)
		
	def __create_new_issue_callback(self):
		summary = self.text_entry.get()
		platform_toggle_value = self.platform_toggle_var.get()
		empty_ticket_toggle_value = self.empty_ticket_toggle_var.get()
		
		if summary == '':
			print '[+]SUMMARY FIELD CANNOT BE EMPTY'
		else:
			if empty_ticket_toggle_value == 1:
				blank_ticket = NewJiraTicket.JiraTicket(summary)              # create a blank issue (no template)
				blank_ticket.create_issue(True)
			elif empty_ticket_toggle_value == 0:
				if platform_toggle_value == 0:
					ticket_ios = NewJiraTicket.JiraTicket(summary, 0)         # create an issue using iOS template
					ticket_ios.create_issue()
				elif platform_toggle_value == 1:
					ticket_droid = NewJiraTicket.JiraTicket(summary, 1)       # create an issue using android template
					ticket_droid.create_issue()
			self.frame.quit()

def run_jira_tasker():
	root_window = Tk()
	app = Jira_Tasker_GUI(root_window)

	root_window.title("CREATE A NEW ISSUE")
	root_window.geometry('600x150')

	root_window.mainloop()
	root_window.destroy()
	
run_jira_tasker()