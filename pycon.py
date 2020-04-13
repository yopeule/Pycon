import json
import sys
import PyQt5
from PyQt5 import QtWidgets
QtCore = PyQt5.QtCore
Qt = QtCore.Qt
QtGui = PyQt5.QtGui

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self, sys_width, sys_height):
        self.title_icon_path = __file__ + '/../title-icon.png'
        super().__init__()
        self.init_ui(sys_width, sys_height)

    def init_ui(self, sys_width, sys_height):
        foo = MyQPlainTextEdit(self)
        self.setCentralWidget(foo)
        self.my_text_edit = foo
        self.setWindowIcon(PyQt5.QtGui.QIcon(self.title_icon_path))
        self.setWindowTitle("Pycon")
        with open(__file__ + '/../my-window-info.json') as jf:
            my_window_info = json.load(jf)
        for window_option in [('window-size', [sys_width/2, sys_height/2], self.resize), ('window-position', [sys_width/4, sys_height/5], self.move)]:
            if window_option[0] in my_window_info:
                my_window_option = my_window_info[window_option[0]]
                for i in range(len(my_window_option)):
                    if my_window_option[i] != 'default':
                        window_option[1][i] = my_window_option[i]
            window_option[2](*window_option[1])

    def keyPressEvent(self, e):
        super().keyPressEvent(e)
        if e.key() == Qt.Key_W:
            if QtWidgets.QApplication.keyboardModifiers() == Qt.ControlModifier:
                self.close()

    def closeEvent(self, e):
        print('close!')
        pass
        super().closeEvent(e)

class MyQPlainTextEdit(QtWidgets.QPlainTextEdit):

    def __init__(self, foo):
        super().__init__(foo)
        with open(__file__ + "/../text-editor-style.txt") as f:
            self.text_edit_style_sheet = f.read()
            self.setStyleSheet(self.text_edit_style_sheet)
        self.myfunction = self.myfunc()
        next(self.myfunction)
        self.preloading()

    def preloading(self):
        self.setPlainText('t')
        self.selectAll()
        self.textCursor().removeSelectedText()

    def keyPressEvent(self, e):
        super().keyPressEvent(e)
        if e.key() in (Qt.Key_Return, Qt.Key_Enter):
            if QtWidgets.QApplication.keyboardModifiers() == Qt.ControlModifier:
                next(self.myfunction)
                self.moveCursor(QtGui.QTextCursor.End)

    def myfunc(self):
        try:
            import my_module
        except ImportError:
            class A:
                def f(self, s):
                    return s + '!'
            my_module = A()
        while True:
            self.setPlainText(my_module.f(self.toPlainText()))
            yield

if __name__ == '__main__':
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    screen_resolution = app.desktop().screenGeometry()
    width, height = screen_resolution.width(), screen_resolution.height()
    ex = MyWindow(width, height)
    ex.show()
    sys.exit(app.exec())