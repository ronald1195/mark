from PyQt5.QtWidgets import (QMainWindow, QApplication, QMenu, QMenuBar, QAction, QFileDialog, QDialog,
                             QDesktopWidget, QLabel, QGraphicsScene, QToolBar, QStatusBar, QSpacerItem, 
                             QSizePolicy, QSplitter, QListView, QTableView, QTreeView, QFileSystemModel,
                             QHBoxLayout, QTextEdit, QScrollArea, QMessageBox, QProgressDialog, QFileDialog)
from PyQt5.QtGui import (QIcon, QImage, QPainter, QPen, QBrush, QPixmap, QPalette)
from PyQt5.QtCore import Qt, QPoint, QPointF, QSize, QDir, QTimer, QObject
from PyQt5 import QtCore, QtGui
import sys
import os
import shutil

from Mark2 import *

#################################################################################################
# Main Window
################################################################################################
class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        QObject.__init__(self)
        ############################################################
        # General Window settings
        ############################################################
        #self.initializeGUIComponents()

        self.InitUI()
        self.setInitialWindowProperties()
                
        
#################################################################################################
# Set the intial properties for the window
#   * Color
#   * Size
#   ... You can think about anything here..
#################################################################################################
    def InitUI(self):
        # LEFT
        #   Add a fileviewer
        model = QFileSystemModel()
        model.setRootPath(QDir.rootPath())

        self.list = QTreeView()
        self.list.setModel(model)
        self.list.header().resizeSection(0,300)
        self.list.setRootIndex(model.index( QDir.homePath() ))
        #/ Users / ronaldmunoz / Developer / Python / Mark / Templates
        # RIGHT
        #   Add a preview
        self.imageLabel = QLabel()
        self.selectedFile = ""
        self.imageArray = []
        self.arrayOfFileNames = []
        self.dir = QDir()

        # PROGRESS BAR
        self.steps = 0

        # self.imageLabel.setBackgroundRole(QPalette.Base)
        self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.imageLabel.setScaledContents(True)

        # Set the values for the scroll area
        self.scrollArea = QScrollArea()
        self.scrollArea.setBackgroundRole(QPalette.Dark)
        self.scrollArea.setWidget(self.imageLabel)

        # CONTAINER WIDGET
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.addWidget(self.list)
        self.splitter.addWidget(self.scrollArea)
        self.splitter.setSizes([500, 400])

        # CENTRAL WIDGET
        self.setCentralWidget(self.splitter)


        # Double Click gesture
        self.list.doubleClicked.connect(self.displaySelectedImage)

        ############################################################
        # Toolbar
        ############################################################

        # TOOLBAR SETTINGS
        #   Name
        #   Icon size
        toolbar = QToolBar("Main toolbar")
        toolbar.setIconSize(QSize(16,16))

        #spacer =
        #spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        #   Add toolbar to the main window        
        self.addToolBar(toolbar)
        self.createActions()
        self.createMenus()
        
        # BUTTONS ON THE TOOLBAR
        self.create_new = QAction("New Template", self)
        self.create_new.setStatusTip("Create a new template from an image")
        self.create_new.triggered.connect(self.CreateTemplate)
        toolbar.addAction(self.create_new)


        self.apply_template = QAction("Apply Template", self)
        self.apply_template.setStatusTip("Apply selected file to image/images")
        self.apply_template.triggered.connect(self.ApplyTemplate)
        toolbar.addAction(self.apply_template)
        
        self.setStatusBar(QStatusBar(self))


    def getFilePath(self, signal):
        file_path=self.list.model().filePath(signal)
        print(file_path)

    def displaySelectedImage(self, signal):
        self.selectedFile = self.list.model().filePath(signal)

        if self.selectedFile:
            image = QImage(self.selectedFile)
            if image.isNull():
                #QMessageBox.information(self, "Image Viewer",
                        #"Cannot load %s." % selectedFile)
                return

            self.pixmap = QPixmap.fromImage(image)

            self.imageLabel.setPixmap(QPixmap.fromImage(image))

            #self.imageLabel.setPixmap(QPixmap.fromImage(image).scaled(self.scrollArea.size(), Qt.KeepAspectRatio))
            self.imageLabel.resize(self.scrollArea.size())

            self.scaleFactor = 1.0

            #self.printAct.setEnabled(True)
            
            #self.fitToWindowAct.setEnabled(True)
            #self.updateActions()

            self.scrollArea.setAlignment(Qt.AlignCenter)

            # print("Size of image label: " + str(self.imageLabel.size()))
            # print("Size of frame:       " + str(self.scrollArea.size()))
            # print("Pixmap size:         " + str(self.pixmap.size()))

            width_scaled = 1 / (self.pixmap.width() / self.scrollArea.width())

            # print("Using: " + str( width_scaled ) )

            self.scaleImage(width_scaled)

    def scaleImage(self, factor):
        #subprint("Scaling image...\nScale factor: " +  str(factor) )
        self.scaleFactor *= factor
        self.imageLabel.resize(self.scaleFactor * self.imageLabel.pixmap().size())

        self.adjustScrollBar(self.scrollArea.horizontalScrollBar(), factor)
        self.adjustScrollBar(self.scrollArea.verticalScrollBar(), factor)

        #self.zoomInAct.setEnabled(self.scaleFactor < 3.0)
        #self.zoomOutAct.setEnabled(self.scaleFactor > 0.05)

    def adjustScrollBar(self, scrollBar, factor):
        scrollBar.setValue(int(factor * scrollBar.value()
                                + ((factor - 1) * scrollBar.pageStep()/2)))

    def zoomIn(self):
        self.scaleImage(1.25)

    def zoomOut(self):
        self.scaleImage(0.8)


    def setInitialWindowProperties(self):
        # This is the stylesheet that is going to manage all the colors in the main window

        # WINDOW SETTINGS:
        #   Name
        #   Size
        #   Position
        self.title = "Mark"
        self.left = 0
        self.top = 0
        self.width = 1000
        self.height = 600


        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle(self.title)
        #self.setStyleSheet(self.styleSheet1);
        self.centerScreen()
        self.setMinimumSize(self.width-100, self.height-100);

    def initializeGUIComponents(self):
        #Values for the plus button
        #self.addButton = QPushButton("New Mark", self)
        self.addButton.setObjectName("addButton")
        self.addButton.setGeometry(self.width,self.height,80, 30)

    def CreateTemplate(self):
        #self.create_new.setCheckable(True)
        print("click")
        self.p2 = MainWindow2()
        self.p2.show()

    def ApplyTemplate(self):

        if self.selectedFile == "":
            buttonReply = QMessageBox.question(self, 'Warning!',
                                               "No template selected. Please select a template.?", QMessageBox.Ok)
            if buttonReply == QMessageBox.Ok:
                print('Ok clicked.')
        else:
            self.getFile()

            apply_to_directory = QMessageBox.question(self, 'Warning!',
                                               "Apply template to other files in this directory?", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

            if apply_to_directory == QMessageBox.Yes:
                # print("The user wants to apply this template  ")
                self.getDirectory()

            # message_before_save = QMessageBox.question(self, 'Warning!',
            #                                    "Select a folder to save your files", QMessageBox.Ok)
            #
            # self.dir = QFileDialog.getExistingDirectory(self, str("Open Directory"),
            #                                        "/home",
            #                                        QFileDialog.ShowDirsOnly
            #                                        | QFileDialog.DontResolveSymlinks)

            print("**************************************************")
            print("The template will be applied to: ")
            print("**************************************************")

            for word in self.imageArray:
                  print(word)

            print("**************************************************")

            self.processImages()

    def processImages(self):
        template = QPixmap(self.selectedFile)
        tmp_index = 0

        progress = QProgressDialog("Processing files...", "Cancel", 0, len(self.arrayOfFileNames), self)
        progress.setWindowModality(Qt.WindowModal)
        progress.resize(500,100)
        progress.move(0,-100)


        # if os.path.exists(self.workingDirectory + "/edited"):
        #     shutil.rmtree(self.workingDirectory + "/edited")
        #
        # os.makedirs(self.workingDirectory + "/edited")
        # #os.mkdir(self.workingDirectory + "/edited")

        infoMessage = QMessageBox.question(self, 'Info!',
                             "Select a destination folder",
                            QMessageBox.Ok | QMessageBox.Ok)

        self.destDir = QFileDialog.getExistingDirectory(None,
                                                   'Open working directory',
                                                    QDir.homePath(),
                                                    QFileDialog.ShowDirsOnly)

        for temp_image in self.imageArray:

            temp_qimage = QPixmap(temp_image)
            progress.setValue(tmp_index)

            if progress.wasCanceled():
                break

            if not temp_qimage.isNull():

                template = template.scaled(temp_qimage.size(), Qt.IgnoreAspectRatio)

                result_image = QPixmap(temp_qimage.width(), temp_qimage.height())
                result_image.fill(Qt.transparent)

                painter = QPainter(result_image)
                painter.drawPixmap(0,0,temp_qimage)
                painter.drawPixmap(0,0,template)

                # print("Files will be saved at:")
                # print(self.workingDirectory + "/edited/" + self.arrayOfFileNames[tmp_index])
                result_image.save(self.destDir + "/" + self.arrayOfFileNames[tmp_index])

                painter.end()

            # print("2 Index : {}".format(tmp_index))

            tmp_index = tmp_index + 1

        progress.setValue(len(self.arrayOfFileNames))

        infoMessage = QMessageBox.question(self, 'Info!',
                                           "All your images have been processed!",
                                           QMessageBox.Ok | QMessageBox.Ok)




    def getDirectory(self):
        self.imageArray.clear()
        self.arrayOfFileNames.clear()

        for file in os.listdir(self.workingDirectory):
            self.arrayOfFileNames.append(file)
            self.imageArray.append(self.workingDirectory + "/" +file)


    def getFile(self):

        self.imageArray.clear()
        self.arrayOfFileNames.clear()
        self.homedir = os.environ['HOME']
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Choose a file to apply the template to", str(self.homedir+"/Documents"),
                                                  "All Files (*);;Python Files (*.py)", options=options)

        self.arrayOfFileNames.append(str(os.path.basename(fileName)))
        self.imageArray.append(fileName)
        self.workingDirectory = os.path.dirname(fileName)


    def centerScreen (self):
        '''centerOnScreen()
        Centers the window on the screen.'''
        resolution = QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2))

    def createActions(self):
        self.exitAct = QAction("E&xit", self, shortcut="Ctrl+Q",
                triggered=self.close)

        self.zoomInAct = QAction("Zoom &In (25%)", self, shortcut="Ctrl++",
                enabled=False, triggered=self.zoomIn)

        self.zoomOutAct = QAction("Zoom &Out (20%)", self, shortcut="Ctrl+-",
                enabled=False, triggered=self.zoomOut)

        self.zoomInAct.setEnabled(True)
        self.zoomOutAct.setEnabled(True)
        
    def createMenus(self):
        self.viewMenu = QMenu("&View", self)
        self.viewMenu.addAction(self.zoomInAct)
        self.viewMenu.addAction(self.zoomOutAct)

        self.menuBar().addMenu(self.viewMenu)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()