
from algorithm import Algorithm, register

@register('naive')
class Naive(Algorithm):
	def pack(self, settings, sprites):
		'''
		settings: settings dictionary 
		sprites: list of Sprite objects
		'''
		size = settings['size']	

		x, y = 0, 0
		cur_max_y = 0
		
		pad = settings['padding']
	
		c = len(sprites)	
		i = 0
		while i < c:
			sprite = sprites[i]
			print i, x, y
			#x += sprite.width + settings['padding'] 
			if y + sprite.height + pad*2 > size[1]:
				self.error = "Can't fit all sprites"
				return False
			elif x + sprite.width + pad*2 >= size[0]:
				y += cur_max_y + pad*2
				cur_max_y = 0 
				x = 0
				# Notice that i is not added!
			else:
				sprite.position = (x+pad, y+pad)	
				cur_max_y = max(cur_max_y, y + sprite.height)
				x += sprite.width + pad*2
				i += 1


		return True
