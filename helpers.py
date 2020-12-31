import wx, subprocess
wapp = wx.App()
frm = wx.Frame(None, -1, '')

def getch():
	# Code from https://blog.csdn.net/damiaomiao666/article/details/50494581
	# by user 小杰666, with minor modifications

	import sys, termios

	fd = sys.stdin.fileno()
	old = termios.tcgetattr(fd)
	new = termios.tcgetattr(fd)
	# turn off echo and press-enter
	new[3] = new[3] & ~termios.ECHO & ~termios.ICANON

	try:
		termios.tcsetattr(fd, termios.TCSADRAIN, new)
		sys.stdin.read(1)
	finally:
		termios.tcsetattr(fd, termios.TCSADRAIN, old)

def new(self, app):
	pass  # TODO: integrate new file w/ multitabbing

def open_file(self, app):
	with wx.FileDialog(frm, "Open file", wildcard="Any file|*",
					   style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
		if fileDialog.ShowModal() == wx.ID_CANCEL:
			return
		path = fileDialog.GetPath()
		app.txtField.fileName = path
		with open(path, 'r') as fr:
			for ch in fr.read():
				app.txtField.txtBuffer.append((ch, (255, 255, 255)))
				if ch == '\n':
					app.txtField.maxLine += 1
		app.txtField.changeLine(0)

def save_as(self, app):
	with wx.FileDialog(frm, "Save As...", wildcard="C++ Source Files (*.cpp)|*.cpp|All Files (*.*)|*.*",
					   style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
		if fileDialog.ShowModal() == wx.ID_CANCEL:
			return
		path = fileDialog.GetPath()
		app.txtField.fileName = path
		with open(path, 'w') as fw:
			s = ''
			for ch, clr in app.txtField.txtBuffer:
				s += ch
			fw.write(s)
			
def save(self, app):
	s = ''
	for ch, clr in app.txtField.txtBuffer:
		s += ch
	if app.txtField.fileName:
		with open(app.txtField.fileName, 'w') as fw:
			fw.write(s)
	else:
		save_as(self, app)

def compile_cpp(self, app, run=0):
	compileFlags = ['./build', str(run), app.txtField.fileName.rstrip(".cpp")]
	print(compileFlags)
	cmd = " ".join(compileFlags)
	for i in range(3): compileFlags.pop(0)
	if run == 0:
		subprocess.run(cmd)
	elif run:
		subprocess.run(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)

def compile_run_cpp(self, app, compileFlags=[]):
	compile_cpp(self, app, 2)

def run_cpp(self, app):
	compile_cpp(self, app, 1)

def calc_pos(pos):
	px, py = pos
	x = max((px - 146) // 10, 0)
	y = max((py - 160) // 20, 0)
	return x, y