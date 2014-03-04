import pilas
import random 

class Fruta(pilas.actores.Manzana):
	"fruta de comer "

	def __init__(self,cantidad,x=0,y=0):
		pilas.actores.Manzana.__init__(self,x=x,y=y)
		self.sonido_salto= pilas.sonidos.cargar('data/sonido/smb_jump-small.wav')
		self.cantidad= cantidad

	def eliminar(self):
		"se activa cuando el personaje toque la manzana "
		pilas.actores.Manzana.eliminar(self)
		self.sonido_salto.reproducir()

	

