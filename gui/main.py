import sys
import traceback

from serial import Serial
from serial.threaded import ReaderThread, LineReader

from PyQt5.QtCore import (
    pyqtSignal, QObject, QTimer
)

from PyQt5.QtGui import (
    QPixmap
)

from PyQt5.QtWidgets import (
    QApplication, QMainWindow
)

from demo_ui import Ui_MainWindow

ScrollBarStyleSheet = '''
QScrollBar:vertical {
    border: 0px solid #999999;
    background:white;
    width:20px;    
    margin: 0px 0px 0px 0px;
}
QScrollBar::handle:vertical {
    background-color: #2596be;
    min-height: 0px;
    border-radius: 8px;
}
QScrollBar::add-line:vertical {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
    stop: 0 rgb(32, 47, 130), stop: 0.5 rgb(32, 47, 130),  stop:1 rgb(32, 47, 130));
    height: 0px;
    subcontrol-position: bottom;
    subcontrol-origin: margin;
}
QScrollBar::sub-line:vertical {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
    stop: 0  rgb(32, 47, 130), stop: 0.5 rgb(32, 47, 130),  stop:1 rgb(32, 47, 130));
    height: 0 px;
    subcontrol-position: top;
    subcontrol-origin: margin;
}
'''
# Custom signals
class MySignalEmitter(QObject):

    rxSignal = pyqtSignal(str)
    startTimerSignal = pyqtSignal(int)
    restartTimerSignal = pyqtSignal(int)
    setSceneSignal = pyqtSignal(int,str)

# Class to read UART by line
class PrintLines(LineReader):
    TERMINATOR = b'\r\n'
    # ENCODING = 'ascii'

    rxSignal = None
    startTimerSignal = None
    restartTimerSignal = None
    setSceneSignal = None

    # Connection opened
    def connection_made(self, transport):
        sys.stdout.write('port opened\n')
    
    # Called when a new line is received
    def handle_line(self, line):
        if line.find('$READY$') != -1:
            # Start timer and set first scene
            self.startTimerSignal.emit(300)

        elif line.find('$HB$') != -1:
            # Restart timer
            self.restartTimerSignal.emit(300)

        elif line.find('$GOTO$_') != -1:
            idx = line.find('$GOTO$_')
            self.setSceneSignal.emit(int(line[idx + 7]),
                                     line[(idx + 8) : (idx + 11)])

        else:
            self.rxSignal.emit(repr(line))

    # Called when connection is lost
    def connection_lost(self, exc):
        if exc:
            traceback.print_exc(exc)
        sys.stdout.write('port closed\n')

class DemoWindow(QMainWindow):

    def __init__(self):
        super(DemoWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Resize main window to the size of the screen
        rec = QApplication.desktop().screenGeometry()
        height = rec.height()
        width = rec.width()
        self.resize(width, height)

        self.lifeTimer=QTimer()

        # Connect signals
        self.SignalEmmiter = MySignalEmitter()
        # Signal to emit when receiving UART data
        self.SignalEmmiter.rxSignal.connect(self.ui.terminalBox.appendPlainText)
        # Signal to emit when system is ready or when receiving heart beats
        self.SignalEmmiter.startTimerSignal.connect(self.lifeTimer.start)
        self.SignalEmmiter.startTimerSignal.connect(lambda: self.ui.statusLabel.setPixmap(QPixmap(":/images/images/heart_red.png")))
        # Signal to emit when receiving heart beats
        self.SignalEmmiter.restartTimerSignal.connect(self.lifeTimer.start)
        self.SignalEmmiter.restartTimerSignal.connect(lambda: self.ui.statusLabel.setPixmap(QPixmap(":/images/images/heart_red.png")))
        # Timeout event
        self.lifeTimer.timeout.connect(lambda: self.ui.statusLabel.setPixmap(QPixmap(":/images/images/heart_gray.png")))
        # Signal to set scene
        self.SignalEmmiter.setSceneSignal.connect(self.setScene)

    def setScene(self, index, sw):

        switches = [
            self.ui.sw0Label,
            self.ui.sw1Label,
            self.ui.sw2Label,
            self.ui.sw3Label,
            self.ui.sw4Label,
            self.ui.sw5Label,
            self.ui.sw6Label,
            self.ui.sw7Label
        ]

        if index == 0:
            self.ui.sw0Label.setPixmap(QPixmap(":/images/images/sw_off.png"))
            self.ui.sw1Label.setPixmap(QPixmap(":/images/images/sw_off.png"))
            self.ui.sw2Label.setPixmap(QPixmap(":/images/images/sw_off.png"))
            self.ui.sw3Label.setPixmap(QPixmap(":/images/images/sw_off.png"))
            self.ui.sw4Label.setPixmap(QPixmap(":/images/images/sw_off.png"))
            self.ui.sw5Label.setPixmap(QPixmap(":/images/images/sw_off.png"))
            self.ui.sw6Label.setPixmap(QPixmap(":/images/images/sw_off.png"))
            self.ui.sw7Label.setPixmap(QPixmap(":/images/images/sw_off.png"))
        
        # Select attack screen
        elif index == 1:
            # Instructions
            self.ui.instLabel.setText("Select a target to attack")
            self.ui.opt1Label.setText("L - Firmware (OpenSBI)")
            self.ui.opt2Label.setText("R - Bao hypervisor")
            self.ui.opt3Label.setText("")
            # Buttons
            self.ui.btnULabel.setPixmap(QPixmap(":/images/images/btnu_dis.png"))
            self.ui.btnDLabel.setPixmap(QPixmap(":/images/images/btnd_dis.png"))
            self.ui.btnLLabel.setPixmap(QPixmap(":/images/images/btnl_en.png"))
            self.ui.btnRLabel.setPixmap(QPixmap(":/images/images/btnr_en.png"))
            self.ui.btnCLabel.setPixmap(QPixmap(":/images/images/btnc_dis.png"))
            # Target
            self.ui.targetLabel.setPixmap(QPixmap(":/images/images/square.png"))
        
        # Update target label (Bao)
        elif index == 2:
            # Target
            self.ui.targetLabel.setPixmap(QPixmap(":/images/images/bao_target.png"))

        # Update target label (OpenSBI)
        elif index == 3:
            # Target
            self.ui.targetLabel.setPixmap(QPixmap(":/images/images/opensbi_target.png"))

        # Switch selection
        elif index == 4:
            # Instructions
            self.ui.instLabel.setText("Make your choice and attack!")
            self.ui.opt1Label.setText("U - Attack!")
            self.ui.opt2Label.setText("C - Change target")
            self.ui.opt3Label.setText("D - Restart attack")
            # Buttons
            self.ui.btnULabel.setPixmap(QPixmap(":/images/images/btnu_en.png"))
            self.ui.btnDLabel.setPixmap(QPixmap(":/images/images/btnd_en.png"))
            self.ui.btnLLabel.setPixmap(QPixmap(":/images/images/btnl_dis.png"))
            self.ui.btnRLabel.setPixmap(QPixmap(":/images/images/btnr_dis.png"))
            self.ui.btnCLabel.setPixmap(QPixmap(":/images/images/btnc_en.png"))

        # Attack (failed)
        elif index == 6:
            # Instructions
            self.ui.instLabel.setText("Attacking!")
            self.ui.opt1Label.setText("")
            self.ui.opt2Label.setText("")
            self.ui.opt3Label.setText("")
            # Buttons
            self.ui.btnULabel.setPixmap(QPixmap(":/images/images/btnu_dis.png"))
            self.ui.btnDLabel.setPixmap(QPixmap(":/images/images/btnd_dis.png"))
            self.ui.btnCLabel.setPixmap(QPixmap(":/images/images/btnc_dis.png"))

            # Set enabled switches
            for n in range(8):
                digit = (int(sw) & (1 << n)) >> n
                if digit:
                    switches[n].setPixmap(QPixmap(":/images/images/sw_on.png"))

        # Attack (success)
        elif index == 5:
            # Instructions
            self.ui.instLabel.setText("Attacking!")
            self.ui.opt1Label.setText("")
            self.ui.opt2Label.setText("")
            self.ui.opt3Label.setText("")
            # Buttons
            self.ui.btnULabel.setPixmap(QPixmap(":/images/images/btnu_dis.png"))
            self.ui.btnDLabel.setPixmap(QPixmap(":/images/images/btnd_dis.png"))
            self.ui.btnCLabel.setPixmap(QPixmap(":/images/images/btnc_dis.png"))
            # Set killer switch
            switches[int(sw)].setPixmap(QPixmap(":/images/images/sw_dead.png"))

        # After failed attack
        elif index == 7:
            # Instructions
            self.ui.instLabel.setText("You were lucky :)")
            self.ui.opt1Label.setText("C - Next round!")
            # Buttons
            self.ui.btnCLabel.setPixmap(QPixmap(":/images/images/btnc_en.png"))
        

if __name__ == "__main__":

    if len(sys.argv) != 2:
        sys.stderr.write('Wrong number of arguments!\nPlease, provide the path to the serial port connected to the FPGA board (e.g., /dev/ttyUSB0)')
        exit()

    app = QApplication(sys.argv)
    win = DemoWindow()

    win.setStyleSheet(ScrollBarStyleSheet)

    # Initiate serial port
    serial_port = Serial(sys.argv[1], baudrate=115200)

    # Setup RX signal
    PrintLines.rxSignal = win.SignalEmmiter.rxSignal

    # Setup timer signals
    PrintLines.startTimerSignal = win.SignalEmmiter.startTimerSignal
    PrintLines.restartTimerSignal = win.SignalEmmiter.restartTimerSignal

    # Setup stackedWidget signal
    PrintLines.setSceneSignal = win.SignalEmmiter.setSceneSignal

    # Initiate ReaderThread
    reader = ReaderThread(serial_port, PrintLines)

    # Start reader
    reader.start()

    win.showFullScreen()

    # reader.stop()
    sys.exit(app.exec())