from scene import *
import sound
import random
import math
import time

A = Action
scl = 0.8
bomb_number = 30


def compute_time(time_ini, time_now):
	return time_now - time_ini
	
def random_pos(size):
	return (random.randrange(20, size[0]), random.randrange(size[1], 2 * size[1]))
			
def alive(player_lives, view):
	if player_lives <= 0:
		return False
	else: 
		return True
		
		
	

class MyScene (Scene):
	def setup(self):
		
		self.background_color = '#727fff'
		self.start_time = time.time()
		
		
		#self.player = SpriteNode('emj:Boy', position = (200, 200), parent = self, scale = 0.7)
		self.player = SpriteNode('emj:Aubergine', position = (200, 200), parent = self, scale = scl)
		self.player_lives = 1
		
		self.player_lives_Node = LabelNode(f"{self.player_lives} lives", position = self.size / 1.05, parent = self, color = 'yellow')
		self.time_Node = LabelNode(f"{0} seconds", position = (0, self.size[1] / 1.1), parent = self, color = "white")
		
		
		self.drops = [SpriteNode('emj:Bomb', (random.randrange(20, self.size[0]), random.randrange(self.size[1], 2 * self.size[1])), scale = scl, parent = self) for i in range(bomb_number)]
		
		self.load_view_bool = True
		
	def drops_in_screen(self):
		for drop in self.drops:
			if drop.position.y < - 50:
				del self.drops[self.drops.index(drop)]
				self.drops.append(SpriteNode('emj:Bomb', (random.randrange(20, self.size[0]), random.randrange(self.size[1] + 100, 2 * self.size[1])), scale = scl, parent = self))
				
			
	def did_change_size(self):
		pass
	
	def draw(self):

		self.time_now = time.time()
		self.time = compute_time(self.start_time, self.time_now)
		
		self.remove_all_Label()
		
		
		self.player_lives_Node = LabelNode(f"{self.player_lives} lives", position = self.size / 1.05, parent = self, color = 'yellow')
		self.time_Node = LabelNode(f"{int(self.time)} seconds", position = (50, self.size[1] / 1.05), parent = self, color = "black")
		
		
				
		self.simulate()		
		self.drops_in_screen()
		
		if not alive(self.player_lives, self.view):
				self.view.close()
				print('You lost !')
				print(f'You stayed alive {self.time} seconds')
				
		
		if  0 < math.fabs(self.time - 15.0) % 15 < 0.02:
			self.add_live()
			
			
	def touch_began(self, touch):
		(x, y) = touch.location
		move = A.move_to(x, y, 0.1)
		self.player.run_action(move)
		
	def load_view(self):
		ui.load_view('UI').present('sheet')
		
		
	def remove_all_Label(self):
		self.player_lives_Node.remove_from_parent()
		self.time_Node.remove_from_parent()
	
	def add_live(self):
		self.live = SpriteNode('emj:Heart', position = random_pos(self.size), parent = self)
			
		
	def touch_moved(self, touch):
		self.touch_began(touch)
	
	def add_all_child(self):
		self.add_child(self.player)
		for drop in self.drops:
			self.add_child(drop)


	def simulate(self):
		if self.time > 5:
			move = A.move_by(0, -300)
		else:
			move = A.move_by(0, 0)
	
			 
		for drop in self.drops:
			drop.run_action(move)
			if self.player.frame.intersects(drop.frame):
				self.player_lives -= 1
				
				drop.remove_from_parent()
				del self.drops[self.drops.index(drop)]
				self.drops.append(SpriteNode('emj:Bomb', (random.randrange(20, self.size[0]), random.randrange(self.size[1], 2 * self.size[1])), scale = scl, parent = self))
		
		try:
			self.live.run_action(move)		
			if self.player.frame.intersects(self.live.frame):
				self.player_lives += 1
				self.live.remove_from_parent()
				del self.live
		except:
			pass
							
if __name__ == '__main__':
	run(MyScene(), show_fps=False)
