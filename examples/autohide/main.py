import os

os.environ['QT_QUICK_BACKEND'] = 'software'
os.environ['QT_WEBENGINE_DISABLE_GPU'] = '1'

import sys
import win32con
import win32gui

from qtpy.QtUiTools import loadUiType
import win32con
import win32gui
from qtpy.QtUiTools import loadUiType
from qtpy import QtCore
from qtpy import QtGui
from qtpy import QtWidgets

from qtpy.QtWebEngineWidgets import QWebEngineView
from qtpy.QtWebEngineWidgets import QWebEngineSettings

try:
    import PyQtAds as QtAds
except (ImportError, NameError, Exception):
    import PySide6QtAds as QtAds

UI_FILE = os.path.join(os.path.dirname(__file__), 'mainwindow.ui')
MainWindowUI, MainWindowBase = loadUiType(UI_FILE)


class MainWindow(MainWindowUI, MainWindowBase):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._hwnd = None

        self.setupUi(self)
 
        QtAds.CDockManager.setConfigFlag(QtAds.CDockManager.eConfigFlag.OpaqueSplitterResize, True)
        QtAds.CDockManager.setConfigFlag(QtAds.CDockManager.eConfigFlag.XmlCompressionEnabled, False)
        QtAds.CDockManager.setConfigFlag(QtAds.CDockManager.eConfigFlag.FocusHighlighting, True)
        QtAds.CDockManager.setConfigFlag(QtAds.CDockManager.eConfigFlag.EnableFloatingAsWindow, True)
        QtAds.CDockManager.setAutoHideConfigFlags(QtAds.CDockManager.eAutoHideFlag.DefaultAutoHideConfig)
        self.dock_manager = QtAds.CDockManager(self)

        # Set central widget
        text_edit = QtWidgets.QPlainTextEdit()
        text_edit.setPlaceholderText("This is the central editor. Enter your text here.")
        central_dock_widget = QtAds.CDockWidget("CentralWidget")
        central_dock_widget.setWidget(text_edit)
        central_dock_area = self.dock_manager.setCentralWidget(central_dock_widget)
        central_dock_area.setAllowedAreas(QtAds.DockWidgetArea.OuterDockAreas)

        # create other dock widgets
        table = QtWidgets.QTableWidget()
        table.setColumnCount(3)
        table.setRowCount(10)
        table_dock_widget = QtAds.CDockWidget("Table 1")
        table_dock_widget.setWidget(table)
        table_dock_widget.setMinimumSizeHintMode(QtAds.CDockWidget.MinimumSizeHintFromDockWidget)
        table_dock_widget.resize(250, 150)
        table_dock_widget.setMinimumSize(200, 150)
        container = self.dock_manager.addAutoHideDockWidget(QtAds.SideBarLocation.SideBarLeft, table_dock_widget)
        container.setSize(480)
        self.menuView.addAction(table_dock_widget.toggleViewAction())
        
        table = QtWidgets.QTableWidget()
        table.setColumnCount(5)
        table.setRowCount(1020)
        table_dock_widget = QtAds.CDockWidget("Table 2")
        table_dock_widget.setWidget(table)
        table_dock_widget.setMinimumSizeHintMode(QtAds.CDockWidget.MinimumSizeHintFromDockWidget)
        table_dock_widget.resize(250, 150)
        table_dock_widget.setMinimumSize(200, 150)
        self.dock_manager.addAutoHideDockWidget(QtAds.SideBarLocation.SideBarLeft, table_dock_widget)
        self.menuView.addAction(table_dock_widget.toggleViewAction())

        properties_table = QtWidgets.QTableWidget()
        properties_table.setColumnCount(3)
        properties_table.setRowCount(10)
        properties_dock_widget = QtAds.CDockWidget("Properties")
        properties_dock_widget.setWidget(properties_table)
        properties_dock_widget.setMinimumSizeHintMode(QtAds.CDockWidget.MinimumSizeHintFromDockWidget)
        properties_dock_widget.resize(250, 150)
        properties_dock_widget.setMinimumSize(200, 150)
        self.dock_manager.addDockWidget(QtAds.DockWidgetArea.RightDockWidgetArea, properties_dock_widget, central_dock_area)
        self.menuView.addAction(properties_dock_widget.toggleViewAction())

        # Initialize QWebEngineView
        self.browser = QWebEngineView()

        # Access default settings for QWebEngine
        settings = self.browser.settings()  # Different from PyQt5, no defaultSettings method in qtpy
        settings.setAttribute(QWebEngineSettings.WebAttribute.Accelerated2dCanvasEnabled, False)
        settings.setAttribute(QWebEngineSettings.WebAttribute.WebGLEnabled, False)

        self.webview_dock_widget = QtAds.CDockWidget("Web Viewer")
        self.webview_dock_widget.setWidget(self.browser)
        self.webview_dock_widget.setMinimumSizeHintMode(QtAds.CDockWidget.eMinimumSizeHintMode.MinimumSizeHintFromDockWidget)
        self.webview_dock_widget.resize(600, 300)
        self.webview_dock_widget.setMinimumSize(600, 300)

        self.dock_manager.addAutoHideDockWidget(QtAds.SideBarLocation.SideBarBottom, self.webview_dock_widget)
        self.menuView.addAction(self.webview_dock_widget.toggleViewAction())

        self.create_perspective_ui()

        # self.webview_dock_widget.topLevelChanged.connect(self.to_single_window)
        # self.webview_dock_widget.visibilityChanged.connect(self.onVisibilityChanged)

        self.browser.load(QtCore.QUrl('https://github.com/nam4dev/pyside6_qtads/blob/main/README.md'))

    def to_single_window(self, floating: bool):
        self._hwnd = None

        if not floating:
            return

        dock_widget: QtAds.CDockWidget = self.sender()
        container = dock_widget.floatingDockContainer()
        if not container:
            return

        hwnd = int(container.winId())

        print('container', hwnd, container)

        container.setWindowFlags(
            Qt.WindowType.Window
            # | Qt.WindowType.WindowSystemMenuHint
            | Qt.WindowType.WindowMinMaxButtonsHint
            | Qt.WindowType.WindowCloseButtonHint
        )

        # # Set window style to ensure it appears as a separate floating window
        # style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
        # style |= win32con.WS_OVERLAPPEDWINDOW
        # win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE, style)

        # Set extended window style to ensure it gets its own taskbar entry
        style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, style | win32con.WS_EX_APPWINDOW)

        # Re-show the window to apply new styles
        win32gui.ShowWindow(hwnd, win32con.SW_SHOW)

    def create_perspective_ui(self):
        save_perspective_action = QtWidgets.QAction("Create Perspective", self)
        save_perspective_action.triggered.connect(self.save_perspective)
        perspective_list_action = QtWidgets.QWidgetAction(self)
        self.perspective_combobox = QtWidgets.QComboBox(self)
        self.perspective_combobox.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self.perspective_combobox.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.perspective_combobox.activated[int].connect(self.dock_manager.openPerspective)
        perspective_list_action.setDefaultWidget(self.perspective_combobox)
        self.toolBar.addSeparator()
        self.toolBar.addAction(perspective_list_action)
        self.toolBar.addAction(save_perspective_action)

    def save_perspective(self):
        perspective_name, ok = QtWidgets.QInputDialog.getText(self, "Save Perspective", "Enter Unique name:")
        if not ok or not perspective_name:
            return

        self.dock_manager.addPerspective(perspective_name)
        blocker = QtCore.QSignalBlocker(self.perspective_combobox)
        self.perspective_combobox.clear()
        self.perspective_combobox.addItems(self.dock_manager.perspectiveNames())
        self.perspective_combobox.setCurrentText(perspective_name)

    def closeEvent(self, event: QtGui.QCloseEvent):
        self.dock_manager.deleteLater()
        super().closeEvent(event)


if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.ApplicationAttribute.AA_EnableHighDpiScaling)

    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec()
