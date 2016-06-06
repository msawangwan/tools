from Tkinter import *
import os
import shutil
import CreateNewIssue as NewJiraTicket

class Jira_Tasker_GUI:
	''' 
		Simple GUI to accomodate the quick-creation of JIRA tickets.
		
		Have done some light testing with invalid/null input, but not all cases
		are accounted for. For example, a broken config file.
		
		TODO: Implement exception handling ...
	'''

	root_dir = os.path.realpath('.')
	tmp_dir = os.path.join(root_dir, "tmp")

	cfg_filename = "userconfig.ini"
	backup_cfg_filename = "userconfig.ini.backup"

	original_cfg = os.path.join(root_dir, cfg_filename)

	has_copied_cfg = False

	def __init__(self, master):
		def __close_on_cancel(): # Define nested func to close over the 'main_frame' var
			self.__del_copied_cfg()
			main_frame.quit()

		main_frame = self.frame = Frame(master)
		main_frame.grid()
		
		Label(main_frame, text='BUG SUMMARY').grid(row=0, column=0, sticky=W) # Label for summary txt entry field

		text_entry = self.text_entry = Entry(main_frame, width=400) # SUMMARY text entry field
		text_entry.grid(row=1, column=0, columnspan=16)

		self.cancel = Button(main_frame, text="EXIT", fg="red", command=__close_on_cancel)                                # CANCEL button
		self.create_new = Button(main_frame, text="CREATE AND POST TO DB", command=self.__create_new_issue_callback)      # CREATE ISSUE button
		self.edit_config = Button(main_frame, text="MAKE TEMP CHANGES TO TEMPLATE (CONFIG)", command=self.__edit_usr_cfg) # EDIT config (edits are NOT saved!)

		self.create_new.grid(row=10, column=0, sticky=W+E)
		self.cancel.grid(row=11, column=0, sticky=W+E)
		self.edit_config.grid(row=9, column=0, sticky=W+E)
		
		self.platform_toggle_var = IntVar()
		self.platform_toggle = Checkbutton(main_frame, text="ANDROID TEMPLATE (default is iOS)", variable=self.platform_toggle_var) # TOGGLE for android or iOS
		self.platform_toggle.grid(row=7, column=0, sticky=W)

		self.empty_ticket_toggle_var = IntVar()
		self.empty_ticket_toggle = Checkbutton(main_frame, text="BLANK TICKET", variable=self.empty_ticket_toggle_var) # TOGGLE for blank issue
		self.empty_ticket_toggle.grid(row=8, column=0, sticky=W)

	def __create_new_issue_callback(self):
		summary = self.text_entry.get()
		platform_toggle_value = self.platform_toggle_var.get()
		empty_ticket_toggle_value = self.empty_ticket_toggle_var.get()
		
		if summary == '':
			print '[+] SUMMARY FIELD CANNOT BE EMPTY'
		else:
			if empty_ticket_toggle_value == 1:
				blank_ticket = NewJiraTicket.JiraTicket(summary)        # create a blank issue
				blank_ticket.create_issue(True)
			elif empty_ticket_toggle_value == 0:
				if platform_toggle_value == 0:
					ticket_ios = NewJiraTicket.JiraTicket(summary, 0)   # create an issue using iOS template
					ticket_ios.create_issue()
				elif platform_toggle_value == 1:
					ticket_droid = NewJiraTicket.JiraTicket(summary, 1) # create an issue using android template
					ticket_droid.create_issue()

			self.__del_copied_cfg()
			self.frame.quit()

	def __edit_usr_cfg(self):
		self.__copy_cfg()

		cfg_path = os.path.join(self.root_dir,self.cfg_filename)
		os.startfile(cfg_path, 'open')
	

	def __copy_cfg(self):
		if not os.path.exists(self.tmp_dir):
			os.makedirs(self.tmp_dir)

			shutil.copy(self.original_cfg, self.tmp_dir)
			backup_cfg = os.path.join(self.tmp_dir, self.cfg_filename)
			backup_cfg_name = os.path.join(self.tmp_dir, self.backup_cfg_filename)

			os.rename(backup_cfg, backup_cfg_name)

			self.has_copied_cfg = True

	def __del_copied_cfg(self):
		if self.has_copied_cfg:
			bckup_cfg = os.path.join(self.tmp_dir, self.backup_cfg_filename)

			shutil.move(bckup_cfg, self.root_dir)
			shutil.move(self.original_cfg, self.tmp_dir)
			shutil.rmtree(self.tmp_dir)

			cfg_to_rename = os.path.join(self.root_dir, self.backup_cfg_filename)
			os.rename(cfg_to_rename, self.original_cfg)

			self.has_copied_cfg = False

def run_jira_tasker():
	root_window = Tk()
	app = Jira_Tasker_GUI(root_window)

	root_window.title("CREATE A NEW ISSUE")
	root_window.geometry("600x350")

	root_window.mainloop()
	root_window.destroy()
	
run_jira_tasker()
