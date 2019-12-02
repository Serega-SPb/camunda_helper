# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Repositories\camunda_helper\modules\set_variable\view.ui'
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
        self.label_2 = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 3, 1, 1)
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 4)
        self.valueVarPte = QtWidgets.QPlainTextEdit(Form)
        self.valueVarPte.setObjectName("valueVarPte")
        self.gridLayout.addWidget(self.valueVarPte, 2, 0, 1, 5)
        self.label = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.typeVarCmb = QtWidgets.QComboBox(Form)
        self.typeVarCmb.setEnabled(False)
        self.typeVarCmb.setObjectName("typeVarCmb")
        self.typeVarCmb.addItem("")
        self.gridLayout.addWidget(self.typeVarCmb, 0, 4, 1, 1)
        self.nameVarTxb = QtWidgets.QLineEdit(Form)
        self.nameVarTxb.setObjectName("nameVarTxb")
        self.gridLayout.addWidget(self.nameVarTxb, 0, 1, 1, 2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.label_4)
        self.validStatusLbl = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.validStatusLbl.sizePolicy().hasHeightForWidth())
        self.validStatusLbl.setSizePolicy(sizePolicy)
        self.validStatusLbl.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.validStatusLbl.setFont(font)
        self.validStatusLbl.setStyleSheet("")
        self.validStatusLbl.setText("")
        self.validStatusLbl.setTextFormat(QtCore.Qt.AutoText)
        self.validStatusLbl.setObjectName("validStatusLbl")
        self.horizontalLayout.addWidget(self.validStatusLbl)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.gridLayout.addLayout(self.horizontalLayout, 3, 0, 1, 5)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_2.setText(_translate("Form", "Type"))
        self.label_3.setText(_translate("Form", "Value"))
        self.label.setText(_translate("Form", "Name"))
        self.typeVarCmb.setItemText(0, _translate("Form", "json"))
        self.label_4.setText(_translate("Form", "Value validate status: "))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
