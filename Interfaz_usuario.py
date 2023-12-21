from PyQt5 import QtWidgets, QtCore
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
import sys
from cmath import atan, sqrt
from Path import Path
import numpy as np
import matplotlib.pyplot as plt
from utilities import normalize_trajectory


#############################################################################

#############################################################################

class DialogPP(QtWidgets.QDialog):
 
    # new signal to send data 
    data = QtCore.pyqtSignal(list)
 
    #========================================================================
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(300,200)

        self.setWindowTitle('Modo de posicionamiento por perfil')

        self.label_info = QtWidgets.QLabel('Las coordenas enviadas al robot son absoluta,\r\nes decir que si pones x=0.1 el robot hara un desplazamiento sobre x de 0.1.\r\nTomar en cuanta que el punto de referencia esta en x=0.0 y=0.38')
        self.label_modo = QtWidgets.QLabel('Modo de trabajo :')
        self.label_x = QtWidgets.QLabel('x :')
        self.label_y = QtWidgets.QLabel('y :')
        self.label_z = QtWidgets.QLabel('z :')

        self.workMode = QtWidgets.QComboBox(self)
        self.workMode.addItems(['P (PP)', 'V'])
        self.workMode.setCurrentIndex(0)
        self.workMode.setMinimumHeight(30)

        self.spinbox_x = QtWidgets.QDoubleSpinBox(self)
        self.spinbox_x.setMinimum(-9.00)
        self.spinbox_y = QtWidgets.QDoubleSpinBox(self)
        self.spinbox_y.setMinimum(-9.00)
        self.spinbox_z = QtWidgets.QDoubleSpinBox(self)
        self.spinbox_z.setMinimum(-9.00)

        # create buttons to end the dialog
        qbb = QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        self.buttonbox = QtWidgets.QDialogButtonBox(qbb)
        self.buttonbox.accepted.connect(self.accept) # => button "Ok"
        self.buttonbox.rejected.connect(self.reject) # => button "Annuler"
 
        posit = QtWidgets.QGridLayout()
        posit.addWidget(self.label_modo, 1, 0, 1, 2)
        posit.addWidget(self.workMode, 1, 3, 1, 3)
        posit.addWidget(self.label_x, 3, 0)
        posit.addWidget(self.spinbox_x, 3, 1)
        posit.addWidget(self.label_y, 4, 0)
        posit.addWidget(self.spinbox_y, 4, 1)
        posit.addWidget(self.label_z, 5, 0)
        posit.addWidget(self.spinbox_z, 5, 1)
        posit.addWidget(self.label_info, 6, 0, 6, 9)
        posit.addWidget(self.buttonbox, 9, 4, 9, 7)        
        self.setLayout(posit)
 

    #========================================================================
    def accept(self):
        """normal closing of the dialog window ("Ok" button)"""

        self.data.emit([self.workMode.currentIndex(),self.spinbox_x.value(), 
                           self.spinbox_y.value(), self.spinbox_z.value()])
        self.close()
 
    #========================================================================
    def rejet(self):
        """canceling the data search (“Cancel” button)
            NB: same for closing using the cross or the system menu"""
        
        self.data.emit([None,None,None,None])
        self.close()


#############################################################################
class Dialog2(QtWidgets.QDialog):
 
    # new signal to send data 
    data = QtCore.pyqtSignal(list)
 
    #========================================================================
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(300,200)

        self.setWindowTitle('Modo de posicion interpolada (2 lados)')

        self.label_info = QtWidgets.QLabel('Las coordenas enviadas al robot son absoluta,\r\nes decir que si pones x=0.1 el robot hara un desplazamiento sobre x de 0.1.\r\nTomar en cuanta que el punto de referencia esta en x=0.0 y=0.38')

        self.label_wp_1x = QtWidgets.QLabel('x1 :')
        self.label_wp_1y = QtWidgets.QLabel('y1 :')
        self.label_wp_1z = QtWidgets.QLabel('z1 :')
        self.label_gl_x = QtWidgets.QLabel('x2 :')
        self.label_gl_y = QtWidgets.QLabel('y2 :')
        self.label_gl_z = QtWidgets.QLabel('z2 :')

        self.spinbox_wp_1x = QtWidgets.QDoubleSpinBox(self)
        self.spinbox_wp_1x.setMinimum(-9.00)
        self.spinbox_wp_1y = QtWidgets.QDoubleSpinBox(self)
        self.spinbox_wp_1y.setMinimum(-9.00)
        self.spinbox_wp_1z = QtWidgets.QDoubleSpinBox(self)
        self.spinbox_wp_1z.setMinimum(-9.00)
        self.spinbox_gl_x = QtWidgets.QDoubleSpinBox(self)
        self.spinbox_gl_x.setMinimum(-9.00)
        self.spinbox_gl_y = QtWidgets.QDoubleSpinBox(self)
        self.spinbox_gl_y.setMinimum(-9.00)
        self.spinbox_gl_z = QtWidgets.QDoubleSpinBox(self)
        self.spinbox_gl_z.setMinimum(-9.00)


        # create buttons to end the dialog
        qbb = QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        self.buttonbox = QtWidgets.QDialogButtonBox(qbb)
        self.buttonbox.accepted.connect(self.accept) # => button "Ok"
        self.buttonbox.rejected.connect(self.rejet) # => button "Annuler"
 

        posit = QtWidgets.QGridLayout()

        posit.addWidget(self.label_wp_1x, 3, 0)
        posit.addWidget(self.spinbox_wp_1x, 3, 1)
        posit.addWidget(self.label_wp_1y, 4, 0)
        posit.addWidget(self.spinbox_wp_1y, 4, 1)
        posit.addWidget(self.label_wp_1z, 5, 0)
        posit.addWidget(self.spinbox_wp_1z, 5, 1)

        posit.addWidget(self.label_gl_x, 3, 2)
        posit.addWidget(self.spinbox_gl_x, 3, 3)
        posit.addWidget(self.label_gl_y, 4, 2)
        posit.addWidget(self.spinbox_gl_y, 4, 3)
        posit.addWidget(self.label_gl_z, 5, 2)
        posit.addWidget(self.spinbox_gl_z, 5, 3)

        posit.addWidget(self.label_info, 6, 0, 6, 9)
        
        posit.addWidget(self.buttonbox, 9, 4, 9, 7)        
        self.setLayout(posit)
 

    #========================================================================
    def accept(self):
        """normal closing of the dialog window ("Ok" button)"""

        self.data.emit([self.spinbox_wp_1x.value(), self.spinbox_wp_1y.value(), self.spinbox_wp_1z.value(),
                           self.spinbox_gl_x.value(), self.spinbox_gl_y.value(), self.spinbox_gl_z.value()])
        self.close()
 
    #========================================================================
    def rejet(self):
        """canceling the data search (“Cancel” button)
            NB: same for closing using the cross or the system menu"""
        
        self.data.emit([None,None,None,None,None,None])
        self.close()


#############################################################################
class Dialog4(QtWidgets.QDialog):
 
    # new signal to send data donnes
    data = QtCore.pyqtSignal(list)
 
    #========================================================================
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(300,200)

        self.setWindowTitle('Modo de posicion interpolada (4 lados)')

        self.label_info = QtWidgets.QLabel('Las coordenas enviadas al robot son absoluta,\r\nes decir que si pones x=0.1 el robot hara un desplazamiento sobre x de 0.1.\r\nTomar en cuanta que el punto de referencia esta en x=0.0 y=0.38')

        self.label_wp_1x = QtWidgets.QLabel('x1 :')
        self.label_wp_1y = QtWidgets.QLabel('y1 :')
        self.label_wp_1z = QtWidgets.QLabel('z1 :')
        self.label_wp_2x = QtWidgets.QLabel('x2 :')
        self.label_wp_2y = QtWidgets.QLabel('y2 :')
        self.label_wp_2z = QtWidgets.QLabel('z2 :')
        self.label_wp_3x = QtWidgets.QLabel('x3 :')
        self.label_wp_3y = QtWidgets.QLabel('y3 :')
        self.label_wp_3z = QtWidgets.QLabel('z3 :')
        self.label_gl_x = QtWidgets.QLabel('x4 :')
        self.label_gl_y = QtWidgets.QLabel('y4 :')
        self.label_gl_z = QtWidgets.QLabel('z4 :')

        self.spinbox_wp_1x = QtWidgets.QDoubleSpinBox(self)
        self.spinbox_wp_1x.setMinimum(-9.00)
        self.spinbox_wp_1y = QtWidgets.QDoubleSpinBox(self)
        self.spinbox_wp_1y.setMinimum(-9.00)
        self.spinbox_wp_1z = QtWidgets.QDoubleSpinBox(self)
        self.spinbox_wp_1z.setMinimum(-9.00)
        self.spinbox_wp_2x = QtWidgets.QDoubleSpinBox(self)
        self.spinbox_wp_2x.setMinimum(-9.00)
        self.spinbox_wp_2y = QtWidgets.QDoubleSpinBox(self)
        self.spinbox_wp_2y.setMinimum(-9.00)
        self.spinbox_wp_2z = QtWidgets.QDoubleSpinBox(self)
        self.spinbox_wp_2z.setMinimum(-9.00)
        self.spinbox_wp_3x = QtWidgets.QDoubleSpinBox(self)
        self.spinbox_wp_3x.setMinimum(-9.00)
        self.spinbox_wp_3y = QtWidgets.QDoubleSpinBox(self)
        self.spinbox_wp_3y.setMinimum(-9.00)
        self.spinbox_wp_3z = QtWidgets.QDoubleSpinBox(self)
        self.spinbox_wp_3z.setMinimum(-9.00)
        self.spinbox_gl_x = QtWidgets.QDoubleSpinBox(self)
        self.spinbox_gl_x.setMinimum(-9.00)
        self.spinbox_gl_y = QtWidgets.QDoubleSpinBox(self)
        self.spinbox_gl_y.setMinimum(-9.00)
        self.spinbox_gl_z = QtWidgets.QDoubleSpinBox(self)
        self.spinbox_gl_z.setMinimum(-9.00)


        # create buttons to end the dialog
        qbb = QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        self.buttonbox = QtWidgets.QDialogButtonBox(qbb)
        self.buttonbox.accepted.connect(self.accept) # => button "Ok"
        self.buttonbox.rejected.connect(self.rejet) # => button "Annuler"
 
        posit = QtWidgets.QGridLayout()

        posit.addWidget(self.label_wp_1x, 3, 0)
        posit.addWidget(self.spinbox_wp_1x, 3, 1)
        posit.addWidget(self.label_wp_1y, 4, 0)
        posit.addWidget(self.spinbox_wp_1y, 4, 1)
        posit.addWidget(self.label_wp_1z, 5, 0)
        posit.addWidget(self.spinbox_wp_1z, 5, 1)

        posit.addWidget(self.label_wp_2x, 3, 2)
        posit.addWidget(self.spinbox_wp_2x, 3, 3)
        posit.addWidget(self.label_wp_2y, 4, 2)
        posit.addWidget(self.spinbox_wp_2y, 4, 3)
        posit.addWidget(self.label_wp_2z, 5, 2)
        posit.addWidget(self.spinbox_wp_2z, 5, 3)

        posit.addWidget(self.label_wp_3x, 3, 4)
        posit.addWidget(self.spinbox_wp_3x, 3, 5)
        posit.addWidget(self.label_wp_3y, 4, 4)
        posit.addWidget(self.spinbox_wp_3y, 4, 5)
        posit.addWidget(self.label_wp_3z, 5, 4)
        posit.addWidget(self.spinbox_wp_3z, 5, 5)

        posit.addWidget(self.label_gl_x, 3, 6)
        posit.addWidget(self.spinbox_gl_x, 3, 7)
        posit.addWidget(self.label_gl_y, 4, 6)
        posit.addWidget(self.spinbox_gl_y, 4, 7)
        posit.addWidget(self.label_gl_z, 5, 6)
        posit.addWidget(self.spinbox_gl_z, 5, 7)

        posit.addWidget(self.label_info, 6, 0, 6, 9)
        
        posit.addWidget(self.buttonbox, 9, 4, 9, 7)        
        self.setLayout(posit)
 

    #========================================================================
    def accept(self):
        """normal closing of the dialog window ("Ok" button)"""

        self.data.emit([self.spinbox_wp_1x.value(), self.spinbox_wp_1y.value(), self.spinbox_wp_1z.value(),
                           self.spinbox_wp_2x.value(), self.spinbox_wp_2y.value(), self.spinbox_wp_2z.value(),
                           self.spinbox_wp_3x.value(), self.spinbox_wp_3y.value(), self.spinbox_wp_3z.value(),
                           self.spinbox_gl_x.value(), self.spinbox_gl_y.value(), self.spinbox_gl_z.value()])
        self.close()
 
    #========================================================================
    def rejet(self):
        """canceling the data search (“Cancel” button)
            NB: same for closing using the cross or the system menu"""
        
        self.data.emit([None,None,None,None,None,None,None,None,None,None,None,None])
        self.close()
 

#############################################################################
class DialogC(QtWidgets.QDialog):
 
    # new signal to send data donnes
    data = QtCore.pyqtSignal(list)
 
    #========================================================================
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(300,200)

        self.setWindowTitle('Circulo')

        self.label_info = QtWidgets.QLabel('Las coordenas enviadas al robot son absoluta,\r\nes decir que si pones x=0.1 el robot hara un desplazamiento sobre x de 0.1.\r\nTomar en cuanta que el punto de referencia esta en x=0.0 y=0.38')

        self.label_wp_1x = QtWidgets.QLabel('x1 :')
        self.label_wp_1y = QtWidgets.QLabel('y1 :')
        self.label_wp_1z = QtWidgets.QLabel('z1 :')

        self.spinbox_wp_1x = QtWidgets.QDoubleSpinBox(self)
        self.spinbox_wp_1x.setMinimum(-9.00)
        self.spinbox_wp_1y = QtWidgets.QDoubleSpinBox(self)
        self.spinbox_wp_1y.setMinimum(-9.00)
        self.spinbox_wp_1z = QtWidgets.QDoubleSpinBox(self)
        self.spinbox_wp_1z.setMinimum(-9.00)


        # create buttons to end the dialog
        qbb = QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        self.buttonbox = QtWidgets.QDialogButtonBox(qbb)
        self.buttonbox.accepted.connect(self.accept) # => button "Ok"
        self.buttonbox.rejected.connect(self.rejet) # => button "Annuler"
 

        posit = QtWidgets.QGridLayout()

        posit.addWidget(self.label_wp_1x, 3, 0)
        posit.addWidget(self.spinbox_wp_1x, 3, 1)
        posit.addWidget(self.label_wp_1y, 4, 0)
        posit.addWidget(self.spinbox_wp_1y, 4, 1)
        posit.addWidget(self.label_wp_1z, 5, 0)
        posit.addWidget(self.spinbox_wp_1z, 5, 1)

        posit.addWidget(self.label_info, 6, 0, 6, 9)
        
        posit.addWidget(self.buttonbox, 9, 4, 9, 7)        
        self.setLayout(posit)
 

    #========================================================================
    def accept(self):
        """normal closing of the dialog window ("Ok" button)"""

        self.data.emit([self.spinbox_wp_1x.value(), self.spinbox_wp_1y.value(), self.spinbox_wp_1z.value()])
        self.close()
 
    #========================================================================
    def rejet(self):
        """canceling the data search (“Cancel” button)
            NB: same for closing using the cross or the system menu"""
        
        self.data.emit([None,None,None])
        self.close()
 

#############################################################################

#############################################################################

class ToolBar(QtWidgets.QToolBar):
    def __init__(self, parent):
        super(ToolBar, self).__init__(parent)
        
        self.portOpenButton = QtWidgets.QPushButton('Conectar') #Connect
        self.portOpenButton.setCheckable(True)
        self.portOpenButton.setMinimumHeight(32)

        self.portNames = QtWidgets.QComboBox(self)
        self.portNames.addItems([port.portName() for port in QSerialPortInfo().availablePorts()])
        self.portNames.setMinimumHeight(30)

        self.baudRates = QtWidgets.QComboBox(self)
        self.baudRates.addItems(['300', '600', '1200', '2400', '4800', '9600', '14400', '19200', '28800', 
                                '38400', '57600', '115200', '230400', '460800', '576000', '921600'
        ])
        self.baudRates.setCurrentText('921600')
        self.baudRates.setMinimumHeight(30)

        self.dataBits = QtWidgets.QComboBox(self)
        self.dataBits.addItems(['5 bit', '6 bit', '7 bit', '8 bit'])
        self.dataBits.setCurrentIndex(3)
        self.dataBits.setMinimumHeight(30)

        self.parity_ = QtWidgets.QComboBox(self)
        self.parity_.addItems(['No Parity', 'Even Parity', 'Odd Parity', 'Space Parity', 'Mark Parity'])
        self.parity_.setCurrentIndex(0)
        self.parity_.setMinimumHeight(30)

        self.stopBits = QtWidgets.QComboBox(self)
        self.stopBits.addItems(['One Stop', 'One And Half Stop', 'Two Stop'])
        self.stopBits.setCurrentIndex(0)
        self.stopBits.setMinimumHeight(30)

        self.flowControl_ = QtWidgets.QComboBox(self)
        self.flowControl_.addItems(['No Flow Control', 'Hardware Control', 'Software Control'])
        self.flowControl_.setCurrentIndex(2)
        self.flowControl_.setMinimumHeight(30)

        self.addWidget(self.portOpenButton)
        self.addWidget(self.portNames)
        self.addWidget(self.baudRates)
        self.addWidget(self.dataBits)
        self.addWidget(self.parity_)
        self.addWidget(self.stopBits)
        self.addWidget(self.flowControl_)

    def serialControlEnable(self, flag):
        self.portNames.setEnabled(flag)
        self.baudRates.setEnabled(flag)
        self.dataBits.setEnabled(flag)
        self.parity_.setEnabled(flag)
        self.stopBits.setEnabled(flag)
        self.flowControl_.setEnabled(flag)
        
    def baudRate(self):
        return int(self.baudRates.currentText())

    def portName(self):
        return self.portNames.currentText()

    def dataBit(self):
        return int(self.dataBits.currentIndex()+ 5)

    def parity(self):
        return self.parity_.currentIndex()

    def stopBit(self):
        return self.stopBits.currentIndex()

    def flowControl(self):
        return self.flowControl_.currentIndex()


#############################################################################

#############################################################################

class Window(QtWidgets.QMainWindow):
 
    serialSendstr = QtCore.pyqtSignal(str)
    
    #========================================================================
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.port = QSerialPort()

        self.setWindowTitle('Monitor serie')
        self.label1 = QtWidgets.QLabel("Conectar el puerto serial antes de ingresar la informacion") #("Connect to the port before enter trajectory information")
        self.labelPP = QtWidgets.QLabel("Modo de posicionamiento por perfil :")
        self.labelPI = QtWidgets.QLabel("Modo de posicion interpolada :")
        
        self.buttonPP = QtWidgets.QPushButton("PP", self)
        self.buttonPP.clicked.connect(self.enterPP)
        self.buttonPP.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred) 

        self.button4 = QtWidgets.QPushButton("4 lados", self)
        self.button4.clicked.connect(self.enter4)
        self.button4.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)

        self.button2 = QtWidgets.QPushButton("2 lados", self)
        self.button2.clicked.connect(self.enter2)
        self.button2.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)

        self.buttonC = QtWidgets.QPushButton("Circulo", self)
        self.buttonC.clicked.connect(self.enterC)
        self.buttonC.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)

        self.setCentralWidget(QtWidgets.QWidget(self))
        layout = QtWidgets.QVBoxLayout(self.centralWidget())
        layout.addWidget(self.label1)
        layout.addWidget(self.labelPP)
        layout.addWidget(self.buttonPP)
        layout.addWidget(self.labelPI)
        layout.addWidget(self.button2)
        layout.addWidget(self.button4)
        layout.addWidget(self.buttonC)


        ### Tool Bar ###
        self.toolBar = ToolBar(self)
        self.addToolBar(self.toolBar)

        ### Status Bar ###
        self.setStatusBar(QtWidgets.QStatusBar(self))
        self.statusText = QtWidgets.QLabel(self)
        self.statusBar().addWidget(self.statusText)
        self.statusText.setText('Conectar el puerto')  #'Connect Port'
        
        ### Signal Connect ###
        self.toolBar.portOpenButton.clicked.connect(self.portOpen)
        self.port.readyRead.connect(self.readFromPort)
        self.serialSendstr.connect(self.sendFromPort)


    def portOpen(self, flag):
        if flag:
            self.port.setBaudRate(self.toolBar.baudRate())
            self.port.setPortName(self.toolBar.portName())
            self.port.setDataBits(self.toolBar.dataBit())
            self.port.setParity(self.toolBar.parity())
            self.port.setStopBits(self.toolBar.stopBit())
            self.port.setFlowControl(self.toolBar.flowControl())
            r = self.port.open(QtCore.QIODevice.ReadWrite)

            if not r:
                self.statusText.setText('Puerto abierto error') #'Port open error'
                self.toolBar.portOpenButton.setChecked(False)
                self.toolBar.serialControlEnable(True)
            else:
                self.statusText.setText('Puerto abierto') #'Port opened'
                self.toolBar.serialControlEnable(False)
        else:
            self.port.close()
            self.statusText.setText('Puerto cerrado')   #'Port closed'
            self.toolBar.serialControlEnable(True)
        

    def readFromPort(self):

        print("read")
        data = self.port.readAll()
        print("data : ", data)
        if(data == "0x13"):
            action = "wait"
            self.serialSendstr.disconnect(self.sendFromPort)
            print("action wait: ", action)
        elif (data == "0x11"):
            action = "write"
            self.serialSendstr.connect(self.sendFromPort)
            print("action send: ", action)
        #print("action : ", action)

    def sendFromPort(self, text):
        #print("send")
        self.port.write(text.encode())
        

    #========================================================================
    def enterPP(self):
        """launch Dialog Window for data entry"""

        self.dialog = DialogPP(self)
        self.dialog.data.connect(self.dataEnteredPP) # prepares the recovery of the data entered
        self.dialog.exec_()


    def enter4(self):
        """launch Dialog Window for data entry"""

        self.dialog = Dialog4(self)
        self.dialog.data.connect(self.dataEntered4) # prepares the recovery of the data entered
        self.dialog.exec_()

    def enter2(self):
        """launch Dialog Window for data entry"""

        self.dialog = Dialog2(self)
        self.dialog.data.connect(self.dataEntered2) # prepares the recovery of the data entered
        self.dialog.exec_()
 
    def enterC(self):
        """launch Dialog Window for data entry"""

        self.dialog = DialogC(self)
        self.dialog.data.connect(self.dataEnteredC) # prepares the recovery of the data entered
        self.dialog.exec_()
 
    #========================================================================
    def dataEnteredPP(self, list):
        """Retrieving information"""        
        self.dialog.hide() # hides the dialog window still displayed (it will be closed immediately afterwards)
        if list!=[None, None, None, None]:
            QtWidgets.QMessageBox.information(self, 
                "Puntos entrados:", 
                "Mode : {}\nwp_1x: {}\nwp_1y : {}\nwp_1z : {}\n".format(list[0],list[1],list[2],list[3]))
            
            #print(list)

            fctMode = self.funcionMode(list[0])

            # Create a Path object
            path = Path()

            # Define some interesting points
            gl_x = list[0] 
            gl_y = list[1]
            gl_z = list[2]

            st = path.robot.fkine(np.deg2rad([180, 0, 0])) #inicial point [2.29110437e-17 3.74165739e-01 0.00000000e+00]
            gl = st + np.array([gl_x, gl_y, gl_z])

            x, y, z = gl
            
            di1 = 0.00   
            di2 = 0.25   
            di3 = 0.38

            ai = -2*di2*(x - di1)
            bi = -2*di2*y
            ci = (x - di1)*(x - di1) + y*y + di2*di2 - di3*di3

            q11 = 2*atan((-bi + sqrt(bi*bi - ci*ci + ai*ai))/(ci-ai))
            q21 = 2*atan((-bi - sqrt(bi*bi - ci*ci + ai*ai))/(ci-ai))
            q11 = q11.real
            q21 = q21.real
            q3 = z

            q_lin = np.array([q11, q21, q3])

            # Normalize desire trajectory
            factor = 4 * 300 / np.pi
            q = normalize_trajectory(q_lin, factor)

            q1 = int(q[0]).to_bytes(length=4, byteorder='big',
                                    signed=True).hex()
            q2 = int(q[1]).to_bytes(length=4, byteorder='big',
                                    signed=True).hex()

            frame = ":" + fctMode + "," + q1 + "," + q2 + "\r\n" 
            
            self.serialSendstr.emit(frame)
            
    
    def dataEntered4(self, list):
        """Retrieving information"""        
        self.dialog.hide() # hides the dialog window still displayed (it will be closed immediately afterwards)
        if list!=[None, None, None, None, None, None, None, None, None, None, None, None]:
            QtWidgets.QMessageBox.information(self, 
                "Puntos entrados:", 
                "wp_1x: {}\nwp_1y : {}\nwp_1z : {}\nwp_2x: {}\nwp_2y : {}\nwp_2z : {}\nwp_3x: {}\nwp_3y : {}\nwp_3z : {}\ngl_x: {}\ngl_y : {}\ngl_z : {}\n".format(list[0], list[1],list[2], list[3],list[4], list[5], list[6], list[7],list[8], list[9],list[10], list[11]))

            # Create a Path object
            path = Path()

            # Define some interesting points
            wp_1x = list[0]
            wp_1y = list[1]  
            wp_1z = list[2]
            wp_2x = list[3] 
            wp_2y = list[4]
            wp_2z = list[5]
            wp_3x = list[6] 
            wp_3y = list[7] 
            wp_3z = list[8]
            gl_x = list[9] 
            gl_y = list[10]
            gl_z = list[11]
            

            st = path.robot.fkine(np.deg2rad([180, 0, 0])) #inicial point [2.29110437e-17 3.74165739e-01 0.00000000e+00]
            wp_1 = st + np.array([wp_1x, wp_1y, wp_1z]) 
            wp_2 = wp_1 + np.array([wp_2x, wp_2y, wp_2z])
            wp_3 = wp_2 + np.array([wp_3x, wp_3y, wp_3z])
            gl = wp_3 + np.array([gl_x, gl_y, gl_z])
            pose = np.block([[st], [wp_1], [wp_2], [wp_3], [gl]])
            max_v = [0.3, 0.3, 0.3, 0.3]
            max_a = [1, 1, 1, 1]

            # LINE
            q_lin, qd_lin, qdd_lin, p_lin, pd_lin, pdd_lin = path.line(
                pose=pose, max_v=max_v, max_a=max_a, enable_way_point=False)

            # Show a trajectory
            path.plot_joint(q_lin, qd_lin, qdd_lin)
            path.plot_task(p_lin, pd_lin, pdd_lin)
            plt.show()

            # Normalize desire trajectory
            factor = 4 * 300 / np.pi
            q = normalize_trajectory(q_lin, factor)

            self.encode_send_trajectory(q,)


    def dataEntered2(self, list):
        """Retrieving information"""        
        self.dialog.hide() # hides the dialog window still displayed (it will be closed immediately afterwards)
        if list!=[None, None, None, None, None, None]:
            QtWidgets.QMessageBox.information(self, 
                "Puntos entrados:", 
                "wp_1x: {}\nwp_1y : {}\nwp_1z : z : {}\ngl_x: {}\ngl_y : {}\ngl_z : {}\n".format(list[0],list[1],list[2], list[3],list[4], list[5]))

            # Create a Path object
            path = Path()

            # Define some interesting points
            # wp first point, gl goal point
            wp_1x = list[0]
            wp_1y = list[1] 
            wp_1z = list[2]
            gl_x = list[3] 
            gl_y = list[4]
            gl_z = list[5]
            
            st = path.robot.fkine(np.deg2rad([180, 0, 0])) #inicial point [2.29110437e-17 3.74165739e-01 0.00000000e+00]
            wp_1 = st + np.array([wp_1x, wp_1y, wp_1z]) 
            gl = wp_1 + np.array([gl_x, gl_y, gl_z])
            pose = np.block([[st], [wp_1], [gl]])
            max_v = [0.3, 0.3, 0.3, 0.3]
            max_a = [1, 1, 1, 1]

            # LINE
            q_lin, qd_lin, qdd_lin, p_lin, pd_lin, pdd_lin = path.line(
                pose=pose, max_v=max_v, max_a=max_a, enable_way_point=False)

            # Show a trajectory
            path.plot_joint(q_lin, qd_lin, qdd_lin)
            path.plot_task(p_lin, pd_lin, pdd_lin)
            plt.show()
            
            # Normalize desire trajectory
            factor = 4 * 300 / np.pi
            q = normalize_trajectory(q_lin, factor)

            self.encode_send_trajectory(q)
             

    def dataEnteredC(self, list):
        """Retrieving information"""       
        self.dialog.hide() # hides the dialog window still displayed (it will be closed immediately afterwards)
        if list!=[None, None, None]:
            QtWidgets.QMessageBox.information(self, 
                "Puntos entrados:", 
                "wp_1x: {}\nwp_1y : {}\nwp_1z : {}\n".format(list[0],list[1],list[2]))

            # Create a Path object
            path = Path()

            wp_1x = list[0]
            wp_1y = list[1]
            wp_1z = list[2]
            
            # CIRCLE
            st = path.robot.fkine(np.deg2rad([180, 0, 0])) #inicial point [2.29110437e-17 3.74165739e-01 0.00000000e+00]
            c = st + np.array([wp_1x, wp_1y, wp_1z]) 

            q_cir, qd_cir, qdd_cir, p_cir, pd_cir, pdd_cir = path.circle(start=st,
                                                             center=c,
                                                             max_vel=0.2,
                                                             max_acc=1.)

            # Show a trajectory
            path.plot_joint(q_cir, qdd_cir, qdd_cir)
            path.plot_task(p_cir, pd_cir, pdd_cir)

            # Normalize desire trajectory
            factor = 8 * 300 / np.pi
            q = normalize_trajectory(q_cir, factor)

            self.encode_send_trajectory(q)             


    def funcionMode(self, list):
        if list == 0:
            mode = "P"            
        elif list == 1:
            mode = "V"
        return mode


    def encode_send_trajectory(self,points):
        for point in points:
            q1 = int(point[0]).to_bytes(length=4, byteorder='big',
                                    signed=True).hex()
            q2 = int(point[1]).to_bytes(length=4, byteorder='big',
                                    signed=True).hex()
            frame = ':S,' + q1 + ',' + q2 + '\r\n'
            print(frame)
            self.serialSendstr.emit(frame)
                   
 
#############################################################################
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    fen = Window()
    fen.show()
    sys.exit(app.exec_())
