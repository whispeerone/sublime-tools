import sublime
import sublime_plugin
import re

class TargetParam:
	def __init__(self, expression, type):
		self.expression = expression
		self.type = type

class ExampleCommand(sublime_plugin.TextCommand):

	def run(self, edit):

		currentLineRaw = self.view.substr(self.view.line(self.view.sel()[0]))

		if (currentLineRaw.find("//") > -1):
			currentLineRaw = currentLineRaw[0 : currentLineRaw.find("//")]

		targetOptions = self.findTarget(currentLineRaw)

		if (targetOptions == None or targetOptions.expression == None):
			self.setCursorToEndOfLine()
			self.printLine(" //nothing found")
			return 

		text = self.prepareText(targetOptions.expression)

		self.printText(text, targetOptions)

	def printText(self, text, targetOptions):

		self.configureCursor(targetOptions)

		if (targetOptions.type == "assigment"):
			self.printLine("\n")

		self.printLine(text)

		if (targetOptions.type == "using"):
			self.printLine("\n")

	def printLine(self, line):
		sublime.set_clipboard(line)
		self.view.run_command('paste_and_indent')

	def isInsertedTextShouldBeUnderLine(self, line):
		if (line.strip().startswith("return")):
			return false
		return true

	def findTarget(self, lineRaw):
		line = lineRaw.strip();

		target = self.findVaribleAssignment(line)

		if target == None:
			target = self.findVariableUsing(lineRaw)

		return target

	def prepareText(self, expression):
		text = "console.log(\"{0}\"); // TODO: do not forget to delete".format(expression)
		text += "\nconsole.log({0}); // TODO: do not forget to delete".format(expression)

		return text;

	def configureCursor(self, target):
		if (target.type == "assigment"):
			self.setCursorToEndOfLine()
		else:
			self.setCursorColumnPosition(0)

	def setCursorToEndOfLine(self, line=None):
		if (line == None):
			line = self.view.substr(self.view.line(self.view.sel()[0]))

		self.setCursorColumnPosition(len(line))

	def setCursorColumnPosition(self, col):
		cursorPosition = self.view.rowcol(self.view.sel()[0].begin())
		newCursonPosition = self.view.text_point(cursorPosition[0], col)
		self.setCursorPosition(newCursonPosition)

	def setCursorPosition(self, point):
		self.view.sel().clear()
		self.view.sel().add(sublime.Region(point))

	def findVaribleAssignment(self, line):

		match = re.match(r'^(?!.*(while|if))(var|const|let )?(.*)=', line)

		if match != None:
			return TargetParam(match.group(3), "assigment") 
		else:
			return None

	def findVariableUsing(self, line):

		if (line.strip().startswith("return")):
			expression = line[line.find("return")+6 : None].replace(";", "")
		else:
			expression = self.getBracketExpression(line)

		if (expression == None):
			return None

		return TargetParam(expression, "using") 

	def getBracketExpression(self, line):
		bracketIndex = line.find("(")

		if bracketIndex == -1:
			return None

		self.setCursorColumnPosition(bracketIndex + 1)

		self.view.run_command('expand_selection', {"to": "brackets"})
		result = self.view.substr(self.view.sel()[0]) 

		return result
