#encoding:utf-8

from numpy import *;
import numpy as np 
from scipy.optimize import leastsq
import numpy as np
import cv2
from matplotlib import pyplot as plt

def testMat():

	a1=array([1,2,3]);
	a1=mat(a1);
	print a1
	print a1.T

	data1=mat(zeros((3,3)))
	print data1
	print data1.T

	print "test array1"
	x = array([1, 2, 3])
	print x
	print x.ndim


	print "test array2"
	a=array([[2,3],[3,4]]) 
	print a

	print "test zeros1"
	y = zeros([2, 3, 3])
	print y 
	print y.ndim

	print "test zeros2"
	y = zeros((1, 2, 3))
	print y
	print y.ndim

def testHistogram():
	import numpy
	import pylab
	# Build a vector of 10000 normal deviates with variance 0.5^2 and mean 2
	mu, sigma = 2, 0.5
	v = numpy.random.normal(mu,sigma,10000)
	# Plot a normalized histogram with 50 bins
	pylab.hist(v, bins=50, normed=1)       # matplotlib version (plot)
	pylab.show()
	# Compute the histogram with numpy and then plot it
	(n, bins) = numpy.histogram(v, bins=50, normed=True)  # NumPy version (no plot)
	pylab.plot(.5*(bins[1:]+bins[:-1]), n)
	pylab.show() 

def testLeastsq():
	def func(x, p):
	  print u""" 数据拟合所用的函数: A*sin(2*pi*k*x + theta) """
	  A, k, theta = p
	  return A*np.sin(2*np.pi*k*x+theta)
	def residuals(p, y, x): 
		print u""" 实验数据x, y和拟合函数之间的差，p为拟合需要找到的系数 """ 
		# print len(x)
		# print x, y, p
		return y - func(x, p) 
	x = np.linspace(0, -2*np.pi, 100)
	print x
	A, k, theta = 10, 0.34, np.pi/6 # 真实数据的函数参数 
	y0 = func(x, [A, k, theta]) # 真实数据 
	y1 = y0 + 2 * np.random.randn(len(x)) # 加入噪声之后的实验数据 
	p0 = [7, 0.2, 0] # 第一次猜测的函数拟合参数

	# 调用leastsq进行数据拟合 
	# residuals为计算误差的函数 
	# p0为拟合参数的初始值 
	# args为需要拟合的实验数据 
	plsq = leastsq(residuals, p0, args=(y1, x)) 
	print u"真实参数:", [A, k, theta] 
	print u"拟合参数", plsq[0] # 实验数据拟合后的参数 
	# pl.plot(x, y0, label=u"真实数据") 
	# pl.plot(x, y1, label=u"带噪声的实验数据") 
	# pl.plot(x, func(x, plsq[0]), label=u"拟合数据") 

	pl.plot(x, y0, label="real satistics") 
	pl.plot(x, y1, label="real voice satistics") 
	pl.plot(x, func(x, plsq[0]), label="nihe shuju")

	pl.legend() 
	pl.show()

def testLine():
	canvas = np.zeros((1024,768,3),dtype="uint8")
	#画绿线
	green = (0,255,0)
	cv2.line(canvas,(0,0),(300,300),green,2)
	cv2.imshow("Canvas",canvas)
	cv2.waitKey(0)

def testTransfrom():
	#scaling:
	img = cv2.imread('./texture/texure.png')
	# cv2.imshow("Image", img) 
	
	rows, cols, channels = img.shape
	print rows, cols, channels

	res = cv2.resize(img, (cols/2, rows/2))
	#Translation:
	# 1.shift
	M_shift = np.float32([[1,0,100],[0,1,50]])
	img_shift = cv2.warpAffine(img, M_shift, (cols, rows))

	# 2.rotate
	M_rotate = cv2.getRotationMatrix2D((cols/2, rows/2), 90, 1)
	img_rotate = cv2.warpAffine(img, M_rotate, (cols, rows))

	# 3.affine
	pts1 = np.float32([[50,50],[200,50],[50,200]])
	pts2 = np.float32([[10,100],[200,50],[100,250]])
	M_affine = cv2.getAffineTransform(pts1,pts2)
	img_affine = cv2.warpAffine(img, M_affine, (cols, rows))

	# 4.perspective
	pts3 = np.float32([[56,65],[368,52],[28,387],[389,390]])
	pts4 = np.float32([[0,0],[300,0],[0,300],[300,300]])
	M_perspective = cv2.getPerspectiveTransform(pts3,pts4)
	img_perspective = cv2.warpPerspective(img, M_perspective, (cols, rows))

	print 'shift:\n', M_shift
	print 'rotate:\n', M_rotate
	print 'affine:\n', M_affine
	print 'perspective:\n', M_perspective

	plt.subplot(231),plt.imshow(img),plt.title('src')
	# plt.subplot(232),plt.imshow(res),plt.title('scale')
	# plt.subplot(233),plt.imshow(img_shift),plt.title('shift')
	# plt.subplot(234),plt.imshow(img_rotate),plt.title('rotate')
	# plt.subplot(235),plt.imshow(img_affine),plt.title('affine')
	# plt.subplot(236),plt.imshow(img_perspective),plt.title('perspective')

	plt.show()

if __name__=="__main__":

	# testMat()
	# testHistogram()
	# testLeastsq()
	# testLine()
	testTransfrom()