from PyQt5 import QtWidgets, QtGui, QtCore, uic
from PyQt5.QtWidgets import QPushButton, QTableWidget, QTableWidgetItem

from hardware.system import System
from hardware.cpu.processor import Processor


class MainWindow(QtWidgets.QMainWindow):
    """Main Window class.
    """
    def __init__(self):
        """Constructor.
        """
        # Call the inherited classes __init__ method
        super(MainWindow, self).__init__()
        # Load the .ui file
        uic.loadUi('./gui/mainwindow.ui', self)

        # Components
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

        # Create 
        self.__init_cache_tables()
        self.__init_memory_table()

    def __init_cache_tables(self) -> None:
        """This method fills the cache table of each processor.
        """
        for i in range(len(self._cache_tables)):
            # Get processor
            processor: Processor = self.__system.get_processor(i)

            for j in range(processor.get_cache_size()):
                # Compute address
                address: str = bin(j)[2:]
                address = '0' * (2 - len(address)) + address

                # Compute value
                value: str = processor.get_mem_block(j)
                value = '0x' + '0' * (4 - len(value)) + value

                # Insert address
                self._cache_tables[i].setItem(j, 0,
                                QTableWidgetItem(address))
                # Insert value
                self._cache_tables[i].setItem(j, 1,
                                QTableWidgetItem(value))

    def __init_memory_table(self) -> None:
        """This method fills the memory table.
        """
        for i in range(self.__system.get_shared_mem_size()):
            # Compute address
            address: str = bin(i)[2:]
            address = '0' * (4 - len(address)) + address

            # Compute value
            value: str = self.__system.read_shared_memory(i)
            value = '0x' + '0' * (4 - len(value)) + value
        
            # Insert address
            self._tb_shared_mem.setItem(i, 0,
                                    QTableWidgetItem(address))
            # Insert value
            self._tb_shared_mem.setItem(i, 1,
                                    QTableWidgetItem(value))

