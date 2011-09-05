
from algorithm import Algorithm, register

@register('simple')
class Simple(Algorithm):
    '''This is a very simple one that works for me right now, not a strong one generally'''
    def pack(self, settings, sprites):
        size = settings['size'] 

        x, y = 0, 0
        cur_max_y = 0
        
        pad = settings['padding']

        for sprite in sprites:
            if sprite.height > sprite.width:
                sprite.rotated = True
                # Now, sprite.height/width will be flipped


        # Sort the sprites
        sprites_sorted = sorted(sprites, cmp=lambda x, y: cmp(x.height, y.height))
    
        c = len(sprites)    
        i = 0
        while i < c:
            sprite = sprites_sorted[i]

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
                cur_max_y = max(cur_max_y, sprite.height)
                x += sprite.width + pad*2
                i += 1


        return True
