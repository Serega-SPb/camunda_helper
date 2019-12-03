# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Repositories\camunda_helper\modules\move_task\view.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(10)
        Form.setFont(font)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.startTaskChbx = QtWidgets.QCheckBox(Form)
        self.startTaskChbx.setObjectName("startTaskChbx")
        self.gridLayout.addWidget(self.startTaskChbx, 2, 0, 1, 1)
        self.transpositionBtn = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.transpositionBtn.sizePolicy().hasHeightForWidth())
        self.transpositionBtn.setSizePolicy(sizePolicy)
        self.transpositionBtn.setMaximumSize(QtCore.QSize(50, 16777215))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.transpositionBtn.setFont(font)
        self.transpositionBtn.setObjectName("transpositionBtn")
        self.gridLayout.addWidget(self.transpositionBtn, 1, 2, 1, 1)
        self.closeTaskChbx = QtWidgets.QCheckBox(Form)
        self.closeTaskChbx.setObjectName("closeTaskChbx")
        self.gridLayout.addWidget(self.closeTaskChbx, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 1, 1, 1)
        self.closeTaskTxb = QtWidgets.QLineEdit(Form)
        self.closeTaskTxb.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(10)
        self.closeTaskTxb.setFont(font)
        self.closeTaskTxb.setObjectName("closeTaskTxb")
        self.gridLayout.addWidget(self.closeTaskTxb, 0, 1, 1, 3)
        self.startTaskTxb = QtWidgets.QLineEdit(Form)
        self.startTaskTxb.setEnabled(False)
        self.startTaskTxb.setObjectName("startTaskTxb")
        self.gridLayout.addWidget(self.startTaskTxb, 2, 1, 1, 3)

        self.retranslateUi(Form)
        self.closeTaskChbx.toggled['bool'].connect(self.closeTaskTxb.setEnabled)
        self.closeTaskChbx.clicked.connect(self.closeTaskTxb.clear)
        self.startTaskChbx.toggled['bool'].connect(self.startTaskTxb.setEnabled)
        self.startTaskChbx.clicked.connect(self.startTaskTxb.clear)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.startTaskChbx.setText(_translate("Form", "Start"))
        self.transpositionBtn.setText(_translate("Form", "↕"))
        self.closeTaskChbx.setText(_translate("Form", "Close"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
