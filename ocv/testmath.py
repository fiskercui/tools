#encoding:utf-8

#Bresenham's Line Algorithm is a way of drawing a line segment onto a square grid. It is especially useful for roguelikes due to their cellular nature. A detailed explanation of the algorithm can be found here.
#In libtcod it is accessible using line(x1, y1, x2, y2, callback). Below are several hand-coded implementations in various languages.


#Bresenham line
def get_line(start, end):
    """Bresenham's Line Algorithm
    Produces a list of tuples from start and end
 
    >>> points1 = get_line((0, 0), (3, 4))
    >>> points2 = get_line((3, 4), (0, 0))
    >>> assert(set(points1) == set(points2))
    >>> print points1
    [(0, 0), (1, 1), (1, 2), (2, 3), (3, 4)]
    >>> print points2
    [(3, 4), (2, 3), (1, 2), (1, 1), (0, 0)]
    """
    # Setup initial conditions
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1
 
    # Determine how steep the line is
    is_steep = abs(dy) > abs(dx)
 
    # Rotate line
    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
 
    # Swap start and end points if necessary and store swap state
    swapped = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True

    print ("swapped", swapped)
 
    # Recalculate differentials
    dx = x2 - x1
    dy = y2 - y1
 
    # Calculate error
    error = int(dx / 2.0)
    ystep = 1 if y1 < y2 else -1
 
    # Iterate over bounding box generating points between start and end
    y = y1
    points = []
    for x in range(x1, x2 + 1):
        coord = (y, x) if is_steep else (x, y)
        points.append(coord)
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx
 
    # Reverse the list if the coordinates were swapped
    if swapped:
        points.reverse()
    return points

#dda line 
#　　1、已知直线的两端点坐标：(x1，y1)，(x2，y2)
# 　　2、已知画线的颜色：color
# 　　3、计算两个方向的变化量：dx=x2－x1
# 　　　　　　　　　　　　　　 dy=y2－y1
# 　　4、求出两个方向最大变化量的绝对值：
# 　　　　　　　　　　　　　　 steps=max(|dx|，|dy|)
# 　　5、计算两个方向的增量(考虑了生成方向)：
# 　　　　　　　　　　　　　　 xin=dx/steps
# 　　　　　　　　　　　　　　 yin=dy/steps
# 　　6、设置初始象素坐标：x=x1,y=y1
# 　　7、用循环实现直线的绘制：
# 　　　　for(i=1；i<=steps；i++) 
# 　　　　{ 

#                   putpixel(x，y，color)；/*在(x，y)处，以color色画点*/
# 　　　　　x=x+xin； 
# 　　　　　y=y+yin；
# 　　　　}






#middle line alogi
#中点画线算法其实是基于判断点在直线的上方还是下方
#中点画线算法的原则是：如下图所示，但斜率K<1时，选定一个点之后，再计算中点M。如果M>0,这线更靠近E点，下一点选择为E点。反之选择NE点。

if __name__=="__main__":
	print (get_line((1,0),(10,4)))

