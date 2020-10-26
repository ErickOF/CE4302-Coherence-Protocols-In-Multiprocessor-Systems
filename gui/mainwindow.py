from PyQt5 import QtGui, QtCore, uic
from PyQt5.QtWidgets import QLabel, QLineEdit, QMainWindow, QMessageBox
from PyQt5.QtWidgets import QPushButton, QTableWidget, QTableWidgetItem
from threading import Thread
from time import sleep

from hardware.system import System
from hardware.cpu.processor import Processor
from utils.formats import instr2string


class MainWindow(QMainWindow):
    """Main Window class.
    """
    def __init__(self):
        """Constructor.
        """
        self.__cycles = 0
        self.__frequency = 1
        self.__total_cycles = 0
        self.__opened = True
        self.__running = False
        self.__wait = True

        # Call the inherited classes __init__ method
        super(MainWindow, self).__init__()

        # Load the .ui file
        uic.loadUi('./gui/mainwindow.ui', self)

        # Components
        # Restart button
        self.__btnRestart = self.findChild(QPushButton, 'btnRestart')
        self.__btnRestart.clicked.connect(self.__btnRestartOnClick)

        # Start button
        self.__btnStart = self.findChild(QPushButton, 'btnStart')
        self.__btnStart.clicked.connect(self.__btnStartOnClick)

        # Step button
        self.__btnStep = self.findChild(QPushButton, 'btnStep')
        self.__btnStep.clicked.connect(self.__btnStepOnClick)

        # Processors' instruction labels
        self.__lblP1Instruction = self.findChild(QLabel, 'lblP1Instr')
        self.__lblP2Instruction = self.findChild(QLabel, 'lblP2Instr')
        self.__lblP3Instruction = self.findChild(QLabel, 'lblP3Instr')
        self.__lblP4Instruction = self.findChild(QLabel, 'lblP4Instr')

        # Processors' action labels
        self.__lblP1Action = self.findChild(QLabel, 'lblP1Action')
        self.__lblP2Action = self.findChild(QLabel, 'lblP2Action')
        self.__lblP3Action = self.findChild(QLabel, 'lblP3Action')
        self.__lblP4Action = self.findChild(QLabel, 'lblP4Action')

        # Processors' previous instruction labels
        self.__lblP1PInstruction = self.findChild(QLabel, 'lblP1PInstr')
        self.__lblP2PInstruction = self.findChild(QLabel, 'lblP2PInstr')
        self.__lblP3PInstruction = self.findChild(QLabel, 'lblP3PInstr')
        self.__lblP4PInstruction = self.findChild(QLabel, 'lblP4PInstr')

        # Cycle label
        self.__lblCycles = self.findChild(QLabel, 'lblCycles')

        # Frequency field
        self.__leFrequency = self.findChild(QLineEdit, 'leFrequency')

        # Max Cycles field
        self.__leMaxCycles = self.findChild(QLineEdit, 'leMaxCycles')

        # Cache tables
        self._cache_tables: list = [self.findChild(QTableWidget, 'tbP1L1Cache'),
                                    self.findChild(QTableWidget, 'tbP2L1Cache'),
                                    self.findChild(QTableWidget, 'tbP3L1Cache'),
                                    self.findChild(QTableWidget, 'tbP4L1Cache')]

        # Memory table
        self._tb_shared_mem: QTableWidget = self.findChild(QTableWidget,
                                                          'tbSharedMem')

        # Create system
        self.__system: System = System(4)

        # Create tables
        self.__initCacheTables()
        self.__initMemoryTable()

        # Create thread to update the GUI
        self.__t_update = Thread(target=self.__update)
        self.__t_update.start()

    def __btnRestartOnClick(self) -> None:
        """This method is executed when the restart button is pressed.
        Restarts all system.
        """
        # Stop current system
        self.__running = False
        self.__system.turn_off()
        self.__cycles = 0

        # Create a new system
        self.__system = System(4)

        # Enable the start button again
        self.__btnStart.setEnabled(True)

    def __btnStartOnClick(self) -> None:
        """This method is executed when the start button is pressed.
        Starts the system and disable the button.
        """
        try:
            # Get frequency
            self.__frequency: float = float(self.__leFrequency.text())

            if 0 < self.__frequency < 8:
                try:
                    # Get frequency
                    self.__total_cycles: int = int(self.__leMaxCycles.text())

                    # Restart cycles
                    self.__cycles = 0

                    # We need to wait every cycle
                    self.__wait = True

                    # Set clock frequency
                    self.__system.set_frequency(self.__frequency)

                    # Start system
                    self.__system.turn_on()
                    self.__running = True

                    # Desable button
                    self.__btnStart.setEnabled(False)
                except ValueError:
                    self.__showMessageDialog('Invalid max cycles!',
                                            'An integer number is required.',
                                            QMessageBox.Warning)
            else:
                self.__showMessageDialog('Invalid frequency!',
                        'Frequency must be greater than 0 and less then 8.',
                        QMessageBox.Warning)
        except ValueError:
            self.__showMessageDialog('Invalid frequency!',
                                    'A number is required.',
                                    QMessageBox.Warning)

    def __btnStepOnClick(self) -> None:
        """This method is executed when the start button is pressed.
        Run one step in the system.
        """
        # No wait
        self.__wait = False

        # Set clock frequency
        self.__system.set_frequency(self.__frequency)

        # Start system
        self.__system.turn_on(False)
        self.__running = True

    def __initCacheTables(self) -> None:
        """This method fills the cache table of each processor.
        """
        for i in range(len(self._cache_tables)):
            # Clear the table
            self._cache_tables[i].clear()

            # Get processor
            processor: Processor = self.__system.get_processor(i)

            for j, block in enumerate(processor.get_cache_mem()):
                # Compute address
                address = block['address']

                # Compute value
                value = '0x' + '0' * (4 - len(block['data'])) +\
                                        block['data']

                # Insert address
                self._cache_tables[i].setItem(j, 0,
                                QTableWidgetItem(address))
                # Insert value
                self._cache_tables[i].setItem(j, 1,
                                QTableWidgetItem(value))
                # Insert state
                self._cache_tables[i].setItem(j, 2,
                                QTableWidgetItem(block['state']))

    def __initMemoryTable(self) -> None:
        """This method fills the memory table.
        """
        self._tb_shared_mem.clear()
 
        for i in range(self.__system.get_shared_mem_size()):
            # Compute address
            address: str = bin(i)[2:]
            address = '0' * (4 - len(address)) + address

            # Compute value
            value: str = self.__system.read_shared_memory(address)
            value = '0x' + '0' * (4 - len(value)) + value
        
            # Insert address
            self._tb_shared_mem.setItem(i, 0,
                                    QTableWidgetItem(address))
            # Insert value
            self._tb_shared_mem.setItem(i, 1,
                                    QTableWidgetItem(value))

    def __showMessageDialog(self, title: str, msg: str,
                            icon=QMessageBox.Information,
                            buttons=[('Ok', QMessageBox.YesRole)]) -> int:
        """This method displays a message dialog with some important
        information for the user.

        Params
        --------------------------------------------------------------
            title: str
                Dialog title.
            msg: str
                Dialog message.
            icon: Icon
                Dialog icon. QMessageBox.Information by default,
            buttons: list
                Buttons to add. Must contain tuple with button message 
                and Button Role. [('Ok', QMessageBox.YesRole)] by
                default.

        Returns
        --------------------------------------------------------------
            Result corresponding to the user answer.
        """
        # Message Box
        msgBox = QMessageBox()

        # Icon, message and tittle
        msgBox.setIcon(icon)
        msgBox.setText(msg)
        msgBox.setWindowTitle(title)

        # Buttons
        for button in buttons:
            msgBox.addButton(QPushButton(button[0]), button[1])

        # Waits for the user answer and returns it
        return msgBox.exec_()

    def __update(self) -> None:
        """This method updates the window.
        """
        while (self.__opened):
            # Update cycles
            if (self.__running):
                self.__cycles += 1

                # Stop if it doesn't have to wait
                if not self.__wait:
                    self.__running = False
                else:
                    # Check it the cycles are not infinite
                    if self.__total_cycles > 0:
                        # Check if the cycles were completed
                        if self.__cycles == self.__total_cycles:
                            # And stop
                            sleep(0.5)
                            self.__system.turn_off()
                            self.__running = False
                            self.__btnStart.setEnabled(True)

            # Get instructions
            instructions = self.__system.get_instructions()
            old_instr = self.__system.get_old_instructions()

            # Set instruction text
            self.__lblP1Instruction.setText(instr2string(0, instructions[0]))
            self.__lblP2Instruction.setText(instr2string(1, instructions[1]))
            self.__lblP3Instruction.setText(instr2string(2, instructions[2]))
            self.__lblP4Instruction.setText(instr2string(3, instructions[3]))

            # Set processors actions
            self.__lblP1Action.setText(self.__system.get_processor(0).get_state())
            self.__lblP2Action.setText(self.__system.get_processor(1).get_state())
            self.__lblP3Action.setText(self.__system.get_processor(2).get_state())
            self.__lblP4Action.setText(self.__system.get_processor(3).get_state())

            self.__lblP1PInstruction.setText(instr2string(0, old_instr[0]))
            self.__lblP2PInstruction.setText(instr2string(1, old_instr[1]))
            self.__lblP3PInstruction.setText(instr2string(2, old_instr[2]))
            self.__lblP4PInstruction.setText(instr2string(3, old_instr[3]))

            # Set current cycle
            self.__lblCycles.setText(f'Cycle: {self.__cycles}')

            # Update tables
            self.__initCacheTables()
            self.__initMemoryTable()

            sleep(0.5)

    def closeEvent(self, event):
        """This method is called when the window closes.
        """
        self.__opened = False
        self.__running = False
        self.__system.turn_off()

