from main import *
#from src.GUI.new_main import MainWindow


class UIFunctions(MainWindow):

    def toggleMenu(self, maxWidth, enable):
        if enable:
            # Get Width
            width = self.mainWindow.frame_left_menu.width()
            standard = 70

            # Set Max Width
            if width == 70:
                widthExtended = maxWidth
            else:
                widthExtended = standard

            # Animation
            self.animation = QPropertyAnimation(self.mainWindow.frame_left_menu, b"minimumWidth")
            self.animation.setDuration(400)
            self.animation.setStartValue(width)
            self.animation.setEndValue(widthExtended)
            self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation.start()