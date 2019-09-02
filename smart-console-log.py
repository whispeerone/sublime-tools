import sublime
import sublime_plugin
import re

class ExampleCommand(sublime_plugin.TextCommand):

	def run(self, edit):

		currentLineRaw = self.view.substr(self.view.line(self.view.sel()[0]))

		self.configureCursor(currentLineRaw)

		variable = self.findTarget(currentLineRaw.strip())
		text = self.prepareText(variable)
		self.printText(text)

	def printText(self, text):

		lines = text.split("\n")

		for line in lines:
			self.printLine("\n")
			self.printLine(line)

	def printLine(self, line):
		sublime.set_clipboard(line)
		self.view.run_command('paste_and_indent')

	def findTarget(self, lineRaw):
		line = lineRaw.strip();

		match = re.match(r'(var|const|let)?( )?(.*)( )?=', line)

		if match != None:
			return match.group(3)
		else:
			print("wooow") # TODO
			return


	def prepareText(self, variable):
		text = "console.log(\"{0}\"); // TODO: do not forget to delete".format(variable)
		text += "\nconsole.log({0}); // TODO: do not forget to delete".format(variable)

		return text;

	def configureCursor(self, line):
		cursorPosition = self.view.rowcol(self.view.sel()[0].begin())
		newCursonPosition = self.view.text_point(cursorPosition[0], len(line))
		self.view.sel().clear()
		self.view.sel().add(sublime.Region(newCursonPosition))
