import pilas
import random 

class EscenaMenu(pilas.escena.Base):
	"Escena encargada de mostrar el menu de opciionel del juego"

	def __init__(self):
		pilas.escena.Base.__init__(self)

	def iniciar(self):
		pilas.fondos.Fondo('data/fondo.jpg')
		self.crear_titulo_del_juego()
		pilas.avisar(u'Use el teclado para controlar el menu')
		self.crear_el_menu_principal()


	def crear_titulo_del_juego(self):
		tituloJuego = pilas.actores.Actor("data/titulo.png")
		tituloJuego.y = 300
		tituloJuego.y = [200]

	def crear_el_menu_principal(self):
		opciones=[("Comensar a Jugar :) ", self.comenzar_a_jugar),
				("Salir ",self.salir_del_juego)]

		self.menu = pilas.actores.Menu(opciones,y=-50)

	def comenzar_a_jugar(self):
		import escena_juego
		pilas.cambiar_escena(escena_juego.Juego())

	def salir_del_juego(self):
		pilas.terminar()

