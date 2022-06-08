# Copyright (c) 2022 Eyeware Tech SA. All rights reserved.
#
# Licensed under the MIT License. See LICENSE file for license information.


# User interface
from PySide6 import QtWidgets, QtCore, QtMultimedia
from overlay import MinimapSetupOverlay, MinimapHighlightOverlay

# Import Eyeware Beam's SDK
from eyeware.client import TrackerClient

# Built-in libs
import sys
import os

MAIN_PATH = os.path.abspath(os.path.dirname(__file__))


class MainWindow(QtWidgets.QMainWindow):
    # UI
    _capture_minimap_button: QtWidgets.QPushButton
    _start_stop_button: QtWidgets.QPushButton
    _alarm_time_input: QtWidgets.QDoubleSpinBox
    _minimap_tolerance_spinbox: QtWidgets.QDoubleSpinBox
    _minimap_setup_overlay: MinimapSetupOverlay
    _minimap_highlight_overlay: MinimapHighlightOverlay
    _volume_slider: QtWidgets.QSlider
    _connected_label: QtWidgets.QLabel
    _show_alarm_overlay_check: QtWidgets.QCheckBox
    # Alarm and audio feedback
    _alarm_timer: QtCore.QTimer
    _media_player: QtMultimedia.QMediaPlayer
    _audio_output: QtMultimedia.QAudioOutput
    # Eye tracking
    _tracker: TrackerClient
    _tracker_polling: QtCore.QTimer
    _gaze_on_minimap: bool = False

    # Main state
    _running: bool = False

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Minimap trainer")

        self.setMinimumWidth(400)

        self._init_user_interface()
        self._init_minimap_alarm()
        self._init_eye_tracking()

    def _init_user_interface(self) -> None:
        """
        Creates the related widget and user interface
        """
        main_frame: QtWidgets.QFrame() = QtWidgets.QFrame(self)
        self._capture_minimap_button: QtWidgets.QPushButton = QtWidgets.QPushButton("Set minimap location", self)
        self._capture_minimap_button.clicked.connect(self._onMinimapSetupOverlayClicked)

        self._start_stop_button = QtWidgets.QPushButton("Start", self)
        self._start_stop_button.clicked.connect(self._onAlarmStartStoppedClicked)

        self._minimap_setup_overlay = MinimapSetupOverlay(self)
        self._minimap_highlight_overlay = MinimapHighlightOverlay(self)

        self._connected_label = QtWidgets.QLabel()

        minimap_settings_box: QtWidgets.QGroupBox = QtWidgets.QGroupBox("Minimap settings", self)
        self._minimap_tolerance_spinbox = QtWidgets.QDoubleSpinBox(minimap_settings_box)
        self._minimap_tolerance_spinbox.setMinimum(0.0)
        self._minimap_tolerance_spinbox.setMaximum(100.0)
        self._minimap_tolerance_spinbox.setValue(10)
        self._minimap_tolerance_spinbox.valueChanged.connect(self._onGazeToleranceChanged)
        self._minimap_setup_overlay.setGazeTolerance(self._minimap_tolerance_spinbox.value())
        minimap_settings_layout: QtWidgets.QGridLayout = QtWidgets.QGridLayout()
        minimap_settings_layout.addWidget(QtWidgets.QLabel("Gaze tolerance (%)", minimap_settings_box), 0, 0)
        minimap_settings_layout.addWidget(self._minimap_tolerance_spinbox, 0, 1)
        minimap_settings_layout.addWidget(self._capture_minimap_button, 1, 0, 1, 2)
        minimap_settings_box.setLayout(minimap_settings_layout)

        time_box: QtWidgets.QGroupBox = QtWidgets.QGroupBox("Trainer settings", self)
        self._volume_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, time_box)
        self._volume_slider.setMinimum(0)
        self._volume_slider.setMaximum(99)
        self._volume_slider.setValue(50)
        self._volume_slider.valueChanged.connect(self._onVolumeChanged)

        self._alarm_time_input = QtWidgets.QDoubleSpinBox(time_box)
        self._alarm_time_input.setMinimum(0.5)
        self._alarm_time_input.setMaximum(60)
        self._alarm_time_input.setSingleStep(0.1)
        self._alarm_time_input.setValue(3.0)

        self._show_alarm_overlay_check = QtWidgets.QCheckBox(self)
        self._show_alarm_overlay_check.setChecked(True)

        time_layout: QtWidgets.QGridLayout = QtWidgets.QGridLayout()
        time_layout.addWidget(QtWidgets.QLabel("Alarm timeout (seconds) ", time_box), 0, 0)
        time_layout.addWidget(self._alarm_time_input, 0, 1)
        time_layout.addWidget(QtWidgets.QLabel("Volume", time_box), 1, 0)
        time_layout.addWidget(self._volume_slider, 1, 1)
        time_layout.addWidget(QtWidgets.QLabel("Visual alarm", time_box), 2, 0)
        time_layout.addWidget(self._show_alarm_overlay_check, 2, 1)
        time_box.setLayout(time_layout)

        main_layout: QtWidgets.QVBoxLayout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(minimap_settings_box)
        main_layout.addWidget(time_box)
        main_layout.addWidget(self._start_stop_button)
        main_layout.addWidget(self._connected_label)

        main_frame.setLayout(main_layout)

        self.setCentralWidget(main_frame)

    def _init_minimap_alarm(self) -> None:
        """
        Initializes the alarm logic
        """
        self._audio_output = QtMultimedia.QAudioOutput(self)
        self._media_player = QtMultimedia.QMediaPlayer(self)
        self._media_player.setAudioOutput(self._audio_output)
        self._media_player.setLoops(-1)
        self._media_player.setSource(QtCore.QUrl.fromLocalFile(os.path.join(MAIN_PATH, "alarm.mp3")))
        self._audio_output.setVolume(0.5)

        self._alarm_timer = QtCore.QTimer(self)
        self._alarm_timer.setSingleShot(True)
        self._alarm_timer.timeout.connect(self._onAlarmTriggered)

    def _init_eye_tracking(self) -> None:
        """
        Initializes the connection with Eyeware Beam's tracking API
        """
        self._tracker = TrackerClient()
        self._tracker_polling = QtCore.QTimer(self)
        self._tracker_polling.timeout.connect(self._updateTrackingData)
        self._tracker_polling.start(33)

    def _updateTrackingData(self) -> None:
        """
        Fetch (periodically) tracking data, including gaze on the screen
        """
        if self._tracker.connected:
            self._connected_label.setText("Connected to eye tracker...")
            head_pose = self._tracker.get_head_pose_info()
            if not head_pose.is_lost:
                screen_gaze = self._tracker.get_screen_gaze_info()
                if not screen_gaze.is_lost:
                    minimap_region = self._minimap_setup_overlay.getMinimapRegionWithGazeTolerance()
                    gaze_on_minimap = minimap_region.contains(screen_gaze.x, screen_gaze.y)
                    if gaze_on_minimap:
                        self._restart_timer()
                return
        else:
            self._connected_label.setText("Disconnected from eye tracker...")
        # We restart the timer if the app is disconnected or the user is not being tracked. Otherwise, it
        # can be a bit annoying
        self._restart_timer()

    def _onMinimapSetupOverlayClicked(self) -> None:
        """
        Whether to open the overlay which allows the user to configure the minimap location
        """
        if not self._minimap_setup_overlay.isVisible():
            self._minimap_setup_overlay.showMaximized()
            self._minimap_setup_overlay.raise_()
        else:
            self._minimap_setup_overlay.hide()

    def _onAlarmStartStoppedClicked(self) -> None:
        """
        Process the user clicking on starting or stopping the gaze sensitive alarm
        """
        self._running = not self._running
        self._alarm_time_input.setEnabled(not self._running)
        self._capture_minimap_button.setEnabled(not self._running)
        self._show_alarm_overlay_check.setEnabled(not self._running)
        if self._running:
            self._restart_timer()
            self._start_stop_button.setText("Stop")
        else:
            self._alarm_timer.stop()
            self._media_player.stop()
            self._minimap_highlight_overlay.hide()
            self._start_stop_button.setText("Start")

    def _onGazeToleranceChanged(self, value: float) -> None:
        self._minimap_setup_overlay.setGazeTolerance(value)

    def _onVolumeChanged(self, value: int) -> None:
        self._audio_output.setVolume(value/100)

    def _restart_timer(self) -> None:
        """
        Restarts the time the user has left to look at the minimap
        """
        if self._running:
            self._alarm_timer.start(self._alarm_time_input.value() * 1000)
            self._media_player.stop()
            self._minimap_highlight_overlay.hide()

    def _onAlarmTriggered(self) -> None:
        """
        Called when the alarm goes off, i.e, when the player hasn't seen the minimap for longer than the timer
        """
        if self._show_alarm_overlay_check.isChecked():
            self._minimap_highlight_overlay.setGeometry(self._minimap_setup_overlay.getMinimapRegion())
            self._minimap_highlight_overlay.showAndRestart()
        self._media_player.play()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
