import sublime
import sublime_plugin
import re

class ExampleCommand(sublime_plugin.TextCommand):

	def run(self, edit):

		currentLineRaw = self.view.substr(self.view.line(self.view.sel()[0]))

		self.configureCursor(currentLineRaw)

		variable = self.findTarget(currentLineRaw)
		text = self.prepareText(variable)
		self.printText(text)

	def printText(self, text):

		lines = text.split("\n")
		print(lines)
		for line in lines:
			self.printLine("\n")
			self.printLine(line)

		self.printLine("\n")

	def printLine(self, line):
		sublime.set_clipboard(line)
		self.view.run_command('paste_and_indent')

	def findTarget(self, lineRaw):
		line = lineRaw.strip();

		target = self.findVaribleAssignment(line)

		if target == None:
			target = self.findVariableUsing(lineRaw)

		return target

	def prepareText(self, variable):
		text = "console.log(\"{0}\"); // TODO: do not forget to delete".format(variable)
		text += "\nconsole.log({0}); // TODO: do not forget to delete".format(variable)

		return text;

	def configureCursor(self, line):
		# TODO if return at first place of line
		if (line.strip().startswith("return")):
			self.setCursorColumnPosition(0)
		else:
			self.setCursorToEndOfLine(line)

	def setCursorToEndOfLine(self, line):
		self.setCursorColumnPosition(len(line))

	def setCursorColumnPosition(self, col):
		cursorPosition = self.view.rowcol(self.view.sel()[0].begin())
		newCursonPosition = self.view.text_point(cursorPosition[0], col)
		self.setCursorPosition(newCursonPosition)

	def setCursorPosition(self, point):
		self.view.sel().clear()
		self.view.sel().add(sublime.Region(point))

	def findVaribleAssignment(self, line):
		match = re.match(r'(var|const|let)?( )?(.*)( )?=', line)

		if match != None:
			return match.group(3)
		else:
			return None

	def findVariableUsing(self, line):
		
		bracketIndex = line.find("(")

		if bracketIndex == -1:
			return None

		self.setCursorColumnPosition(bracketIndex + 1)

		self.view.run_command('expand_selection', {"to": "brackets"})
		result = self.view.substr(self.view.sel()[0]) 

		self.setCursorToEndOfLine(line)

		return result
