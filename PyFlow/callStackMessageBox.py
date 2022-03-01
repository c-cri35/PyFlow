import os
import sys
import traceback

from Qt.QtWidgets import QMessageBox, QTextEdit

cwd = os.getcwd()


def makePathRelative(path):
    if not os.path.isabs(path):
        return path

    prefix = os.path.commonpath([path, cwd])
    return path[len(prefix) + 1:]


def parseTraceback(e, value, tb):
    exception = "{}: {}".format(e.__name__, str(value))
    tracebackList = "\n".join(
        [
            f'File "{makePathRelative(file)}", line {line}, in {function}' + (f'\n\t{text}' if text else '')
            for file, line, function, text in traceback.extract_tb(tb)[::-1]
        ]
    )

    return "\n".join(
        ["Traceback (most recent call first):", tracebackList, exception]
    )


def showCallStackMessageBox(e: Exception, title: str, text: str = None):
    msgBox = QMessageBox(None)
    msgBox.setIcon(QMessageBox.Critical)
    msgBox.setWindowTitle(title)
    msgBox.setText(str(e) if text is None else text)
    msgBox.setDetailedText(parseTraceback(*sys.exc_info()))

    # show details by default
    for button in msgBox.buttons():
        if msgBox.buttonRole(button) == QMessageBox.ActionRole:
            button.click()
            break

    # adapt size to better show the callstack
    textBoxes = msgBox.findChildren(QTextEdit)
    if textBoxes:
        textBoxes[0].setFixedSize(750, 250)

    msgBox.exec()
