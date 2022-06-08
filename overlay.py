# Copyright (c) 2022 Eyeware Tech SA. All rights reserved.
#
# Licensed under the MIT License. See LICENSE file for license information.

# Qt libraries
from PySide6 import QtWidgets, QtGui, QtCore

# Built-in libraries
import time

CONST_MINIMAP_SIZE_AS_WIDTH_RATIO: float = 0.15
INSTRUCTIONS: str = "Select the region where the minimap is. Press ESC when ready."


class MinimapHighlightOverlay(QtWidgets.QDialog):
    """
    Overlay to raise attention to the minimap
    """
    _show_highlight: bool = False
    _start_time: float = time.time()

    def __init__(self, parent: QtWidgets.QWidget = None) -> None:
        super().__init__(parent)
        self.setWindowFlags(
            self.windowFlags()
            | QtCore.Qt.Window
            | QtCore.Qt.WindowStaysOnTopHint
            | QtCore.Qt.FramelessWindowHint
            | QtCore.Qt.X11BypassWindowManagerHint
        )
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.setAutoFillBackground(True)

        timer= QtCore.QTimer(self)
        timer.timeout.connect(self._update_highlight)
        timer.start(20)
    
    def showAndRestart(self) -> None:
        self._start_time: float = time.time() 
        self.show()
        self.raise_()
        self.update()

    # Painting event
    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        if self._show_highlight:
            painter = QtGui.QPainter(self)
            brush = QtGui.QBrush(QtGui.QColor(255, 0, 0, 100))
            painter.setBrush(brush)
            painter.drawRect(QtCore.QRect(QtCore.QPoint(0, 0), self.size()))
            painter.end()

    def _update_highlight(self) -> None:
        current_time = (time.time() - self._start_time) % 0.2
        previous_show_highlight = self._show_highlight
        self._show_highlight = current_time < 0.1
        if previous_show_highlight != self._show_highlight:
            self.update()


class MinimapSetupOverlay(QtWidgets.QDialog):
    _minimap_region: QtCore.QRect
    _mouse_pressed: bool = False
    _gaze_tolerance_in_percentage: float = 0.0

    def __init__(self, parent: QtWidgets.QWidget = None) -> None:
        super().__init__(parent)
        self.setWindowFlags(
            self.windowFlags()
            | QtCore.Qt.Window
            | QtCore.Qt.WindowStaysOnTopHint
            | QtCore.Qt.FramelessWindowHint
            | QtCore.Qt.X11BypassWindowManagerHint
            | QtCore.Qt.MaximizeUsingFullscreenGeometryHint
        )
        self.setMouseTracking(True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.setAutoFillBackground(True)
        self.setModal(True)
        self.move(QtCore.QPoint(0, 0))

        primary_screen = QtGui.QGuiApplication.instance().screenAt(QtCore.QPoint(0, 0))

        screen_geometry = primary_screen.geometry()

        minimap_size = int(CONST_MINIMAP_SIZE_AS_WIDTH_RATIO * screen_geometry.width())

        self._minimap_region = QtCore.QRect(
            screen_geometry.width() - minimap_size, screen_geometry.height() - minimap_size, minimap_size, minimap_size
        )

    def setGazeTolerance(self, tolerance_as_percentage_of_screen_width: float) -> None:
        """
        Sets the gaze tolerance by adding a percentage of the screen width
        """
        self._gaze_tolerance_in_percentage = tolerance_as_percentage_of_screen_width
        self.update()

    def getMinimapRegionWithGazeTolerance(self) -> QtCore.QRect:
        """
        Returns the minimap region defined by the user with an extra margin
        
        The extra margin is important because eye tracking is not 100% accurate.  

        Adding a margin thus prevents the detection of looking at minimap being overly sensitive and missing
        cases in which the user is actually looking at it, but the system does not detect that, which can be
        annoying if an alarm triggers. Making the margin too large may otherwise make the system believe that
        the user is looking at the minimap most of the time.

        Note: margin can partially account for peripheral vision.
        """
        margin = int((self._gaze_tolerance_in_percentage/100.0) * self.width() / 2.0)
        minimap_region_with_tolerance = self.getMinimapRegion().marginsAdded(
            QtCore.QMargins(margin, margin, margin, margin)
        )
        return minimap_region_with_tolerance

    def getMinimapRegion(self) -> QtCore.QRect:
        """
        Returns the minimap region as defined by the user
        """
        return self._minimap_region.normalized()

    # Setting the region through mouse events
    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.button() != QtCore.Qt.LeftButton:
            return super().mousePressEvent(event)
        self._minimap_region = QtCore.QRect(event.pos().x(), event.pos().y(), 1, 1)
        self._mouse_pressed = True
        self.update()

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        if self._mouse_pressed:
            self._minimap_region = QtCore.QRect(self._minimap_region.topLeft(), event.pos())
            self.update()

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.button() == QtCore.Qt.LeftButton:
            self._mouse_pressed = False
        return super().mouseReleaseEvent(event)

    # Stopping the setup
    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()
        return super().keyPressEvent(event)

    # Painting event
    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        painter = QtGui.QPainter(self)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 100))
        painter.setBrush(brush)
        painter.drawRect(self.geometry())
        
        pen = QtGui.QPen(QtGui.QColor(255, 255, 255))
        painter.setPen(pen)

        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0, 100))
        painter.setBrush(brush)
        painter.drawRect(self.getMinimapRegionWithGazeTolerance())

        brush = QtGui.QBrush(QtGui.QColor(255, 255, 0, 100))
        painter.setBrush(brush)

        painter.drawRect(self._minimap_region)

        font = painter.font()
        font.setPointSize(20)
        painter.setFont(font)

        painter.drawText(self.geometry(), QtCore.Qt.AlignCenter, INSTRUCTIONS)
        painter.end()
