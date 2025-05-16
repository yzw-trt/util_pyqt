import sys
from PySide6.QtWidgets import QApplication, QWidget, QLineEdit, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator


class wheel_LineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFocusPolicy(Qt.StrongFocus)

        # 添加最大值和最小值属性
        self._minimum = float("-inf")
        self._maximum = float("inf")

        # 设置验证器，只允许输入数字和一个小数点
        reg = QRegularExpression(r"^-?\d*\.?\d*$")
        validator = QRegularExpressionValidator(reg)
        self.setValidator(validator)

    def focusOutEvent(self, event):
        # 失去焦点时检查和格式化输入
        text = self.text()
        if text:
            try:
                if text.endswith("."):
                    self.setText(text + "0")
                elif text == "-":
                    self.setText("0")
                elif text == "-.":
                    self.setText("-0.0")
            except ValueError:
                self.setText("0")
        super().focusOutEvent(event)

    def wheelEvent(self, event):
        cursor = self.cursorPosition()
        text = self.text()
        idx = max((cursor - 1), 0)

        try:
            # 检查光标位置是否在数字或小数点上
            if idx < len(text) and (text[idx].isdigit() or text[idx] == "."):
                # 将文本转换为浮点数
                num = float(text) if "." in text else int(text)
                delta = event.angleDelta().y()

                # 计算光标位置对应的小数位数
                decimal_pos = text.find(".")
                if decimal_pos == -1:  # 整数
                    v = 10 ** (len(text) - cursor)
                else:  # 小数
                    if cursor <= decimal_pos:  # 光标在小数点左边
                        v = 10 ** (decimal_pos - cursor)
                    else:  # 光标在小数点右边
                        v = 10 ** (decimal_pos - cursor + 1)

                # 根据滚轮方向增加或减少值
                if delta > 0:
                    num += v
                else:
                    num -= v

                # 检查是否超出范围限制
                if num < self._minimum:
                    num = self._minimum
                elif num > self._maximum:
                    num = self._maximum

                # 保持原有的小数位数
                if "." in text:
                    decimal_places = len(text[text.find(".") + 1 :])
                    text2 = f"{num:.{decimal_places}f}"
                else:
                    # text2 = str(int(num))
                    text2 = str(num)

                self.setText(text2)
                # 调整光标位置
                new_cursor = min(cursor, len(text2))
                self.setCursorPosition(new_cursor)

        except ValueError:
            pass  # 如果输入的不是有效数字，忽略滚轮事件

        event.accept()

    def value(self):
        # 返回当前输入的值，转换为浮点数
        text = self.text()
        if text:
            try:
                return float(text)
            except ValueError:
                return 0.0
        return 0.0

    def setValue(self, value):
        # 设置输入框的值
        if isinstance(value, (int, float)):
            self.setText(str(value))
        else:
            raise ValueError("Value must be an int or float.")

    def setRange(self, minimum, maximum):
        """设置数值范围"""
        if minimum > maximum:
            minimum, maximum = maximum, minimum
        self._minimum = float(minimum)
        self._maximum = float(maximum)

        # 检查当前值是否在新范围内
        current = self.value()
        if current < minimum:
            self.setValue(minimum)
        elif current > maximum:
            self.setValue(maximum)

    def clearRange(self):
        """清除范围限制"""
        self._minimum = float("-inf")
        self._maximum = float("inf")


class showExample(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("数字输入框")
        self.setGeometry(100, 100, 300, 100)

        self.layout = QVBoxLayout()

        self.label = QLabel("输入数字:")
        self.layout.addWidget(self.label)

        self.input_field = wheel_LineEdit(self)
        self.input_field.setPlaceholderText("输入数字")
        self.input_field.setMaxLength(15)  # 增加最大长度以适应小数
        self.input_field.setAlignment(Qt.AlignRight)
        self.layout.addWidget(self.input_field)
        self.setLayout(self.layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = showExample()
    widget.show()
    sys.exit(app.exec())
