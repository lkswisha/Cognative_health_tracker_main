#Making an edit

from datetime import datetime
import canvas
import pandas as pd
import sys, os
import platform
import webbrowser
import random
import pyautogui
import csv
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf
from datetime import date
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt, QEvent)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence,
                           QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PySide2.QtWidgets import *
from PySide2.QtUiTools import QUiLoader
from CogTests import VIP
from CogTests import GameMain
from CogTests import TrailBlazer
import global_variables as gv

# GUI FILE

# IMPORT FUNCTIONS
from csv_handler import *
from CogTests.GameMain import SaccadeTest
from ui_functions import *

windowHeightOffset = 60
winDimension = pyautogui.size()

# Handle high resolution displays:

"""
Class Definition for whole GUI window for the clinician portal and its elements
"""
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        file = QtCore.QFile("UI Files/ui_main.ui")
        if not file.open(QtCore.QFile.ReadOnly):
            print(f"Cannot open {file}: {file.errorString()}")
            sys.exit(-1)
        self.mainWindow = loader.load(file)
        file.close()
        if not self.mainWindow:
            print(loader.errorString())
            sys.exit(-1)

        # self.mainWindow.showMaximized()
        self.mainWindow.resize(winDimension[0], winDimension[1]-windowHeightOffset)
        self.mainWindow.show()
        # print(pyautogui.size())

        self.populatePatients()
        #Changing the Patient Page label in the UI for the Patient Window
        self.mainWindow.patientPage_label_2.setFont(QFont("Helvetica", 32))
        self.mainWindow.patientPage_label_2.move(winDimension[0] / 6-20, windowHeightOffset/2)

        #Changing the tree elements which contains the patient information
        self.mainWindow.treeWidget_2.resize(winDimension[0]-3*windowHeightOffset,winDimension[1]-6*windowHeightOffset)
        self.mainWindow.treeWidget_2.move(windowHeightOffset/2,2*windowHeightOffset)
        QTreeView.header(self.mainWindow.treeWidget_2).resizeSection(0, self.mainWindow.width() / 6)
        QTreeView.header(self.mainWindow.treeWidget_2).resizeSection(1, self.mainWindow.width() / 6)
        QTreeView.header(self.mainWindow.treeWidget_2).resizeSection(2, self.mainWindow.width() / 6)
        QTreeView.header(self.mainWindow.treeWidget_2).resizeSection(3, self.mainWindow.width() / 6)
        QTreeView.header(self.mainWindow.treeWidget_2).resizeSection(4, self.mainWindow.width() / 6)
        QTreeView.header(self.mainWindow.treeWidget_2).resizeSection(5, self.mainWindow.width() / 6)

        # Changing the Register Button in the UI for the Patient Window
        self.mainWindow.btn_register_2.setFont(QFont("Helvetica", 16))
        self.mainWindow.btn_register_2.move(0.8*winDimension[0] , winDimension[1] - 4 * windowHeightOffset)
        self.mainWindow.btn_register_2.resize(275, 50)

        # placing all the elements based on device resolution also dont know why resizing works here :(
        # self.mainWindow.register_firstName.setFo

        #Changing the Patient Data label in the UI for the Register Patient Page
        self.mainWindow.patientDataLabel.setFont(QFont("Helvetica", 32))
        self.mainWindow.patientDataLabel.move(4 * winDimension[0] / 10, windowHeightOffset)

        # Changing the First Name label in the UI for the Register Patient Page
        self.mainWindow.firstNameLabel.setFont(QFont("Helvetica", 16))
        self.mainWindow.firstNameLabel.move(winDimension[0] / 3, 3 * windowHeightOffset)

        # Changing the First Name input box in the UI for the Register Patient Page
        self.mainWindow.register_firstName.move(winDimension[0] / 3 + 260, 3 * windowHeightOffset + 15)

        # Changing the Last Name label in the UI for the Register Patient Page
        self.mainWindow.lastNameLabel.setFont(QFont("Helvetica", 16))
        self.mainWindow.lastNameLabel.move(winDimension[0] / 3, 4 * windowHeightOffset)

        # Changing the Last Name input box in the UI for the Register Patient Page
        self.mainWindow.register_lastName.move(winDimension[0] / 3 + 260, 4 * windowHeightOffset + 15)

        # Changing the User Name label in the UI for the Register Patient Page
        self.mainWindow.userIdLabel.setFont(QFont("Helvetica", 16))
        self.mainWindow.userIdLabel.move(winDimension[0] / 3, 5 * windowHeightOffset)

        # Changing the User Name input box in the UI for the Register Patient Page
        self.mainWindow.register_userId.move(winDimension[0] / 3 + 260, 5 * windowHeightOffset + 15)

        # Changing the Password label in the UI for the Register Patient Page
        self.mainWindow.passwordLabel.setFont(QFont("Helvetica", 16))
        self.mainWindow.passwordLabel.move(winDimension[0] / 3, 6 * windowHeightOffset)

        # Changing the Password input box in the UI for the Register Patient Page
        self.mainWindow.register_password.move(winDimension[0] / 3 + 260, 6 * windowHeightOffset + 15)

        # Changing the Confirm Password label in the UI for the Register Patient Page
        self.mainWindow.confirmPassLabel.setFont(QFont("Helvetica", 16))
        self.mainWindow.confirmPassLabel.move(winDimension[0] / 3, 7 * windowHeightOffset)

        # Changing the Confirm Password input box in the UI for the Register Patient Page
        self.mainWindow.register_confirmPassword.move(winDimension[0] / 3 + 260, 7 * windowHeightOffset + 15)

        # Changing the Organization label in the UI for the Register Patient Page
        self.mainWindow.organizationLabel.setFont(QFont("Helvetica", 16))
        self.mainWindow.organizationLabel.move(winDimension[0] / 3, 8 * windowHeightOffset)

        # Changing the Organization input box in the UI for the Register Patient Page
        self.mainWindow.register_organization.move(winDimension[0] / 3 + 260, 8 * windowHeightOffset + 15)

        # Changing the Role label in the UI for the Register Patient Page
        self.mainWindow.roleLabel.setFont(QFont("Helvetica", 16))
        self.mainWindow.roleLabel.move(winDimension[0] / 3, 9 * windowHeightOffset)

        # Changing the Role input box in the UI for the Register Patient Page
        self.mainWindow.register_role.move(winDimension[0] / 3 + 260, 9 * windowHeightOffset + 15)

        # Changing the Birthday label in the UI for the Register Patient Page
        self.mainWindow.birthdayLabel.setFont(QFont("Helvetica", 16))
        self.mainWindow.birthdayLabel.move(winDimension[0] / 3, 10 * windowHeightOffset)

        # Changing the Birthday input box in the UI for the Register Patient Page
        self.mainWindow.register_bday.move(winDimension[0] / 3 + 260, 10 * windowHeightOffset + 15)

        # Changing the Register in the UI for the Register Patient Page
        self.mainWindow.registerBtn.setFont(QFont("Helvetica", 16))
        self.mainWindow.registerBtn.move(0.8*winDimension[0], winDimension[1] - 4 * windowHeightOffset)
        self.mainWindow.registerBtn.resize(275, 50)

        ## TOGGLE/BURGUER MENU
        self.mainWindow.btn_toggle.clicked.connect(lambda: UIFunctions.toggleMenu(self, 250, True))

        # Contains the current username
        self.user=""

        # Ordering Test Messages
        self.orderTestSuccess = "Tests have been ordered for the patient"
        self.orderTestFail = "Tests have not been ordered for the patient"

        ## PAGES

        # Home Page
        self.mainWindow.btn_home.clicked.connect(
            lambda: self.mainWindow.Pages_Widget.setCurrentWidget(self.mainWindow.MainPage))

        # Changing Home Screen Image Elements in the Home Page
        self.mainWindow.main_label.setPixmap(QtGui.QPixmap(gv.path_to_images + 'esmetrics.jpg'))
        self.mainWindow.main_label.setScaledContents(True)
        self.mainWindow.main_label.move(winDimension[0] / 4, winDimension[1] / 4)

        # Changing the Copyright label line 1 in the Home Page
        self.mainWindow.copyrightLabel1.setFont(QFont('Helvetica', 10))
        self.mainWindow.copyrightLabel1.move(winDimension[0] / 3 - 2 * windowHeightOffset,
                                             0.5 * winDimension[1] + 0.04 * winDimension[1])

        # Changing the Copyright label line 2 in the Home Page
        self.mainWindow.copyrightLabel2.setFont(QFont('Helvetica', 10))
        self.mainWindow.copyrightLabel2.move(winDimension[0] / 3 - 2 * windowHeightOffset,
                                             0.5 * winDimension[1] + 0.08 * winDimension[1])

        # Changing the Copyright label line 3 in the Home Page
        self.mainWindow.copyrightLabel3.setFont(QFont('Helvetica', 10))
        self.mainWindow.copyrightLabel3.move(winDimension[0] / 3 - 2 * windowHeightOffset,
                                             0.5 * winDimension[1] + 0.12 * winDimension[1])

        # Changing the Copyright label line 4 in the Home Page
        self.mainWindow.copyrightLabel4.setFont(QFont('Helvetica', 10))
        self.mainWindow.copyrightLabel4.move(winDimension[0] / 3 - 2 * windowHeightOffset,
                                             0.5 * winDimension[1] + 0.16 * winDimension[1])

        # Changing the Copyright label line 5 in the Home Page
        self.mainWindow.copyrightLabel5.setFont(QFont('Helvetica', 10))
        self.mainWindow.copyrightLabel5.move(winDimension[0] / 3 - 2 * windowHeightOffset,
                                             0.5 * winDimension[1] + 0.2 * winDimension[1])

        # Changing the Copyright label line 6 in the Home Page
        self.mainWindow.copyrightLabel6.setFont(QFont('Helvetica', 10))
        self.mainWindow.copyrightLabel6.move(winDimension[0] / 3 - 2 * windowHeightOffset,
                                             0.5 * winDimension[1] + 0.24 * winDimension[1])

        # Changing the Copyright label line 7 in the Home Page
        self.mainWindow.copyrightLabel7.setFont(QFont('Helvetica', 10))
        self.mainWindow.copyrightLabel7.move(winDimension[0] / 3 - 2 * windowHeightOffset,
                                             0.5 * winDimension[1] + 0.28 * winDimension[1])

        ## Currently Disabled
        # Settings Page
        #self.mainWindow.btn_settings.clicked.connect(
            #lambda: self.mainWindow.Pages_Widget.setCurrentWidget(self.mainWindow.SettingsPage))

        # When the Patients Button is clicked, it will go to the patientsPageSetup() function
        self.mainWindow.btn_patients_test.clicked.connect(
            self.patientPageSetup)

        # Register Patients Page
        self.mainWindow.btn_register_2.clicked.connect(
            lambda: self.mainWindow.Pages_Widget.setCurrentWidget(self.mainWindow.RegisterPage))
        # self.mainWindow.setFont(QFont('Helvetica',))
        # self.mainWindow.label.move()

        # Help Page
        self.mainWindow.btn_help.clicked.connect(
            self.openHelpDoc)
        # lambda: self.mainWindow.Pages_Widget.setCurrentWidget(self.mainWindow.HelpPage))

        # Results Page
        # self.mainWindow.btn_results.clicked.connect(
        # lambda: self.mainWindow.Pages_Widget.setCurrentWidget(self.mainWindow.ResultsPage))

        # Tests Page
        self.mainWindow.btn_tests.clicked.connect(
            lambda: self.mainWindow.Pages_Widget.setCurrentWidget(self.mainWindow.TestsPage))

        # Changing the Tests label in the the test practice window
        self.mainWindow.tests_label.setFont(QFont('Helvetica',32))
        self.mainWindow.tests_label.move(winDimension[0]/4,0)

        # Setting the VIP test Button
        self.mainWindow.vip_btn.setGeometry(winDimension[0] / 6, winDimension[1] / 6,
                                            winDimension[0] / 4, winDimension[1] / 4)

        # Setting the Saccade test Button
        self.mainWindow.sas_btn.setGeometry(3*winDimension[0] / 6, winDimension[1] / 6,
                                            winDimension[0] / 4, winDimension[1] / 4)

        # Setting the Trailblazer test Button
        self.mainWindow.tb_btn.setGeometry(winDimension[0] / 6, 3*winDimension[1] / 6,
                                            winDimension[0] / 4, winDimension[1] / 4)

        # Setting the Maze test Button
        self.mainWindow.maze_btn.setGeometry(3*winDimension[0] / 6, 3*winDimension[1] / 6,
                                            winDimension[0] / 4, winDimension[1] / 4)

        # When the patient history button is clicked, it will go to the getPatientHistory() function
        self.mainWindow.historyButton.clicked.connect(self.getPatientHistory)

        # When the item in  the tree is clicked, it will go to the setting up test page
        self.mainWindow.treeWidget_2.itemClicked.connect(
            self.testPage)
        # self.mainWindow.vip_btn.clicked.connect(self.)

        # Logoff Window
        self.mainWindow.btn_logout.clicked.connect(self.toLogOut)

        # Opening the VIP tests for clinicians
        self.mainWindow.vip_btn.clicked.connect(self.vipTest)

        # Opening the Saccade tests for clinicians
        self.mainWindow.sas_btn.clicked.connect(self.sasTest)

        # Opening the Trail Blazer tests for clinicians
        self.mainWindow.tb_btn.clicked.connect(self.tbTest)

        # Opening the Maze tests for clinicians
        self.mainWindow.maze_btn.clicked.connect(self.mazeTest)

        # Register Patient
        self.mainWindow.registerBtn.clicked.connect(self.registerUser)

        # Predefined messages
        self.register_success = "Registered successfully"
        self.register_failure = "Failed registration"
        self.password_failure= "Passwords do not match"
        self.mainWindow.submitButton.clicked.connect(self.checked)

    """
    Function that unchecks all the boxs in the set up test page
    """
    def uncheckBoxes(self):
        self.mainWindow.vipBox.setChecked(False)
        self.mainWindow.sasBox.setChecked(False)
        self.mainWindow.tbBox.setChecked(False)
        self.mainWindow.mazeBox.setChecked(False)
        self.mainWindow.facialBox.setChecked(False)
        self.mainWindow.eyetrackingBox.setChecked(False)

    """
    Function that calls the uncheckBoxes() function and sets the window to the set up test window
    """
    def patientPageSetup(self):
        self.uncheckBoxes()
        self.mainWindow.Pages_Widget.setCurrentWidget(self.mainWindow.page_2)

    #add another page to add another org to a patient?

    """
    Function that opens all of the result pdfs
    """
    def getPatientHistory(self):
        # Opening the saccade csv result file
        if os.path.exists(self.mainWindow.treeWidget_2.currentItem().text(2) + '_sas.csv'):
            df = pd.read_csv(self.mainWindow.treeWidget_2.currentItem().text(2) + '_sas.csv')
            df.columns = df.columns.str.strip()
            # print("<{}>".format(df.columns[1]))
            html = df.to_html()
            displayResultsTxt = open(self.mainWindow.treeWidget_2.currentItem().text(2) + '_sas.html', "w")
            displayResultsTxt.write(html)
            displayResultsTxt.close()
            filename = 'file:///' + os.getcwd() + '/' + self.mainWindow.treeWidget_2.currentItem().text(2) + '_sas.html'
            webbrowser.open_new_tab(filename)
            results = []
            x = []
            y = []

            with open(self.mainWindow.treeWidget_2.currentItem().text(2) + '_sas.csv', 'r', newline='') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)
                for row in reader:  # each row is a list
                    results.append(row)
            for idx1 in range(len(results)):
                for idx2 in range(len(results[idx1])):
                    if idx2 == 0:
                        x.append(results[idx1][idx2])
                    elif idx2 == 18:
                        y.append(float(results[idx1][idx2]))
                    else:
                        pass

            # Creating the Average Saccade Time Per Round graph
            x = pd.to_datetime(x)
            df = pd.DataFrame()
            df['value'] = y
            df = df.set_index(x)
            plt.plot(df)
            plt.gcf().autofmt_xdate()
            plt.title("Average Saccade Time Per Round")
            plt.savefig("sas1.pdf", format="pdf", bbox_inches="tight")
            # plt.show()

            # Creating the Overall Saccade Result pdf which includes the graph
            pdfs = [self.mainWindow.treeWidget_2.currentItem().text(2) + '-sas.pdf', 'sas1.pdf']
            merger = PdfMerger()
            for pdf in pdfs:
                merger.append(pdf)
            merger.write(self.mainWindow.treeWidget_2.currentItem().text(2) + 'sas.pdf')
            merger.close()
            if (os.path.exists('sas1.pdf')):
                os.remove('sas1.pdf')
            webbrowser.open_new(self.mainWindow.treeWidget_2.currentItem().text(2) + 'sas.pdf')

        # Opening the VIP csv result file
        if os.path.exists(self.mainWindow.treeWidget_2.currentItem().text(2) + '_vip.csv'):
            df = pd.read_csv(self.mainWindow.treeWidget_2.currentItem().text(2) + '_vip.csv')
            df.columns = df.columns.str.strip()
            # print("<{}>".format(df.columns[1]))
            html = df.to_html()
            displayResultsTxt = open(self.mainWindow.treeWidget_2.currentItem().text(2) + '_vip.html', "w")
            displayResultsTxt.write(html)
            displayResultsTxt.close()
            filename = 'file:///' + os.getcwd() + '/' + self.mainWindow.treeWidget_2.currentItem().text(2) + '_vip.html'
            webbrowser.open_new_tab(filename)
            results = []
            x = []
            bulbar = []
            upperBody = []
            lowerBody = []
            with open(self.mainWindow.treeWidget_2.currentItem().text(2) + '_vip.csv', 'r', newline='') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)
                for row in reader:  # each row is a list
                    results.append(row)
            for idx1 in range(len(results)):
                for idx2 in range(len(results[idx1])):
                    if idx2 == 0:
                        x.append(results[idx1][idx2])
                    elif idx2 == 2:
                        bulbar.append(float(results[idx1][idx2]))
                    elif idx2 == 3:
                        upperBody.append(float(results[idx1][idx2]))
                    elif idx2 == 4:
                        lowerBody.append(float(results[idx1][idx2]))
                    else:
                        pass

            # Creating the VIP Bulbar Scores graph
            x = pd.to_datetime(x)
            # print(x)
            # df = pd.DataFrame({'Bulbar': bulbar, 'Upper Body': upperBody, 'Lower Body': lowerBody})
            # df['value'] = y
            df = pd.DataFrame()
            df['value'] = bulbar
            df = df.set_index(x)
            plt.figure(1)
            plt.plot(df)
            plt.gcf().autofmt_xdate()
            plt.title("VIP Bulbar Scores")
            plt.savefig("vip1.pdf", format="pdf", bbox_inches="tight")
            # plt.show()

            # Creating the VIP Upper Body Scores graph
            plt.figure(2)
            df = pd.DataFrame()
            df['value'] = upperBody
            df = df.set_index(x)
            plt.plot(df)
            plt.gcf().autofmt_xdate()
            plt.title("VIP Upper Body Scores")
            plt.savefig("vip2.pdf", format="pdf", bbox_inches="tight")
            # plt.show()

            # Creating the VIP Lower Body Scores graph
            plt.figure(3)
            df = pd.DataFrame()
            df['value'] = lowerBody
            df = df.set_index(x)
            plt.plot(df)
            plt.gcf().autofmt_xdate()
            plt.title("VIP Lower Body Scores")
            plt.savefig("vip3.pdf", format="pdf", bbox_inches="tight")
            # plt.show()

            # Creating the Overall VIP Result pdf which includes the graphs
            pdfs = [self.mainWindow.treeWidget_2.currentItem().text(2) + '-vip.pdf', 'vip1.pdf', 'vip2.pdf', 'vip3.pdf']
            merger = PdfMerger()
            for pdf in pdfs:
                merger.append(pdf)
            merger.write(self.mainWindow.treeWidget_2.currentItem().text(2) + 'vip.pdf')
            merger.close()
            if (os.path.exists('vip1.pdf')):
                os.remove('vip1.pdf')
            if (os.path.exists('vip2.pdf')):
                os.remove('vip2.pdf')
            if (os.path.exists('vip3.pdf')):
                os.remove('vip3.pdf')
            webbrowser.open_new(self.mainWindow.treeWidget_2.currentItem().text(2) + 'vip.pdf')
        #if os.path.exists(self.mainWindow.treeWidget_2.currentItem().text(2)+ '.pdf'):
            #self.openVIPDoc(self.mainWindow.treeWidget_2.currentItem().text(2))

        # Opening the Trailblazer csv result file
        if os.path.exists(self.mainWindow.treeWidget_2.currentItem().text(2)+'_tb.csv'):
            df = pd.read_csv(self.mainWindow.treeWidget_2.currentItem().text(2) + '_tb.csv')
            df.columns = df.columns.str.strip()
            # print("<{}>".format(df.columns[1]))
            html = df.to_html()
            displayResultsTxt = open(self.mainWindow.treeWidget_2.currentItem().text(2) + '_tb.html', "w")
            displayResultsTxt.write(html)
            displayResultsTxt.close()
            filename = 'file:///' + os.getcwd() + '/' + self.mainWindow.treeWidget_2.currentItem().text(2) + '_tb.html'
            webbrowser.open_new_tab(filename)
            results = []
            x = []
            time = []
            incorrect = []
            with open(self.mainWindow.treeWidget_2.currentItem().text(2) + '_tb.csv', 'r', newline='') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)
                for row in reader:  # each row is a list
                    results.append(row)
            for idx1 in range(len(results)):
                for idx2 in range(len(results[idx1])):
                    if idx2 == 0:
                        x.append(results[idx1][idx2])
                    elif idx2 == 2:
                        time.append(float(results[idx1][idx2]))
                    elif idx2 == 3:
                        incorrect.append(float(results[idx1][idx2]))
                    else:
                        pass

            # Creating the TB Average Trail Blazer Time graph
            x = pd.to_datetime(x)
            plt.figure(4)
            df = pd.DataFrame()
            df['value'] = time
            df = df.set_index(x)
            plt.plot(df)
            plt.gcf().autofmt_xdate()
            plt.title('Average Trail Blazer Time')
            plt.savefig("tb1.pdf", format="pdf", bbox_inches="tight")
            # plt.show()

            # Creating the TB Incorrect Guesses graph
            plt.figure(5)
            df = pd.DataFrame()
            df['value'] = incorrect
            df = df.set_index(x)
            plt.plot(df)
            plt.gcf().autofmt_xdate()
            plt.title("Incorrect Guesses")
            plt.savefig("tb2.pdf", format="pdf", bbox_inches="tight")
            # plt.show()

            # Creating the Overall Trailblazer Result pdf which includes the graphs
            pdfs = [self.mainWindow.treeWidget_2.currentItem().text(2) + '-tb.pdf', 'tb1.pdf', 'tb2.pdf']
            merger = PdfMerger()
            for pdf in pdfs:
                merger.append(pdf)
            merger.write(self.mainWindow.treeWidget_2.currentItem().text(2) + 'tb.pdf')
            merger.close()
            if (os.path.exists('tb1.pdf')):
                os.remove('tb1.pdf')
            if (os.path.exists('tb2.pdf')):
                os.remove('tb2.pdf')
            webbrowser.open_new(self.mainWindow.treeWidget_2.currentItem().text(2) + 'tb.pdf')

    "Function to open any pdf given the username"
    def openVIPDoc(self,username):
        path=username+".pdf"
        webbrowser.open_new(path)

    "Function to open a documention pdf"
    def openHelpDoc(self):
        path = "ClinicianHelpDocument.pdf"
        webbrowser.open_new(path)

    "Function to set up the test page"
    def testPage(self):
        # Setting the current window to the test page for the patient
        self.mainWindow.Pages_Widget.setCurrentWidget(self.mainWindow.page)

        #Changing the test order message
        self.mainWindow.testOrderMessage.move(winDimension[0] - 550, winDimension[1] / 2)
        self.mainWindow.testOrderMessage.setHidden(True)

        self.mainWindow.clinicianNameInput.setText(data_handler.patientLists[window.getUser()]["first_name"]+" "+data_handler.patientLists[window.getUser()]["last_name"])

        #Gets information from the clinician input box
        clinicianName=self.mainWindow.clinicianNameInput.text()

        # Gets information from the department input box
        departmentName=self.mainWindow.departmentInput.text()

        df = pd.read_csv("users.csv")
        #Gets the name of the clinician and the department
        df.loc[df['username']== data_handler.patientLists[self.mainWindow.treeWidget_2.currentItem().text(2)][
            "username"] , 'clinician name'] = clinicianName
        df.loc[df['username'] == data_handler.patientLists[self.mainWindow.treeWidget_2.currentItem().text(2)][
            "username"], 'department'] = departmentName
        df.to_csv('users.csv',index=False)

        #Sets the name of the patient
        self.mainWindow.patientInfoButton.setText(
            data_handler.patientLists[self.mainWindow.treeWidget_2.currentItem().text(2)]["first_name"] + " " +
            (data_handler.patientLists[self.mainWindow.treeWidget_2.currentItem().text(2)])[
                'last_name'])  # need to change the name of the label since its not a button

        self.mainWindow.patientInfoButton.setFont(QFont('Helvetica', 32))
        self.mainWindow.patientInfoButton.move(winDimension[0] / 3, 2 * windowHeightOffset)

        # Changing the Name label in the Test Page
        self.mainWindow.nameLabel.setFont(QFont('Helvetica', 16))
        self.mainWindow.nameLabel.move(winDimension[0] / 3 + 90, 0)

        # Changing the Department label in the Test Page
        self.mainWindow.departmentLabel.setFont(QFont('Helvetica', 16))
        self.mainWindow.departmentLabel.move(winDimension[0] / 3, 50)

        # Changing the Name input box in the Test Page
        self.mainWindow.clinicianNameInput.move(winDimension[0] / 3 + 180, 25)

        # Changing the Department input box in the Test Page
        self.mainWindow.departmentInput.move(winDimension[0] / 3 + 180, 80)

        # Changing the Test Order label in the Test Page
        self.mainWindow.testOrderLabel.setFont(QFont('Helvetica', 16))
        self.mainWindow.testOrderLabel.move(winDimension[0] / 3 - 200,
                                            0)  # fix it to line up with the clinician name label

        # Changing the EyeTracking check box in the Test Page
        self.mainWindow.eyetrackingBox.setFont(QFont('Helvetica', 16))
        self.mainWindow.eyetrackingBox.move(winDimension[0] / 3 + 400, 50)

        # Changing the VIP check box in the Test Page
        self.mainWindow.vipBox.setFont(QFont('Helvetica', 16))
        self.mainWindow.vipBox.move(winDimension[0] / 3 - 200, winDimension[1] / 4)

        # Changing the Saccade check box in the Test Page
        self.mainWindow.sasBox.setFont(QFont('Helvetica', 16))
        self.mainWindow.sasBox.move(winDimension[0] / 3 - 200, winDimension[1] / 4 + 2 * windowHeightOffset)

        # Changing the Trailblazer check box in the Test Page
        self.mainWindow.tbBox.setFont(QFont('Helvetica', 16))
        self.mainWindow.tbBox.move(winDimension[0] / 3 - 200, winDimension[1] / 4 + 4 * windowHeightOffset)

        # Changing the Maze check box in the Test Page
        self.mainWindow.mazeBox.setFont(QFont('Helvetica', 16))
        self.mainWindow.mazeBox.move(winDimension[0] / 3 - 200, winDimension[1] / 4 + 6 * windowHeightOffset)

        # Changing the Facial Test check box in the Test Page
        self.mainWindow.facialBox.setFont(QFont('Helvetica', 16))
        self.mainWindow.facialBox.move(winDimension[0] / 3, winDimension[1] / 4)

        # Changing the Submit button in the Test Page
        self.mainWindow.submitButton.setFont(QFont('Helvetica', 16))
        self.mainWindow.submitButton.move(winDimension[0] - 350, winDimension[1] - 4 * windowHeightOffset)
        self.mainWindow.submitButton.resize(275, 50)

        # Changing the History button in the Test Page
        self.mainWindow.historyButton.setFont(QFont('Helvetica', 16))
        self.mainWindow.historyButton.move(windowHeightOffset / 6, winDimension[1] - 4 * windowHeightOffset)
        self.mainWindow.historyButton.resize(275, 50)

    "Function to update the csv file"
    def updateTests(self, username, test):

        # Trying with Pandas
        # import pandas as pd (on top)
        df = pd.read_csv("users.csv")

        if test == 'vip':
            df.loc[df['username'] ==window.getUser(),'vip']='False'
        if test == 'sas':
            df.loc[df['username'] == window.getUser(), 'sas'] = 'False'
        if test== 'tb':
            df.loc[df['username'] == window.getUser(), 'tb'] = 'False'
            #print(value)
            # df.replace(data_handler.patientsList[username]
        # elif test='sas':

        data_handler.windows_password_protect("./users.csv")
        #data_handler.windows_password_protect("./data.csv")

        """
        fd=open("users.csv",'r')
        reader=csv.DictReader(fd)
        tempList=[]
        for row in reader:
            newrow={'first_name': row["first_name"],'last_name': row["last_name"],
                                                    'date_of_birth': row["date_of_birth"], 'organization': row["organization"],
                                                    'username': row["username"],'password': row["password"],
                                                    'role': row["role"], 'vip': row['vip'],'sas': row['sas'],
                                                    'tb': row['tb'],'maze': row['maze']}
            tempList.append(newrow)
        fd.close()
        writer=open("users.csv","w",newline='')
        headers=['first_name', 'last_name', 'date_of_birth', 'organization', 'username', 'password', 'role','vip','sas','tb','maze']
        data=csv.DictWriter(writer, delimiter=",",fieldnames= headers)
        #data.writerow(dict((heads, heads) for heads in headers))
        data.writerows(tempList)
        writer.close()
        """""

        """
        with open('users.csv', "a+", newline='') as file_credentials:
            writer = csv.DictWriter(file_credentials,
                                    fieldnames=['first_name', 'last_name', 'date_of_birth', 'organization',
                                                'username', 'password', 'role', 'vip', 'sas', 'tb', 'maze'])
            writer.writerow({'first_name': data_handler[username]["first_name"],'last_name': data_handler[username]["last_name"],
                                     'date_of_birth': data_handler[username]["date_of_birth"],'organization': data_handler[username]["organization"],
                                     'username': data_handler[username]["username"],'password': data_handler[username]['password'],'role': data_handler[username]['role'],
                                     'vip':vip,'sas':sas,'tb':tb,'maze':maze})
            print(sas)
        """""

    "Function to check what boxes are checked and enable the test depending on which box was checked"
    def checked(self):
        # Checks if the VIP box was checked
        if self.mainWindow.vipBox.isChecked():
            if data_handler.patientLists[self.mainWindow.treeWidget_2.currentItem().text(2)]['vip'] == 'False':
                data_handler.patientLists[self.mainWindow.treeWidget_2.currentItem().text(2)]['vip'] = 'True'
                # Updates in the csv
                data_handler.updatePatientTestStatus('vip','True',data_handler.patientLists[self.mainWindow.treeWidget_2.currentItem().text(2)]['username'])
        # Checks if the SAS box was checked
        if self.mainWindow.sasBox.isChecked():
            if data_handler.patientLists[self.mainWindow.treeWidget_2.currentItem().text(2)]["sas"] == 'False':
                data_handler.patientLists[self.mainWindow.treeWidget_2.currentItem().text(2)]["sas"] = 'True'
                data_handler.updatePatientTestStatus('sas', 'True', data_handler.patientLists[
                    self.mainWindow.treeWidget_2.currentItem().text(2)]['username'])
            #self.uncheckBoxes()
            print(data_handler.patientLists[self.mainWindow.treeWidget_2.currentItem().text(2)]["sas"])
        # Checks if the TB box was checked
        if self.mainWindow.tbBox.isChecked():
            if data_handler.patientLists[self.mainWindow.treeWidget_2.currentItem().text(2)]["tb"] == 'False':
                data_handler.patientLists[self.mainWindow.treeWidget_2.currentItem().text(2)]["tb"] = 'True'
                data_handler.updatePatientTestStatus('tb', 'True', data_handler.patientLists[
                    self.mainWindow.treeWidget_2.currentItem().text(2)]['username'])
        # Checks if the EyeTracking box was checked
        if self.mainWindow.eyetrackingBox.isChecked():
            data_handler.updatePatientTestStatus('eyetracking','True', data_handler.patientLists[
                    self.mainWindow.treeWidget_2.currentItem().text(2)]['username'])

        # Checks to see if clinician clicked a test button to notify them whether they were sucessful
        if self.mainWindow.vipBox.isChecked() or self.mainWindow.sasBox.isChecked() or self.mainWindow.tbBox.isChecked():
            self.mainWindow.testOrderMessage.setText(self.orderTestSuccess)
            self.mainWindow.testOrderMessage.setStyleSheet("color: green")
            self.mainWindow.testOrderMessage.setHidden(False)
        else:
            self.mainWindow.testOrderMessage.setText(self.orderTestFail)
            self.mainWindow.testOrderMessage.setStyleSheet("color: red")
            self.mainWindow.testOrderMessage.setHidden(False)
        self.uncheckBoxes()
            # data_handler.patientLists[self.mainWindow.treeWidget.currentItem().text(2)]["sas"] = ~(data_handler.patientLists[self.mainWindow.treeWidget.currentItem().text(2)]["sas"])

    "Function to open the VIP test in the test practice page"
    def vipTest(self):
        # instructions()
        vip=VIP.VipTest("clinician")
        vip.VIP()

    def updateTB(self):
        data_handler.patientLists["username"]["tb"][2] = 1

    def updateMaze(self):
        data_handler.patientLists["username"]["maze"][3] = 1

    "Function to open the Saccade test in the test practice page"
    def sasTest(self):
        saccade = GameMain.SaccadeTest("clinician")

        saccade.Saccade()

    "Function to open the Trailblazer test in the test practice page"
    def tbTest(self):
        print('Trailblazer Test')
        tb = TrailBlazer.TrailBlazerTest()
        tb.TrailBlazer(7)

    def mazeTest(self):
        print('Maze Test')

    # updating the patient list in the GUI
    # def updatePatientsList(self):

    # patientsList.

    "Function to populate the patients in the tree widget in the patients page"
    def populatePatients(self):
        for patient in data_handler.patientLists.values():
            if patient["organization"] == data_handler.get_attribute(window.getUser(), "organization") and \
                    patient["role"] == "patient":
                QTreeWidgetItem(self.mainWindow.treeWidget_2,
                                [patient["first_name"], patient["last_name"], patient["username"], patient["date_of_birth"],
                                 patient["organization"],
                                 patient["role"]])

    "Function to logout"
    def toLogOut(self):
        self.mainWindow.hide()
        window.loginWindow.show()
        # self.center()
        # self.resize(480,620)

    "Function to clear all the text in the register patient page"
    def clearFields(self):
        self.mainWindow.register_firstName.clear()
        self.mainWindow.register_lastName.clear()
        self.mainWindow.register_userId.clear()
        self.mainWindow.register_password.clear()
        self.mainWindow.register_confirmPassword.clear()
        self.mainWindow.register_organization.clear()
        self.mainWindow.register_role.clear()
        self.mainWindow.register_bday.clear()

    "Function to register a patient in the register patient page"
    def registerUser(self):
        # Set the text inputted in the register patient page
        first_name = self.mainWindow.register_firstName.text()
        last_name = self.mainWindow.register_lastName.text()
        username = self.mainWindow.register_userId.text()
        password = self.mainWindow.register_password.text()
        confirm_password = self.mainWindow.register_confirmPassword.text()
        organization = self.mainWindow.register_organization.text()
        role = self.mainWindow.register_role.text()
        bday = self.mainWindow.register_bday.text()
        data = [{'first_name': first_name, 'last_name': last_name, 'date_of_birth': bday,
                 'organization': organization, 'username': username, 'password': password, 'role': role}]

        #Checks if the password input is the same as the confirm password input
        if(password!=confirm_password):
            self.mainWindow.register_message.setText(self.password_failure)
            self.mainWindow.register_message.setStyleSheet("color: green;")
            self.mainWindow.register_message.setHidden(False)
            success=False
        else:
            success = data_handler.add_credentials(data)

        #Inputs a message if the user was successfully registered
        if success:
            self.mainWindow.register_message.setText(self.register_success)
            self.mainWindow.register_message.setStyleSheet("color: green;")
            self.mainWindow.register_message.setHidden(False)
            data_handler.updatePatientDict()
            QTreeWidgetItem(self.mainWindow.treeWidget_2, [first_name, last_name, username, bday,
                            organization,role])
            self.clearFields()
            # self.populatePatients()
        else:
            self.mainWindow.register_message.setText(self.register_failure)
            self.mainWindow.register_message.setStyleSheet("color: green;")
            self.mainWindow.register_message.setHidden(False)

        #self.populatePatients()

"""
Class Definition for whole GUI window for the patient portal and its elements
"""
class MainWindowPatient(QMainWindow):
    def __init__(self):
        super(MainWindowPatient, self).__init__()
        file = QtCore.QFile("UI Files/ui_main_patient.ui")
        if not file.open(QtCore.QFile.ReadOnly):
            print(f"Cannot open {file}: {file.errorString()}")
            sys.exit(-1)
        self.mainWindow = loader.load(file)
        file.close()
        if not self.mainWindow:
            print(loader.errorString())
            sys.exit(-1)
        self.mainWindow.resize(winDimension[0], winDimension[1]-windowHeightOffset)
        self.mainWindow.show()

        # Changing Home Screen Image Elements in the Home Page
        self.mainWindow.main_label.setPixmap(QtGui.QPixmap(gv.path_to_images + 'esmetrics.jpg'))
        self.mainWindow.main_label.setScaledContents(True)
        self.mainWindow.main_label.move(winDimension[0] / 4, winDimension[1] / 4)

        # Changing the Copyright label line 1 in the Home Page
        self.mainWindow.copyrightLabel1.setFont(QFont('Helvetica', 10))
        self.mainWindow.copyrightLabel1.move(winDimension[0] / 3 - 2 * windowHeightOffset,
                                             0.5 * winDimension[1] + 0.04 * winDimension[1])

        # Changing the Copyright label line 2 in the Home Page
        self.mainWindow.copyrightLabel2.setFont(QFont('Helvetica', 10))
        self.mainWindow.copyrightLabel2.move(winDimension[0] / 3 - 2 * windowHeightOffset,
                                             0.5 * winDimension[1] + 0.08 * winDimension[1])

        # Changing the Copyright label line 3 in the Home Page
        self.mainWindow.copyrightLabel3.setFont(QFont('Helvetica', 10))
        self.mainWindow.copyrightLabel3.move(winDimension[0] / 3 - 2 * windowHeightOffset,
                                             0.5 * winDimension[1] + 0.12 * winDimension[1])

        # Changing the Copyright label line 4 in the Home Page
        self.mainWindow.copyrightLabel4.setFont(QFont('Helvetica', 10))
        self.mainWindow.copyrightLabel4.move(winDimension[0] / 3 - 2 * windowHeightOffset,
                                             0.5 * winDimension[1] + 0.16 * winDimension[1])

        # Changing the Copyright label line 5 in the Home Page
        self.mainWindow.copyrightLabel5.setFont(QFont('Helvetica', 10))
        self.mainWindow.copyrightLabel5.move(winDimension[0] / 3 - 2 * windowHeightOffset,
                                             0.5 * winDimension[1] + 0.2 * winDimension[1])

        # Changing the Copyright label line 6 in the Home Page
        self.mainWindow.copyrightLabel6.setFont(QFont('Helvetica', 10))
        self.mainWindow.copyrightLabel6.move(winDimension[0] / 3 - 2 * windowHeightOffset,
                                             0.5 * winDimension[1] + 0.24 * winDimension[1])

        # Changing the Copyright label line 7 in the Home Page
        self.mainWindow.copyrightLabel7.setFont(QFont('Helvetica', 10))
        self.mainWindow.copyrightLabel7.move(winDimension[0] / 3 - 2 * windowHeightOffset,
                                             0.5 * winDimension[1] + 0.28 * winDimension[1])

        #List of tests enabled for the user
        self.tests = [data_handler.patientLists[window.getUser()]['vip'],
                      data_handler.patientLists[window.getUser()]['sas'],
                      data_handler.patientLists[window.getUser()]['tb'],
                      data_handler.patientLists[window.getUser()]['maze']]
        # data_handler.updatePatientDict()

        #Gets the current users name
        self.user = window.getUser()
        print(self.user)
        self.isItRunning = False
        self.testsEnabled=False
        # data_handler.updatePatientDict()
        ## TOGGLE/BURGUER MENU
        self.mainWindow.btn_toggle.clicked.connect(lambda: UIFunctions.toggleMenu(self, 250, True))

        ## PAGES

        # Home Page
        self.mainWindow.btn_home.clicked.connect(
            lambda: self.mainWindow.Pages_Widget.setCurrentWidget(self.mainWindow.MainPage))

        # Settings Page
        #self.mainWindow.btn_settings.clicked.connect(
            #lambda: self.mainWindow.Pages_Widget.setCurrentWidget(self.mainWindow.SettingsPage))

        # Help Page
        # self.mainWindow.btn_help.clicked.connect(
        # lambda: self.mainWindow.Pages_Widget.setCurrentWidget(self.mainWindow.HelpPage))

        self.mainWindow.btn_help.clicked.connect(self.openHelpDoc)

        # Tests Page
        self.mainWindow.btn_tests.clicked.connect(
            self.checkTests)

        # Logoff Window
        self.mainWindow.btn_logout.clicked.connect(self.toLogOut)

        # Register Patient
        self.mainWindow.registerBtn.clicked.connect(self.registerUser)

        # Saccade Test Button
        self.mainWindow.sasTestButton.clicked.connect(self.sasRunning)

        # VIP Test Button
        self.mainWindow.vipTestButton.clicked.connect(self.vipRunning)

        # Trailblazer Test Button
        self.mainWindow.tbTestButton.clicked.connect(self.tbRunning)

        # Predefined messages
        self.register_success = "Registered successfully"
        self.register_failure = "Failed registration"

    "Function that runs Saccade and outputs out a result pdf"
    def sasRunning(self):  # have one function that takes in type of test. when updating self.test have a check case for type of test and index properly
        # data_handler.updatePatientTestStatus('sas','True',self.user)
        eye_tracking = False
        if ('patient' == data_handler.get_attribute(self.user, 'role')):
            if ('True' == data_handler.get_attribute(self.user, 'eyetracking')):
                eye_tracking = True

        saccade = GameMain.SaccadeTest(self.user, eye_tracking)
        py = saccade.Saccade()

        while py != 1:
            pass

        data_handler.updatePatientTestStatus('sas', 'False', window.getUser())
        #self.mainWindow.Pages_Widget.setCurrentWidget(self.mainWindow.MainPage)
        if self.tests[0] == "False" and self.tests[1] == "False" and self.tests[2] == "False" and self.tests[
            3] == "False":
            self.isItRunning = False
        self.tests[1] = "False"

        with open(self.user + '_vip_mouse.csv', 'a') as patientCsv1:
            patientCsv1.seek(0)
            writer = csv.DictWriter(patientCsv1,
                                    fieldnames=['Time', 'Mouse Coordinate'],
                                    lineterminator='\n')
            writer.writerow({'Time': datetime.now().strftime("%d_%m_%Y_%H_%M_%S")})
            for i in vip.getMouseLocation():
                writer.writerow({'Mouse Coordinate': i})

        with open(self.user + '_sas.csv', 'a') as patientCsv:
            patientCsv.seek(0)
            writer = csv.DictWriter(patientCsv,
                                    fieldnames=['Date', 'Test', 'Round 1', 'Round 2', 'Round 3', 'Round 4',
                                                'Round 5', 'Round 6', 'Round 7', 'Round 8', 'Round 9',
                                                'Round 10', 'Round 11', 'Round 12', 'Round 13', 'Round 14',
                                                'Round 15', 'Round 16','Average Time'], lineterminator='\n')
            if os.stat(self.user + '_sas.csv').st_size == 0:  # checks if file is empty
                writer.writeheader()

            today = date.today()
            averageTime = (saccade.results[0] + saccade.results[1] + saccade.results[2] + saccade.results[3] +
                           saccade.results[4] + saccade.results[5] + saccade.results[6] + saccade.results[7] +
                           saccade.results[8] + saccade.results[9] + saccade.results[10] + saccade.results[11] +
                           saccade.results[12] + saccade.results[13] + saccade.results[14] + saccade.results[15]) / 16
            writer.writerow(
                {'Date': today.strftime('%m/%d/%Y %H:%M:%S'), 'Test': 'Sas', 'Round 1': saccade.results[0],
                 'Round 2': saccade.results[1],  # date works time doesn't
                 'Round 3': saccade.results[2], 'Round 4': saccade.results[3],
                 'Round 5': saccade.results[4], 'Round 6': saccade.results[5], 'Round 7': saccade.results[6],
                 'Round 8': saccade.results[7], 'Round 9': saccade.results[8],
                 'Round 10': saccade.results[9], 'Round 11': saccade.results[10], 'Round 12': saccade.results[11],
                 'Round 13': saccade.results[12], 'Round 14': saccade.results[13],
                 'Round 15': saccade.results[14], 'Round 16': saccade.results[15], 'Average Time':averageTime})
            # file_credentials.flush()
            # return 1
        #Change this to change the text and the format of the pdf
        textLines = [
            "            Saccade (SAS) Tests Results",
            "                                                                               ",
            "Patient",
            "                                                                               ",
            data_handler.patientLists[window.getUser()]['first_name'] + " " + data_handler.patientLists[window.getUser()]['last_name'],
            "                                                                               ",
            "Test Date: " + str(today),
            "Test Ordered By: " + data_handler.patientLists[window.getUser()]['clinician name'] + " Clinician"
            "                                                                               ",
            "                                                                               ",
            "Average Time Per Round:                  " + str(averageTime) + "            Healthy Range: [XX-YY]",
            "                                                                           ",
        ]
        pdf = canvas.Canvas(window.getUser() + "-sas.pdf")

#        text = pdf.beginText(40, 680)
#        pdf.setFont("Helvetica", 16)
#        for line in textLines:
#            text.textLine(line)

#        pdf.drawText(text)

#        pdf.save()
#        self.checkTests()

    "Function that runs VIP and outputs out a result pdf"
    def vipRunning(self):
        # data_handler.updatePatientTestStatus('vip', 'True', self.user)
        eye_tracking = False
        if ('patient' == data_handler.get_attribute(self.user, 'role')):
            if ('True' == data_handler.get_attribute(self.user, 'eyetracking')):
                eye_tracking = True

        print(data_handler.patientLists)
        vip = VIP.VipTest(self.user, eye_tracking=eye_tracking)
        vip.VIP()
        vip.setRunning('True')

        while vip.getRunning == 'True':
            pass

        data_handler.updatePatientTestStatus('vip', 'False', window.getUser())
        # self.mainWindow.Pages_Widget.setCurrentWidget(self.mainWindow.MainPage)
        if self.tests[0] == "False" and self.tests[1] == "False" and self.tests[2] == "False" and self.tests[
            3] == "False":
            self.isItRunning = False
        self.tests[0] = "False"

        with open(self.user + '_vip_mouse.csv', 'a') as patientCsv1:
            patientCsv1.seek(0)
            writer = csv.DictWriter(patientCsv1,
                                    fieldnames=['Time', 'Mouse Coordinate'],
                                    lineterminator='\n')
            writer.writerow({'Time': datetime.now().strftime("%d_%m_%Y_%H_%M_%S")})
            for i in vip.getMouseLocation():
                writer.writerow({'Mouse Coordinate': i})

        with open(self.user + '_vip.csv', 'a') as patientCsv:
            patientCsv.seek(0)
            writer = csv.DictWriter(patientCsv,
                                    fieldnames=['Date','Test','Bulbar', 'Upper_Body', 'Lower_Body',], lineterminator='\n')
            if os.stat(self.user + '_vip.csv').st_size == 0:  # checks if file is empty
                writer.writeheader()

            today = date.today()
            writer.writerow(
                {'Date': today.strftime('%m/%d/%Y %H:%M:%S'), 'Test': 'Vip', 'Bulbar': vip.getBulbar(),
                 'Upper_Body': vip.getUpperBody(),  # date works time doesn't
                 'Lower_Body': vip.getLowerBody()})

            # Change this to change the text and the format of the pdf
            textLines = [
                "            Verb-Image Pair (VIP) Tests Results",
                "                                                                               ",
                "Patient",
                "                                                                               ",
                data_handler.patientLists[window.getUser()]['first_name'] + " " + data_handler.patientLists[window.getUser()]['last_name'],
                "                                                                               ",
                "Test Date: " + str(today),
                "Test Ordered By: " + data_handler.patientLists[window.getUser()]['clinician name'] + " Clinician",
                "                                                                               ",
                "                                                                               ",
                "Bulbar Score:                  " + str(vip.getBulbar()) + "            Healthy Range: [XX-YY]",
                "                                                                           ",
                "Upper Limb Score:                  " + str(vip.getUpperBody()) + "            Healthy Range: [XX-YY]",
                "                                                                           ",
                "Bulbar Score:                  " + str(vip.getLowerBody()) + "            Healthy Range: [XX-YY]",
            ]
            pdf = canvas.Canvas(window.getUser() + "-vip.pdf")

#            text = pdf.beginText(40, 680)
#            pdf.setFont("Helvetica", 16)
#            for line in textLines:
#                text.textLine(line)

#            pdf.drawText(text)

#            pdf.save()
#        vip.setRunning('False')
#        self.checkTests()

    "Function that runs Trailblazer and outputs out a result pdf"
    def tbRunning(self):
        eye_tracking = False
        if ('patient' == data_handler.get_attribute(self.user, 'role')):
            if ('True' == data_handler.get_attribute(self.user, 'eyetracking')):
                eye_tracking = True

        tb=TrailBlazer.TrailBlazerTest(eye_tracking)
        test=tb.TrailBlazer(7)
        while test != 1:
            pass
        data_handler.updatePatientTestStatus('tb', 'False', window.getUser())
        if self.tests[0] == "False" and self.tests[1] == "False" and self.tests[2] == "False" and self.tests[
            3] == "False":
            self.isItRunning = False
        self.tests[2] = "False"

        with open(self.user + '_tb_mouse.csv', 'a') as patientCsv1:
            patientCsv1.seek(0)
            writer = csv.DictWriter(patientCsv1,
                                    fieldnames=['Time', 'Mouse Coordinate'],
                                    lineterminator='\n')
            writer.writerow({'Time': datetime.now().strftime("%d_%m_%Y_%H_%M_%S")})
            for i in tb.getMouseLocation():
                writer.writerow({'Mouse Coordinate': i})

        with open(self.user + '_tb.csv', 'a') as patientCsv:
            patientCsv.seek(0)
            writer = csv.DictWriter(patientCsv,
                                    fieldnames=['Date', 'Test', 'Total Time', 'Number of Incorrect Choices'], lineterminator='\n')
            if os.stat(self.user + '_tb.csv').st_size == 0:  # checks if file is empty
                writer.writeheader()

            today = date.today()
            writer.writerow(
                {'Date': today.strftime('%m/%d/%Y %H:%M:%S'), 'Test': 'Trailblazer', 'Total Time': tb.getTotalTime(),
                 'Number of Incorrect Choices': tb.getNumOfIncorrect(),  # date works time doesn't
                 })
        # Change this to change the text and the format of the pdf
        textLines = [
            "            TrailBlazer (TB) Tests Results",
            "                                                                               ",
            "Patient",
            "                                                                               ",
            data_handler.patientLists[window.getUser()]['first_name'] + " " +data_handler.patientLists[window.getUser()]['last_name'],
            "                                                                               ",
            "Test Date: " + str(today),
            "Test Ordered By: " + data_handler.patientLists[window.getUser()]['clinician name'] + " Clinician",
            "                                                                               ",
            "                                                                               ",
            "Total Time:                  " + str(tb.getTotalTime()) + "            Healthy Range: [XX-YY]",
            "                                                                           ",
            "Number of Incorrect Guesses:                  " + str(tb.getNumOfIncorrect()) + "         Healthy Range: [XX-YY]",
            "                                                                           ",
        ]
        pdf = canvas.Canvas(window.getUser() + "-tb.pdf")

#        text = pdf.beginText(40, 680)
#        pdf.setFont("Helvetica", 16)
#        for line in textLines:
#            text.textLine(line)

#        pdf.drawText(text)

#        pdf.save()
#        self.checkTests()


    "Checks which tests are enabled and if no tests are enabled it will go to the no tests enabled window"
    def checkTests(self):
        if self.tests[0] == "False" and self.tests[1] == "False" and self.tests[2] == "False" and self.tests[
            3] == "False":
            #Checks if tests were previously enabled so it can go to the complete test window
            if(self.testsEnabled==True):
                self.testsEnabled=False
                self.mainWindow.Pages_Widget.setCurrentWidget(self.mainWindow.CompleteTests)
                self.mainWindow.testsCompleteLabel1.setFont(QFont("Helvetica", 32))
                self.mainWindow.testsCompleteLabel1.move(6 * windowHeightOffset, winDimension[1] / 4)
                self.mainWindow.testsCompleteLabel2.setFont(QFont("Helvetica", 32))
                self.mainWindow.testsCompleteLabel2.move(6 * windowHeightOffset, 1.5*winDimension[1] / 4)
            #If the tests weren't previously enabled then it goes to the no tests enabled window
            else:
                self.mainWindow.Pages_Widget.setCurrentWidget(self.mainWindow.page_2)
                self.mainWindow.testNotEnabledLabel.setFont(QFont("Helvetica", 32))
                self.mainWindow.testNotEnabledLabel.move(6 * windowHeightOffset, winDimension[1] / 4)
        #If a tests were enabled then check which ones
        else:
            print(data_handler.patientLists[self.user])
            idx = 0
            print(self.tests)
            testValues = ['False', 'False', 'False', 'False']
            if self.tests[0] == 'True':
                self.isItRunning = True
                testValues[0] = 'vip'
            if self.tests[1] == 'True':
                self.isItRunning = True
                testValues[1] = 'sas'
            if self.tests[2] == 'True':
                self.isItRunning = True
                testValues[2] = 'tb'
            if self.tests[3] == 'True':
                self.isItRunning = True
                testValues[3] = 'maze'
            random.shuffle(testValues)
            #Performs all of the enabled tests
            while self.performTests(testValues) != 1 and self.isItRunning == False:
                pass
        # didnt change name after saving so leave it for now page_2 is the page that tells the user that no tests have been enabled.

    "Fucntion to check which enabled test to take first"
    def performTests(self, tests):
        print(tests)
        for testType in tests:
            # Checks if VIP was enabled
            if testType == 'vip':
                # self.isItRunning = True
                self.testsEnabled=True
                #Sets the window to VIP instructions
                self.mainWindow.Pages_Widget.setCurrentWidget(self.mainWindow.VipInstructions)

                # Changing the VIP label in the VIP instructions window
                self.mainWindow.performingVIPLabel.setFont(QFont('Helvetica', 32))
                self.mainWindow.performingVIPLabel.move(6 * windowHeightOffset, winDimension[1] / 4)

                # Changing the VIP instruction label1 in the VIP instructions window
                self.mainWindow.vipInstructionLabel1.setFont(QFont('Helvetica', 32))
                self.mainWindow.vipInstructionLabel1.move(6 * windowHeightOffset,
                                                          winDimension[1] / 4 + 2 * windowHeightOffset)
                # Changing the VIP instruction label2 in the VIP instructions window
                self.mainWindow.vipInstructionLabel2.setFont(QFont('Helvetica', 32))
                self.mainWindow.vipInstructionLabel2.move(6 * windowHeightOffset,
                                                          winDimension[1] / 4 + 3 * windowHeightOffset)

                # Changing the test button in the VIP instructions window
                self.mainWindow.vipTestButton.setFont(QFont('Helvetica', 16))
                self.mainWindow.vipTestButton.move(winDimension[0] - 350, winDimension[1] - 4 * windowHeightOffset)
                self.mainWindow.vipTestButton.resize(275, 50)
                break
            # Checks if Saccade was enabled
            elif testType == "sas":
                # self.isItRunning=True
                self.testsEnabled = True
                print(self.isItRunning)
                # Sets the window to Saccade instructions
                self.mainWindow.Pages_Widget.setCurrentWidget(self.mainWindow.SaccadeInstruction)

                # Changing the Saccade label in the Sas instructions window
                self.mainWindow.performingSASLabel.setFont(QFont('Helvetica',32))
                self.mainWindow.performingSASLabel.move(6 * windowHeightOffset, winDimension[1] / 4)

                # Changing the Saccade Instruction label line 1 in the Sas instructions window
                self.mainWindow.sasInstruction1.setFont(QFont('Helvetica', 32))
                self.mainWindow.sasInstruction1.move(6 * windowHeightOffset, winDimension[1] / 4+2*windowHeightOffset)

                # Changing the Saccade Instruction label line 2 in the Sas instructions window
                self.mainWindow.sasInstruction2.setFont(QFont('Helvetica', 32))
                self.mainWindow.sasInstruction2.move(6 * windowHeightOffset, winDimension[1] / 4+3*windowHeightOffset)

                # Changing the Saccade Instruction label line 3 in the Sas instructions window
                self.mainWindow.sasInstruction3.setFont(QFont('Helvetica', 32))
                self.mainWindow.sasInstruction3.move(6 * windowHeightOffset, winDimension[1] / 4+4*windowHeightOffset)

                # Changing the Saccade Instruction label line 4 in the Sas instructions window
                self.mainWindow.sasInstruction4.setFont(QFont('Helvetica', 32))
                self.mainWindow.sasInstruction4.move(6 * windowHeightOffset, winDimension[1] / 4+5*windowHeightOffset)

                # Changing the test button in the Sas instructions window
                self.mainWindow.sasTestButton.setFont(QFont('Helvetica', 16))
                self.mainWindow.sasTestButton.move(winDimension[0] - 350, winDimension[1] - 4 * windowHeightOffset)
                self.mainWindow.sasTestButton.resize(275, 50)
                break

            # Checks if Trailblazer was enabled
            if testType== 'tb':
                self.testsEnabled = True
                # Sets the window to Trailblazer instructions
                self.mainWindow.Pages_Widget.setCurrentWidget(self.mainWindow.TbInstructions)
                # Changing the Trailblazer label in the VIP instructions window
                self.mainWindow.performingTBLabel.setFont(QFont('Helvetica', 32))
                self.mainWindow.performingTBLabel.move(6 * windowHeightOffset, winDimension[1] / 4)

                # Changing the Trailblazer Instruction label line 1 in the Tb instructions window
                self.mainWindow.performingTBLabel_2.setFont(QFont('Helvetica', 32))
                self.mainWindow.performingTBLabel_2.move(6 * windowHeightOffset, winDimension[1] / 4+2*windowHeightOffset)

                # Changing the Trailblazer Instruction label line 2 in the Tb instructions window
                self.mainWindow.performingTBLabel_3.setFont(QFont('Helvetica', 32))
                self.mainWindow.performingTBLabel_3.move(6 * windowHeightOffset, winDimension[1] / 4+3*windowHeightOffset)

                #Changing the test button in the Tb instructions window
                self.mainWindow.tbTestButton.setFont(QFont('Helvetica', 16))
                self.mainWindow.tbTestButton.move(winDimension[0] - 350, winDimension[1] - 4 * windowHeightOffset)
                self.mainWindow.tbTestButton.resize(275, 50)
                break
            else:
                print("Coming Soon :) ")
                # break
        if self.tests[0] == "False" and self.tests[1] == "False" and self.tests[2] == "False" and self.tests[
            3] == "False":  #
            print(1)
            return 1

    "Function to open a documention pdf"
    def openHelpDoc(self):
        path = "PatientHelpDocument.pdf"
        webbrowser.open_new(path)

    "Function to logout"
    def toLogOut(self):
        self.mainWindow.hide()
        window.loginWindow.show()
        # self.center()
        # self.resize(480,620)

    "Function to register a patient in the register patient page"
    def registerUser(self):
        first_name = self.mainWindow.register_firstName.text()
        last_name = self.mainWindow.register_lastName.text()
        username = self.mainWindow.register_userId.text()
        password = self.mainWindow.register_password.text()
        confirm_password = self.mainWindow.register_confirmPassword.text()
        organization = self.mainWindow.register_organization.text()
        role = self.mainWindow.register_role.text()
        bday = self.mainWindow.register_bday.text()
        data = [{'first_name': first_name, 'last_name': last_name, 'date_of_birth': bday,
                 'organization': organization, 'username': username, 'password': password, 'role': role,
                 'vip': 'False', 'sas': 'False', 'tb': 'False', 'maze': 'False'}]

        success = data_handler.add_credentials(data)
        if success:
            self.mainWindow.register_message.setText(self.register_success)
            self.mainWindow.register_message.setStyleSheet("color: green;")
            self.mainWindow.register_message.setHidden(False)
        else:
            self.mainWindow.register_message.setText(self.register_failure)
            self.mainWindow.register_message.setStyleSheet("color: green;")
            self.mainWindow.register_message.setHidden(False)

"""
Class Definition for whole GUI window for the login and its elements
"""
class login(QDialog):
    def __init__(self):
        super(login, self).__init__()

        # Open QT Designer file
        file = QtCore.QFile("UI Files/login.ui")
        if not file.open(QtCore.QFile.ReadOnly):
            print(f"Cannot open {file}: {file.errorString()}")
            sys.exit(-1)
        self.loginWindow = loader.load(file)
        file.close()

        if not self.loginWindow:
            print(loader.errorString())
            sys.exit(-1)

        #adjusting all the elements in login.ui to match device resolution
        self.loginWindow.resize(winDimension[0],winDimension[1]-windowHeightOffset)
        self.loginWindow.loginLabel.setFont(QFont('Helvetica',32))
        self.loginWindow.loginLabel.move(0.45*winDimension[0], windowHeightOffset)
        self.loginWindow.usernameLabel.setFont(QFont('Helvetica',16))
        self.loginWindow.usernameLabel.move(0.4*winDimension[0],4*windowHeightOffset)
        self.loginWindow.username.resize(winDimension[0]/10,winDimension[1]/30)
        self.loginWindow.username.move(0.5*winDimension[0],4.4*windowHeightOffset)
        self.loginWindow.username.setFont(QFont('Helvetica',14))
        self.loginWindow.passwordLabel.setFont(QFont('Helvetica',16))
        self.loginWindow.passwordLabel.move(0.4*winDimension[0],5*windowHeightOffset)
        self.loginWindow.password.resize(winDimension[0]/10,winDimension[1]/30)
        self.loginWindow.password.move(0.5 * winDimension[0], 5.4 * windowHeightOffset)
        self.loginWindow.password.setFont(QFont("Helvetica",14))
        self.loginWindow.orgLabel.setFont(QFont('Helvetica', 16))
        self.loginWindow.orgLabel.move(0.4 * winDimension[0], 6 * windowHeightOffset)
        self.loginWindow.organization.resize(winDimension[0] / 10, winDimension[1] / 30)
        self.loginWindow.organization.move(0.5 * winDimension[0], 6.4 * windowHeightOffset)
        self.loginWindow.organization.setFont(QFont("Helvetica", 14))
        self.loginWindow.signinButton.setFont(QFont("Helvetica",16))
        self.loginWindow.signinButton.resize(0.06*winDimension[0],0.05*winDimension[1])
        self.loginWindow.signinButton.move(0.5 * winDimension[0],7.4 * windowHeightOffset)



        self.loginWindow.show()
        self.user = ''
        self.loginWindow.signinButton.clicked.connect(self.loginFunc)
        self.loginWindow.password.setEchoMode(QtWidgets.QLineEdit.Password)

        self.mainWindow = None

        self.username_doesnt_exist = "username doesn't exist."
        self.password_incorrect = "incorrect password"
        self.restricted_access = "user belongs to unknown role"
        self.login_successful = "login successful."
        self.logout = "logged out."
        # self.center()
        # self.resize(480,620)

    def loginFunc(self):
        username = self.loginWindow.username.text()
        password = self.loginWindow.password.text()
        organization = self.loginWindow.organization.text()
        self.loginWindow.login_message.setHidden(True)

        access = data_handler.check_credentials(username, password,organization)
        if (access == 0):
            self.setUser(username)
            if ('physician' == data_handler.get_attribute(username, 'role')):
                self.toClinicianScreen()
            elif ('patient' == data_handler.get_attribute(username, 'role')):
                self.toPatientHomeScreen()
            else:
                # TODO - dont allow role to be something other than PATIENT or PHYSICIAN
                self.loginWindow.login_message.setText(self.restricted_access)
                self.loginWindow.login_message.setStyleSheet("color: red;")
                self.loginWindow.login_message.setHidden(False)
        elif (access == 1):
            self.loginWindow.login_message.setText(self.password_incorrect+" or incorrect organization")
            self.loginWindow.login_message.setStyleSheet("color: red;")
            self.loginWindow.login_message.setHidden(False)
        else:
            self.loginWindow.login_message.setText(self.username_doesnt_exist)
            self.loginWindow.login_message.setStyleSheet("color: red;")
            self.loginWindow.login_message.setHidden(False)

    def setUser(self, username):
        self.user = username

    def getUser(self):
        return self.user

    def toClinicianScreen(self):  # function to add to a list to transistion to next window
        self.loginWindow.hide()
        self.clearFields()
        self.mainScreen = MainWindow()

    def toPatientHomeScreen(self):
        self.loginWindow.hide()
        self.clearFields()
        self.mainScreen = MainWindowPatient()

    def clearFields(self):
        self.loginWindow.password.clear()
        self.loginWindow.username.clear()
        self.loginWindow.organization.clear()


if __name__ == "__main__":
    data_handler = CSVHandler()
    data_handler.updatePatientDict()
    loader = QUiLoader()
    app = QApplication(sys.argv)
    window = login()
    sys.exit(app.exec_())