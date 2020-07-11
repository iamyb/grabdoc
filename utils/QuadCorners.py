import cv2
import numpy as np

## https://stackoverflow.com/questions/41138000/fit-quadrilateral-tetragon-to-a-blob
def _get_approx_corners(img):
    img=img.copy()
    #gray = cv2.cvtColor(img.copy(),cv2.COLOR_BGR2GRAY)
    gray = img
    
    contours, hierarchy = cv2.findContours(gray.astype(np.uint8),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    contours.sort(key=lambda x: len(x),reverse=True)
    
    epsilon = 0.05*cv2.arcLength(contours[0],True)
    approx = cv2.approxPolyDP(contours[0],epsilon,True)
    #plt.imshow(cv2.drawContours(img, [approx], 0, (0,255,255), 3))
    #plt.show()
    
    return approx,contours

def _perp(a) :
    b = np.empty_like(a)
    b[0] = -a[1]
    b[1] = a[0]
    return b

def _seg_intersect(a1,a2, b1,b2) :
    da = a2-a1
    db = b2-b1
    dp = a1-b1
    dap = _perp(da)
    denom = np.dot( dap, db)
    num = np.dot( dap, dp )
    return (num / denom.astype(float))*db + b1

def get_corners(img):
    #img = results[6][2].copy()
    corners, contours = _get_approx_corners(img)

    l_corners = list(corners)
    l_corners.sort(key=lambda x: np.sum(x))
    #print(l_corners[0])
    if len(corners) < 4:
        return np.array([5,5]),np.array([5,img.shape[1]-5]),np.array([img.shape[0]-5,5]),np.array([img.shape[0]-5,img.shape[1]-5])

    c0 = l_corners[0][0]
    c1 = l_corners[1][0]
    c2 = l_corners[2][0]
    c3 = l_corners[3][0]

    #print(corners[0])
    edges = [(c1,c0),(c2,c0),(c1,c3),(c2,c3)]
    edpts = []

    for e0,e1 in edges:
        pts=[]
        for p in contours[0]:
            p = p[0]
            d = np.cross(e1-e0, p-e0) / np.linalg.norm(e1-e0)
            if abs(d) < 5:
                pts.append(p)

        [vx,vy,x,y] = cv2.fitLine(np.array(pts),cv2.DIST_L2,0,0.01,0.01)

        # Now find two extreme points on the line to draw line
        lefty = int((-x*vy/vx) + y)
        righty = int(((img.shape[1]-x)*vy/vx)+y)

        #print(vx,vy,x,y)
        #_ = cv2.line(img,(gray.shape[1]-1,righty),(0,lefty),255,1)
        edpts.append((np.array([img.shape[1]-1,righty]),np.array([0,lefty])))

    final_c0 = _seg_intersect(edpts[0][0],edpts[0][1],edpts[1][0],edpts[1][1])
    final_c1 = _seg_intersect(edpts[0][0],edpts[0][1],edpts[2][0],edpts[2][1])
    final_c2 = _seg_intersect(edpts[3][0],edpts[3][1],edpts[2][0],edpts[2][1])
    final_c3 = _seg_intersect(edpts[3][0],edpts[3][1],edpts[1][0],edpts[1][1])
    
    return final_c0,final_c1,final_c2,final_c3
