import sys
sys.path.insert(0, "..")
import pilas


#teclas = {pilas.simbolos.a:'izquierda',pilas.simbolos.d:'derecha',pilas.simbolos.ESPACIO:'arriba'}
#mandos= pilas.control.Control(pilas.escena_actual(),teclas)

class Comelon(pilas.actores.Actor):

	def __init__(self,mapa,x=0,y=0):
		pilas.actores.Actor.__init__(self,x=0,y=0)
		self.imagen= pilas.imagenes.cargar_grilla('data/martian.png',12)
		
		self.definir_cuadro(0)
		self.mapa= mapa
		self.hacer(Esperando())
		self.velocidad = 3
		#self.radio_de_colision = 20

		#self.cuadro = 0
		#que se mueva con el comportamiento personalizado
		#self.aprender(pilas.habilidades.MoverseConElTeclado,control=mandos)
		#self.aprender(pilas.habilidades.SeMantieneEnPantalla)
		self.colisiona_arriba_izquierda = False 
		self.colisiona_arriba_derecha = False
		self.colisiona_abajo_izquierda = False
		self.colisiona_abajo_derecha = False

		self.obtener_colisiones()

	def definir_cuadro(self,indice):
		self.imagen.definir_cuadro(indice)
		self.definir_centro((32,68))

	def puese_saltar(self):
		return True 

	def obtener_distancia_al_suelo(self):
		"retorn la distancia en pixeles del suelo"
		return self.mapa.obtener_distancia_al_suelo(self.x, self.y, 100)

	def obtener_colisiones(self):
		self.colisiona_arriba_izquierda = self.mapa.es_punto_solido(self.izquierda,self.arriba)
		self.colisiona_arriba_derecha = self.mapa.es_punto_solido(self.derecha,self.arriba)
		self.colisiona_abajo_izquierda = self.mapa.es_punto_solido(self.izquierda,self.abajo)
		self.colisiona_abajo_derecha = self.mapa.es_punto_solido(self.derecha,self.abajo)



class Esperando(pilas.comportamientos.Comportamiento):
	"actor en posicion normal o esperando a que el usuario pulse alguan tecla "
	def iniciar(self,receptor):
		self.receptor= receptor
		self.receptor.definir_cuadro(0)


	def actualizar(self):
		
		if pilas.escena_actual().control.izquierda: 
			self.receptor.hacer(Caminando())
		elif pilas.escena_actual().control.derecha:
			self.receptor.hacer(Caminando())
		if pilas.escena_actual().control.arriba:
			self.receptor.hacer(Saltando(-9))



		self.caer_si_no_toca_el_suelo()

	def caer_si_no_toca_el_suelo(self):
		if self.receptor.obtener_distancia_al_suelo() > 0 :
			self.receptor.hacer(Saltando(0))

class Caminando(Esperando):

	def __init__(self):
		self.cuadros=[1,1,1,2,2,2]
		self.paso = 0
		

	def iniciar(self,receptor):
		self.receptor = receptor
		#self.cuadros = [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5]


	def actualizar(self):
		self.avanzar_animacion()
		vx = 0

		if pilas.escena_actual().control.izquierda:
			vx = -(self.receptor.velocidad)
			if not self.receptor.espejado:
				self.receptor.espejado = True
			#self.receptor.x -= VELOCIDAD
			self.receptor.obtener_colisiones()
			if not(self.receptor.colisiona_arriba_izquierda or self.receptor.colisiona_abajo_izquierda):
				self.receptor.x += vx

		elif pilas.escena_actual().control.derecha:
			vx =  self.receptor.velocidad
			if self.receptor.espejado:
				self.receptor.espejado = False 
			#self.receptor.x += VELOCIDAD
			self.receptor.obtener_colisiones()
			if not(self.receptor.colisiona_arriba_derecha or self.receptor.colisiona_abajo_derecha):
				self.receptor.x +=vx
		else:
			self.receptor.hacer(Esperando())

		if pilas.escena_actual().control.arriba:
			self.receptor.hacer(Saltando(-9))


		self.caer_si_no_toca_el_suelo()


	def caer_si_no_toca_el_suelo(self):
		if self.receptor.obtener_distancia_al_suelo() > 0:
			self.receptor.hacer(Saltando(0))

	def avanzar_animacion(self):
		self.paso += 1
		if self.paso >= len(self.cuadros):
			self.paso=0

		self.receptor.definir_cuadro(self.cuadros[self.paso])

class Saltando(pilas.comportamientos.Comportamiento):
	"Actor saltando"
	def __init__(self,velocidad_de_salto):
		self.velocidad_de_salto = velocidad_de_salto
		pilas.comportamientos.Comportamiento.__init__(self)


	def iniciar(self,receptor):
		self.receptor=receptor
		self.receptor.definir_cuadro(3)
		#self.origen = self.receptor.y 
		#self.dy=10

	def actualizar(self):
		#self.receptor.y += self.dy
		#self.dy -= 0.3
		self.velocidad_de_salto += 0.25
		distancia=self.receptor.obtener_distancia_al_suelo()

		if self.velocidad_de_salto > distancia:
			self.receptor.y -= distancia
			self.receptor.hacer(Esperando())
		else:
			self.receptor.y -= self.velocidad_de_salto

		vx, vy = 0, 0 

		if pilas.escena_actual().control.izquierda:
			vx = -(self.receptor.velocidad)
			self.receptor.espejado =True
			self.receptor.obtener_colisiones()
			if not (self.receptor.colisiona_arriba_izquierda or self.receptor.colisiona_abajo_izquierda):
				self.receptor.x += vx 

		elif pilas.escena_actual().control.derecha:
			vx = self.receptor.velocidad
			self.receptor.espejado = False
			self.receptor.obtener_colisiones()
			if not (self.receptor.colisiona_arriba_derecha or self.receptor.colisiona_abajo_derecha):
				self.receptor.x += vx 


		#if self.receptor.y < self.origen:
		#	self.receptor.y = self.origen
		#	self.receptor.hacer(Esperando())

		#if mandos.izquierda:
		#	self.receptor.x -= VELOCIDAD
		#elif mandos.derecha:
		#	self.receptor.x += VELOCIDAD