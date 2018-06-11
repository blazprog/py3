gbox_name = QGridBoxLayout()
callerLabel = QLabel('Caller')
self.callerEdit = QLineEdit()

startLabel = QLabel('Start')
self.startDateTime = QLineEdit()

topicLabel = QLabel('Topic')
self.topicEdit = QLineEdit()

self.firstButton = QPushButton('first')
self.firstButton.clicked.connect(self.function_name)

self.lastButton = QPushButton('Last')
self.lastButton.clicked.connect(self.last)



