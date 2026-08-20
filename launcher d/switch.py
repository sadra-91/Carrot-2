from PyQt6.QtWidgets import QAbstractButton
from PyQt6.QtCore import Qt, QRectF, QPropertyAnimation, pyqtProperty, QEasingCurve
from PyQt6.QtGui import QPainter, QColor


class DeSwitch(QAbstractButton):
    def __init__(
        self,
        parent=None,
        width=54,
        height=30,
        active_color="#34C759",
        inactive_color="#5C5C5C",
        thumb_color="#FFFFFF",
    ):
        super().__init__(parent)

        self.setCheckable(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedSize(width, height)

        self._active_color = QColor(active_color)
        self._inactive_color = QColor(inactive_color)
        self._thumb_color = QColor(thumb_color)

        self._margin = 3
        self._diameter = height - self._margin * 2
        self._offset = self._margin

        self._animation = QPropertyAnimation(self, b"offset")
        self._animation.setDuration(180)
        self._animation.setEasingCurve(QEasingCurve.Type.OutCubic)

        self.toggled.connect(self._animate)

    def sizeHint(self):
        return self.size()

    @pyqtProperty(float)
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, value):
        self._offset = value
        self.update()

    def _animate(self, checked):
        self._animation.stop()
        self._animation.setStartValue(self._offset)

        if checked:
            end = self.width() - self._diameter - self._margin
        else:
            end = self._margin

        self._animation.setEndValue(end)
        self._animation.start()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        painter.setPen(Qt.PenStyle.NoPen)

        if self.isChecked():
            painter.setBrush(self._active_color)
        else:
            painter.setBrush(self._inactive_color)

        painter.drawRoundedRect(
            QRectF(0, 0, self.width(), self.height()),
            self.height() / 2,
            self.height() / 2,
        )

        painter.setBrush(self._thumb_color)
        painter.drawEllipse(
            QRectF(
                self._offset,
                self._margin,
                self._diameter,
                self._diameter,
            )
        )

    def mouseReleaseEvent(self, event):
        if (
            event.button() == Qt.MouseButton.LeftButton
            and self.rect().contains(event.position().toPoint())
        ):
            self.toggle()

        super().mouseReleaseEvent(event)

    def resizeEvent(self, event):
        self._diameter = self.height() - self._margin * 2

        if self.isChecked():
            self._offset = self.width() - self._diameter - self._margin
        else:
            self._offset = self._margin

        super().resizeEvent(event)

    def setColors(self, active=None, inactive=None, thumb=None):
        if active is not None:
            self._active_color = QColor(active)
        if inactive is not None:
            self._inactive_color = QColor(inactive)
        if thumb is not None:
            self._thumb_color = QColor(thumb)
        self.update()