import leo.core.leoGlobals as g
from leo.core.leoQt import QtCore, QtGui, QtWidgets, QtConst

import time  # temporary for debugging
def DBG(text):
    """DBG - temporary debugging function

    :param str text: text to print
    """
    print("LEP: \033[34m%s\033[39m" % text)
class LEP_PlainTextEdit(QtWidgets.QTextEdit):
    """LEP_PlainTextEdit - simple LeoEditorPane editor
    """
    lep_name = "Plain Text Edit"
    def __init__(self, c=None, lep=None, *args, **kwargs):
        """set up"""
        QtWidgets.QTextEdit.__init__(self, *args, **kwargs)
        self.c = c
        self.lep = lep
        self.textChanged.connect(self.text_changed)
    def focusInEvent (self, event):
        QtWidgets.QTextEdit.focusInEvent(self, event)
        DBG("focusin()")
        self.lep.edit_widget_focus()
        self.update_position(self.lep.get_position())

    def focusOutEvent (self, event):
        QtWidgets.QTextEdit.focusOutEvent(self, event)
        DBG("focusout()")
        #X p = self.lep.get_position()
        #X p.b = self.toPlainText()
        #X self.lep.c.redraw()
    def new_position(self, p):
        """new_position - update for new position

        :param Leo position p: new position
        """
        self.setText(p.b)
    def text_changed(self):
        """text_changed - text editor text changed"""
        if QtWidgets.QApplication.focusWidget() == self:
            DBG("text changed, focused")
            self.lep.text_changed(self.toPlainText())
        else:
            DBG("text changed, NOT focused")
    def update_position(self, p):
        """update_position - update for current position

        :param Leo position p: current position
        """
        DBG("update editor position")
        self.setText(p.b)
