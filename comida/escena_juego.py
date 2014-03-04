import pilas
import frutas
import comelon
import mapa
import random 

#teclas = {pilas.simbolos.a:'izquierda',pilas.simbolos.d:'derecha',pilas.simbolos.ESPACIO:'arriba'}
#mandos= pilas.control.Control(pilas.escena_actual(),teclas)

class Estado:
	"Representa un estado dentro del juego."

	def actualizar(self):
		pass


class Jugando(Estado):
	"representa el estado del juego "

	def __init__(self,juego,nivel):
		self.nivel = nivel
		self.juego = juego 
		self.juego.crear_frutas(cantidad= nivel * 3)
		pilas.mundo.agregar_tarea(1,self.actualizar)
		pilas.mundo.agregar_tarea(1/10.0, self.cambiar_posicion_camara)


	def actualizar(self):
		if self.juego.ha_eliminado_todas_las_frutas():
			self.juego.cambiar_estado(Iniciando(self.juego,self.nivel+1))
			return False

		return True 

	def cambiar_posicion_camara(self):
		p = self.juego.personaje
		pilas.escena_actual().camara.x = [p.x], 0.1
		return True




class Iniciando(Estado):
	"Estado cuando comienza el juego "


	def __init__(self,juego,nivel):
		self.texto = pilas.actores.Texto("Iniciando el nivel %d" % (nivel))
		self.nivel = nivel 
		self.texto.color = pilas.colores.blanco
		self.contador_de_segundos= 0
		self.juego = juego 

		pilas.mundo.agregar_tarea(1,self.actualizar)
		
	def actualizar (self):
		self.contador_de_segundos += 1
		if self.contador_de_segundos > 2:
			self.juego.cambiar_estado(Jugando(self.juego,self.nivel))
			self.texto.eliminar()
			return False

		return True 

class Juego(pilas.escena.Base):
	"Escena del jugador "

	def __init__(self):
		pilas.escena.Base.__init__(self)

	def iniciar(self):
		#pilas.fondos.Espacio()
		#pilas.fondos.Fondo('data/mapa/fondoMario.png')
		self.frutas = []
		self.crear_comelon()
		self.cambiar_estado(Iniciando(self,1))
		self.puntaje = pilas.actores.Puntaje(x=280,y=220,color=pilas.colores.blanco)
		pilas.actores.Texto("Comidas : ",x=200,y=220)

	def cambiar_estado(self,estado):
		self.estado = estado

	def crear_comelon(self):
		#comelon = pilas.actores.Nave()
		mapa_juego = mapa.crear_mapa()
		personaje_comelon = comelon.Comelon(mapa_juego,y=170)
		self.personaje=personaje_comelon
		self.colisiones.agregar(personaje_comelon,self.frutas,self.comer_fruta)

	def cuando_explota_asteroide(self):
		pass
		#self.puntaje.aumentar(1)

	def crear_frutas(self,cantidad):
		for rango in range(0,cantidad):
			x = random.randrange(-320,320)
			y = random.randrange(-240,240)
			self.frutas.append(frutas.Fruta(cantidad,x=x,y=-y))

	def comer_fruta(self,personaje,fruta):
		fruta.eliminar()
		self.puntaje.aumentar(1)
		#self.frutas.eliminar()

	def ha_eliminado_todas_las_frutas(self):
		return len(self.frutas) ==0

	def personaje_principal(self):
		return 


