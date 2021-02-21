#!/usr/bin/env python3

import sys, os
import time
from time import sleep
import numpy as np

from PyQt5 import QtGui, QtCore

from PyQt5 import uic
from PyQt5.QtGui import QMovie, QPainter, QPixmap
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QMainWindow, QDialog, QApplication, QPushButton, QVBoxLayout, QAction, QMenu, QFileDialog 

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

from busca_largura import buscaLargura #clase que implementa a busca por largura
from busca_profundidade import buscaProfundidade #clase que implementa a busca por profundidade

Ui_MainWindow, QtBaseClass = uic.loadUiType("trabalho_01.ui")

class MainWindow(QMainWindow, Ui_MainWindow, buscaLargura, buscaProfundidade):
	
	def __init__(self, parent=None):        
		QMainWindow.__init__(self)
		Ui_MainWindow.__init__(self)		
		self.setupUi(self) 

		#para colocar robo animado
		self.movie = QMovie("robot.gif")
		self.movie.frameChanged.connect(self.repaint)
		self.movie.start()

		self.timer = QTimer(self)

		self.paredes = 0
		self.caminho = 1
		self.entrada = 2
		self.saida = 3	
		self.pegadas = 4
		self.jaVisitado = 5
		self.labirinto = []

		#para armazenar historico do percurso
		self.fila_i = []
		self.fila_j = []
		self.fila_pegadas = []

		self.createActions()
		self.createMenus()
		self.pushButton01.clicked.connect(self.simule)
		self.pushButton02.clicked.connect(self.limparCaminhada)

		self.events()
		self.timer.setInterval(300)
		self.timer.start()

	#funcao que anima robo
	def paintEvent(self, event):
		currentFrame = self.movie.currentPixmap()
		frameRect = currentFrame.rect()
		frameRect.moveCenter(self.rect().center())
		if frameRect.intersects(event.rect()):
			painter = QPainter(self)
			painter.drawPixmap(frameRect.left(), frameRect.top(), currentFrame)

	def events(self):
		self.timer.timeout.connect(self.update)

	def update(self):
		if(len(self.labirinto) > 0 and len(self.fila_pegadas) > 0):
			self.alteraLabirinto()
			self.aplicateColors()		
			self.pushButton02.setEnabled(True)

	def simule(self):
		if(self.radioButton01.isChecked()):	
			self.limparCaminhada()
			self.buscaEmLargura()	
		elif(self.radioButton02.isChecked()):	
			self.limparCaminhada()
			self.buscaEmProfundidade()		
		else:
			return	

	def limparCaminhada(self):
		self.clear()
		self.labirinto = np.loadtxt(self.filename[0], dtype='int', delimiter='	')
		self.aplicateColors()	
		self.fila_i.clear()	
		self.fila_j.clear()	
		self.fila_pegadas.clear()	

	def alteraLabirinto(self):
		if(len(self.fila_pegadas) > 0):
			self.labirinto[self.fila_i[0]][self.fila_j[0]] = self.fila_pegadas[0]	
			self.fila_i.pop(0)	
			self.fila_j.pop(0)
			self.fila_pegadas.pop(0)	

	def buscaEmLargura(self):
		self.variavel = buscaLargura(self.filename[0])
		self.fila_i,self.fila_j,self.fila_pegadas = self.variavel.percorreLabirinto()
		#print(self.fila_i, self.fila_j, self.fila_pegadas)

	def buscaEmProfundidade(self):
		self.variavel = buscaProfundidade(self.filename[0])
		self.fila_i,self.fila_j,self.fila_pegadas = self.variavel.percorreLabirinto()
		#print(self.fila_i, self.fila_j, self.fila_pegadas)

	def createActions(self):
		self.openAct = QAction("&Open Archive", self, shortcut="Ctrl+O", triggered=self.open)   

	def open(self):
		self.filename = QFileDialog.getOpenFileName(self, 'Open File', os.getenv('HOME'))   
		self.labirinto = np.loadtxt(self.filename[0], dtype='int', delimiter='	')

		self.movie = QMovie() #retirando robozinho		
		
		self.aplicateColors()		

		self.pushButton01.setEnabled(True) 
		self.radioButton01.setEnabled(True) 
		self.radioButton02.setEnabled(True) 			
		#print(self.labirinto)	
		#self.label.setText(filename[0])

	def clear(self):
		while self.gridLayout_3.count():
			item = self.gridLayout_3.takeAt(0)
			widget = item.widget()
			widget.deleteLater()

	def createMenus(self):
		self.fileMenu = QMenu("&Menu", self)
		self.fileMenu.addSeparator()
		self.fileMenu.addAction(self.openAct)        
		self.fileMenu.addSeparator()       

		self.menuBar().addMenu(self.fileMenu)  

	def aplicateColors(self): 
		sleep(0.3)  
		self.clear() 	
		for i in range(len(self.labirinto)):
			for j in range(len(self.labirinto)):
				if(self.labirinto[i][j] == self.caminho or self.labirinto[i][j] == self.jaVisitado):
					self.b1 = QPushButton("pushButton_"+str(i)+"_"+str(j))  
					self.b1.setStyleSheet("background-color : white")
					self.b1.setFixedSize(500/len(self.labirinto), 500/len(self.labirinto))
					self.b1.setText(" ")
					self.b1.setEnabled(False)
					self.gridLayout_3.addWidget(self.b1,i,j)
				elif(self.labirinto[i][j] == self.paredes ):
					self.b1 = QPushButton("pushButton_"+str(i)+"_"+str(j))  
					self.b1.setStyleSheet("background-color : black")
					self.b1.setFixedSize(500/len(self.labirinto), 500/len(self.labirinto))
					self.b1.setText(" ") 
					self.b1.setEnabled(False) 
					self.gridLayout_3.addWidget(self.b1,i,j)
				elif(self.labirinto[i][j] == self.entrada ):
					self.b1 = QPushButton("pushButton_"+str(i)+"_"+str(j))  
					self.b1.setStyleSheet("background-color : red")  
					self.b1.setFixedSize(500/len(self.labirinto), 500/len(self.labirinto))
					self.b1.setText(" ")
					self.b1.setEnabled(False)
					self.gridLayout_3.addWidget(self.b1,i,j)
				elif(self.labirinto[i][j] == self.saida ):
					self.b1 = QPushButton("pushButton_"+str(i)+"_"+str(j))  
					self.b1.setStyleSheet("background-color : green")  
					self.b1.setFixedSize(500/len(self.labirinto), 500/len(self.labirinto))
					self.b1.setText(" ")
					self.b1.setEnabled(False)
					self.gridLayout_3.addWidget(self.b1,i,j)
				elif(self.labirinto[i][j] == self.pegadas ):
					self.b1 = QPushButton("pushButton_"+str(i)+"_"+str(j))  
					self.b1.setStyleSheet("background-color : yellow")  
					self.b1.setFixedSize(500/len(self.labirinto), 500/len(self.labirinto))
					self.b1.setText(" ")
					self.b1.setEnabled(False)
					self.gridLayout_3.addWidget(self.b1,i,j)
				else:
					return

if __name__ == '__main__':
	app = QApplication(sys.argv)

	main = MainWindow()
	main.show()

	sys.exit(app.exec_())
