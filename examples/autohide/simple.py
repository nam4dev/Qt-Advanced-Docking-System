from PySide6.QtWidgets import (
        QApplication,
        QMainWindow,
        QLabel,
    )
import PySide6QtAds

if __name__ == '__main__':

    app = QApplication()
    mw = QMainWindow()

    PySide6QtAds.CDockManager.setAutoHideConfigFlags(PySide6QtAds.CDockManager.eAutoHideFlag.DefaultAutoHideConfig)

    contents = QLabel("Main Widget")
    contents.setStyleSheet("background-color: lightblue;")

    central_dock = PySide6QtAds.CDockWidget("Central Dock", mw)
    central_dock.setWidget(contents)

    dock_manager = PySide6QtAds.CDockManager(mw)

    central_dock_area = dock_manager.setCentralWidget(central_dock)
    central_dock_area.setAllowedAreas(PySide6QtAds.DockWidgetArea.OuterDockAreas)

    side_contents = QLabel("Side dock (auto-hide)")
    side_contents.setStyleSheet("background-color: lightyellow;")

    dock = PySide6QtAds.CDockWidget("Demo", mw)
    dock.setWidget(side_contents)

    # Would expect to work
    """
        enum SideBarLocation
        {
            SideBarTop,
            SideBarLeft,
            SideBarRight,
            SideBarBottom,
            SideBarNone
        };
    """

    SideBarLocation = PySide6QtAds.ads.SideBarLocation

    dock_manager.addAutoHideDockWidget(SideBarLocation.SideBarRight, dock)
    mw.show()

    app.exec()
