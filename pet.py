import sys
from PyQt5.QtCore import Qt, QTimer, QPoint, QDateTime
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtGui import QFont, QColor

class DesktopPet(QWidget):
    def __init__(self):
        super().__init__()
        self.is_minimized = False
        self.drag_position = QPoint()
        self.initUI()

    def initUI(self):
        # 窗口属性：无边框、工具窗口（不在任务栏占用大图标）、窗口置顶
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground) # 背景透明

        # 主卡片样式
        self.main_style = """
            QWidget#MainCard {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #c8102e, stop:1 #8f0c1f);
                border: 2px solid #ffd766;
                border-radius: 16px;
            }
        """
        self.setObjectName("MainCard")
        self.setStyleSheet(self.main_style)
        self.setFixedSize(260, 160)

        # 布局构建
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(12, 8, 12, 12)

        # 1. 顶部标题栏
        header_layout = QHBoxLayout()
        title_label = QLabel("🎉 国庆倒计时", self)
        title_label.setStyleSheet("color: #ffd766; font-weight: bold; font-size: 13px;")
        
        btn_min = QPushButton("—", self)
        btn_min.setFixedSize(20, 20)
        btn_min.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.2);
                color: white;
                border-radius: 10px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: rgba(255, 255, 255, 0.4); }
        """)
        btn_min.clicked.connect(self.toggle_minimize)

        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(btn_min)
        self.layout.addLayout(header_layout)

        # 2. 中间倒计时显示区
        self.time_label = QLabel("00 : 00 : 00", self)
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setFont(QFont("Segoe UI", 22, QFont.Bold))
        self.time_label.setStyleSheet("color: #ffd766; margin-top: 5px;")
        self.layout.addWidget(self.time_label)

        # 3. 底部提示文案
        self.tip_label = QLabel("再坚持一下，下班奔向假期！🥳", self)
        self.tip_label.setAlignment(Qt.AlignCenter)
        self.tip_label.setStyleSheet("color: #ffffff; font-size: 12px; margin-top: 2px;")
        self.layout.addWidget(self.tip_label)

        # 定时器：每秒更新一次时间
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_countdown)
        self.timer.start(1000)
        self.update_countdown()

    def update_countdown(self):
        # 设定目标时间：2026年9月30日 20:00:00
        target = QDateTime.fromString("2026-09-30 20:00:00", "yyyy-MM-dd hh:mm:ss")
        now = QDateTime.currentDateTime()
        secs = now.secsTo(target)

        if secs <= 0:
            self.time_label.setText("下班啦！")
            self.tip_label.setText("🎉 国庆快乐，尽情享受假期！")
        else:
            hours = secs // 3600
            mins = (secs % 3600) // 60
            s = secs % 60
            self.time_label.setText(f"{hours:02d} : {mins:02d} : {s:02d}")

    def toggle_minimize(self):
        if not self.is_minimized:
            # 切换为圆形图标模式
            self.is_minimized = True
            self.setFixedSize(60, 60)
            self.setStyleSheet("""
                QWidget#MainCard {
                    background-color: #c8102e;
                    border: 2px solid #ffd766;
                    border-radius: 30px;
                }
            """)
            self.time_label.setText("🇨🇳")
            self.time_label.setFont(QFont("Segoe UI", 18))
            self.tip_label.hide()
        else:
            # 恢复卡片模式
            self.is_minimized = False
            self.setFixedSize(260, 160)
            self.setStyleSheet(self.main_style)
            self.time_label.setFont(QFont("Segoe UI", 22, QFont.Bold))
            self.tip_label.show()
            self.update_countdown()

    # 实现鼠标无边框拖拽
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    def mouseDoubleClickEvent(self, event):
        if self.is_minimized and event.button() == Qt.LeftButton:
            self.toggle_minimize()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pet = DesktopPet()
    pet.show()
    sys.exit(app.exec_())
