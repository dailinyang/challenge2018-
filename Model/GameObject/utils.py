from copy import copy


# class Vec(object):
# 	def __init__(self,*args, **kwargs):
# 		if len(args)==2:
# 			self.x=args[0]
# 			self.y=args[1]
# 		else:
# 			self.x=args[0].x
# 			self.y=args[0].y	
# 	def __str__(self):
# 		return "("+str(self.x)+','+str(self.y)+")"
# 	def __add__(self,that):
# 		return Vec(self.x+that.x,self.y+that.y)
# 	def __sub__(self,that):
# 		return Vec(self.x-that.x,self.y-that.y)
# 	def __mul__(self,that):
# 		return Vec(self.x*that,self.y*that)
# 	def __truediv__(self,that):
# 		return Vec(self.x/that,self.y/that)
# 	def mag(self):
# 		return (self.x**2+self.y**2)**(1/2)
# 	def mag2(self):
# 		return (self.x**2+self.y**2)
# 	def norm(self):
# 		return self/self.mag()


