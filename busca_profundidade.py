import numpy as np
import random

class Pilha(object):
	def __init__(self):
		self.dados = []

	def retorna(self):		
		return self.dados[-1]
 
	def empilha(self, elemento):
		self.dados.append(elemento)
 
	def desempilha(self):
		if not self.vazia():
			return self.dados.pop(-1)
 
	def vazia(self):
		return len(self.dados) == 0


class buscaProfundidade():
	
	def __init__(self, arq, parent=None):      
		self.paredes = 0
		self.caminho = 1
		self.entrada = 2
		self.saida = 3	
		self.pegadas = 4
		self.jaVisitado = 5
		self.pilha_Direcoes = Pilha()	

		self.fila_Eventos_i = []
		self.fila_Eventos_j = []
		self.fila_Eventos_pegadas = []		

		self.labirinto = np.loadtxt(arq, dtype='int', delimiter='	')					
		self.posInicial() #achando posicao inicial e final no labirinto	

	def posInicial(self):
		for i in range(len(self.labirinto)):
			for j in range(len(self.labirinto)):
				if(self.labirinto[i][j] == self.entrada):
					self.pos_i = i
					self.pos_j = j					

	def percorreLabirinto(self):
		while(True): #enquanto ele nao achar a saida
			if(self.temDirecaoDisponivel() == True): #se existir alguma posicao disponivel para percorrer ou seja que nao seja parede ou caminho ja percorrido
				self.direcao = random.randrange(4) #sorteando uma direcao a andar 0=norte 1=sul 2=leste 3=oeste
				if(self.verificaDirecao(self.direcao) == True): #verificando se direcao eh valida para andar
					if(self.labirinto[self.pos_i][self.pos_j] == self.saida):						
						return(self.fila_Eventos_i, self.fila_Eventos_j, self.fila_Eventos_pegadas)	

					self.fila_Eventos_i.append(self.pos_i)
					self.fila_Eventos_j.append(self.pos_j)
					self.fila_Eventos_pegadas.append(self.pegadas)

					self.labirinto[self.pos_i][self.pos_j] = self.pegadas #colocando pegada
					self.pilha_Direcoes.empilha(self.direcao)

			elif(self.temDirecaoDisponivelPegadas() == True): #se existir alguma posicao disponivel para percorrer ou seja que nao seja parede ou caminho ja percorrido
				self.direcao = random.randrange(4) #sorteando uma direcao a andar 0=norte 1=sul 2=leste 3=oeste
				if(self.verificaDirecaoPegadas(self.direcao) == True): #verificando se direcao eh valida para andar
					if(self.labirinto[self.pos_i][self.pos_j] == self.saida):						
						return(self.fila_Eventos_i, self.fila_Eventos_j, self.fila_Eventos_pegadas)	

					self.fila_Eventos_i.append(self.pos_i)
					self.fila_Eventos_j.append(self.pos_j)
					self.fila_Eventos_pegadas.append(self.pegadas)

					self.labirinto[self.pos_i][self.pos_j] = self.pegadas #colocando pegada
					self.pilha_Direcoes.empilha(self.direcao)

			else: #nao tem nenhum novo caminho valido para andar entao devo voltar para o caminho onde se estava anteriormente
				self.voltaDirecaoAnterior() #usando variavel que armazenou a direcao anterior para voltar																	

	def temDirecaoDisponivel(self):
		contador = 0
		if((self.pos_i-1 >= 0 and self.labirinto[self.pos_i-1][self.pos_j] == self.caminho) or (self.pos_i-1 >= 0 and self.labirinto[self.pos_i-1][self.pos_j] == self.saida)):
			contador += 1
		elif((self.pos_i+1 <= len(self.labirinto)-1 and self.labirinto[self.pos_i+1][self.pos_j] == self.caminho) or (self.pos_i+1 <= len(self.labirinto)-1 and self.labirinto[self.pos_i+1][self.pos_j] == self.saida)): 
			contador += 1
		elif((self.pos_j-1 >= 0 and self.labirinto[self.pos_i][self.pos_j-1] == self.caminho) or (self.pos_j-1 >= 0 and self.labirinto[self.pos_i][self.pos_j-1] == self.saida)):
			contador += 1
		elif((self.pos_j+1 <= len(self.labirinto)-1 and self.labirinto[self.pos_i][self.pos_j+1] == self.caminho) or (self.pos_j+1 <= len(self.labirinto)-1 and self.labirinto[self.pos_i][self.pos_j+1] == self.saida)):
			contador += 1

		if(contador > 0):
			return True
		else:
			return False 

	def temDirecaoDisponivelPegadas(self):
		contador = 0
		if((self.pos_i-1 >= 0 and self.labirinto[self.pos_i-1][self.pos_j] == self.pegadas)):
			contador += 1
		if((self.pos_i+1 <= len(self.labirinto)-1 and self.labirinto[self.pos_i+1][self.pos_j] == self.pegadas)): 
			contador += 1
		if((self.pos_j-1 >= 0 and self.labirinto[self.pos_i][self.pos_j-1] == self.pegadas)):
			contador += 1
		if((self.pos_j+1 <= len(self.labirinto)-1 and self.labirinto[self.pos_i][self.pos_j+1] == self.pegadas)):
			contador += 1

		if(contador > 1):
			return True
		else:
			return False 

	def verificaDirecaoPegadas(self,valor):
		if(valor == 0): #caso seja direcao norte (para cima)
			if((self.pos_i-1 >= 0 and self.labirinto[self.pos_i-1][self.pos_j] == self.pegadas) or (self.pos_i-1 >= 0 and self.labirinto[self.pos_i-1][self.pos_j] == self.saida)): #caso a posicao seja valida e a posicao valida nao seja parede
				self.pos_i -= 1				
				return True
			else:
				return False

		elif(valor == 1): #caso seja direcao sul (para baixo)
			if((self.pos_i+1 <= len(self.labirinto)-1 and self.labirinto[self.pos_i+1][self.pos_j] == self.pegadas) or (self.pos_i+1 <= len(self.labirinto)-1 and self.labirinto[self.pos_i+1][self.pos_j] == self.saida)): #caso a posicao seja valida e a posicao valida nao seja parede
				self.pos_i += 1
				return True
			else:
				return False

		elif(valor == 2): #caso seja direcao leste (para esquerda)
			if((self.pos_j-1 >= 0 and self.labirinto[self.pos_i][self.pos_j-1] == self.pegadas) or (self.pos_j-1 >= 0 and self.labirinto[self.pos_i][self.pos_j-1] == self.saida)): #caso a posicao seja valida e a posicao valida nao seja parede
				self.pos_j -= 1
				return True
			else:
				return False

		elif(valor == 3): #caso seja direcao oeste (para direita)
			if((self.pos_j+1 <= len(self.labirinto)-1 and self.labirinto[self.pos_i][self.pos_j+1] == self.pegadas) or (self.pos_j+1 <= len(self.labirinto)-1 and self.labirinto[self.pos_i][self.pos_j+1] == self.saida)): #caso a posicao seja valida e a posicao valida nao seja parede
				self.pos_j += 1
				return True
			else:
				return False	

	def verificaDirecao(self,valor):
		if(valor == 0): #caso seja direcao norte (para cima)
			if((self.pos_i-1 >= 0 and self.labirinto[self.pos_i-1][self.pos_j] == self.caminho) or (self.pos_i-1 >= 0 and self.labirinto[self.pos_i-1][self.pos_j] == self.saida)): #caso a posicao seja valida e a posicao valida nao seja parede
				self.pos_i -= 1				
				return True
			else:
				return False

		elif(valor == 1): #caso seja direcao sul (para baixo)
			if((self.pos_i+1 <= len(self.labirinto)-1 and self.labirinto[self.pos_i+1][self.pos_j] == self.caminho) or (self.pos_i+1 <= len(self.labirinto)-1 and self.labirinto[self.pos_i+1][self.pos_j] == self.saida)): #caso a posicao seja valida e a posicao valida nao seja parede
				self.pos_i += 1
				return True
			else:
				return False

		elif(valor == 2): #caso seja direcao leste (para esquerda)
			if((self.pos_j-1 >= 0 and self.labirinto[self.pos_i][self.pos_j-1] == self.caminho) or (self.pos_j-1 >= 0 and self.labirinto[self.pos_i][self.pos_j-1] == self.saida)): #caso a posicao seja valida e a posicao valida nao seja parede
				self.pos_j -= 1
				return True
			else:
				return False

		elif(valor == 3): #caso seja direcao oeste (para direita)
			if((self.pos_j+1 <= len(self.labirinto)-1 and self.labirinto[self.pos_i][self.pos_j+1] == self.caminho) or (self.pos_j+1 <= len(self.labirinto)-1 and self.labirinto[self.pos_i][self.pos_j+1] == self.saida)): #caso a posicao seja valida e a posicao valida nao seja parede
				self.pos_j += 1
				return True
			else:
				return False	

	def voltaDirecaoAnterior(self):	
		if(self.pilha_Direcoes.retorna() == 1):	
			if(self.pos_i-1 >= 0 and self.labirinto[self.pos_i-1][self.pos_j] == self.pegadas): #caso a posicao seja valida e a posicao valida  seja uma pegada
				self.labirinto[self.pos_i][self.pos_j] = self.pegadas
				self.pilha_Direcoes.desempilha()

				self.fila_Eventos_i.append(self.pos_i)
				self.fila_Eventos_j.append(self.pos_j)
				self.fila_Eventos_pegadas.append(self.pegadas)

				self.pos_i -= 1	

		elif(self.pilha_Direcoes.retorna() == 0):		
			if(self.pos_i+1 <= len(self.labirinto)-1 and self.labirinto[self.pos_i+1][self.pos_j] == self.pegadas):  #caso a posicao seja valida e a posicao valida  seja uma pegada
				self.labirinto[self.pos_i][self.pos_j] = self.pegadas
				self.pilha_Direcoes.desempilha()

				self.fila_Eventos_i.append(self.pos_i)
				self.fila_Eventos_j.append(self.pos_j)
				self.fila_Eventos_pegadas.append(self.pegadas)

				self.pos_i += 1

		elif(self.pilha_Direcoes.retorna() == 3):			
			if(self.pos_j-1 >= 0 and self.labirinto[self.pos_i][self.pos_j-1] == self.pegadas):  #caso a posicao seja valida e a posicao valida  seja uma pegada
				self.labirinto[self.pos_i][self.pos_j] = self.pegadas
				self.pilha_Direcoes.desempilha()

				self.fila_Eventos_i.append(self.pos_i)
				self.fila_Eventos_j.append(self.pos_j)
				self.fila_Eventos_pegadas.append(self.pegadas)

				self.pos_j -= 1		

		elif(self.pilha_Direcoes.retorna() == 2):
			if(self.pos_j+1 <= len(self.labirinto)-1 and self.labirinto[self.pos_i][self.pos_j+1] == self.pegadas):  #caso a posicao seja valida e a posicao valida  seja uma pegada
				self.labirinto[self.pos_i][self.pos_j] = self.pegadas
				self.pilha_Direcoes.desempilha()

				self.fila_Eventos_i.append(self.pos_i)
				self.fila_Eventos_j.append(self.pos_j)
				self.fila_Eventos_pegadas.append(self.pegadas)
				
				self.pos_j += 1	