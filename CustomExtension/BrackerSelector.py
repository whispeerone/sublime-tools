import sublime
import sublime_plugin
import re

class SelectBracketCommand(sublime_plugin.TextCommand):

	def run(self, edit):

		currentLineRaw = self.view.substr(self.view.line(self.view.sel()[0]))

		bracketIndex = currentLineRaw.find("(")

		if bracketIndex == -1:
			bracketIndex = currentLineRaw.find("{")

		if bracketIndex == -1: 
			return

		self.setCursorColumnPosition(bracketIndex + 1)

		self.view.run_command('expand_selection', {"to": "brackets"})
		

	def setCursorColumnPosition(self, col):
		cursorPosition = self.view.rowcol(self.view.sel()[0].begin())
		newCursonPosition = self.view.text_point(cursorPosition[0], col)
		self.setCursorPosition(newCursonPosition)

	def setCursorPosition(self, point):
		self.view.sel().clear()
		self.view.sel().add(sublime.Region(point))
