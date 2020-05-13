# import cv2
from PIL import Image
def responsive(img_src, numX, numY, saveIn):
    numX, numY = int(numX), int(numY)
    img = Image.open(img_src)
    # img = cv2.imread(img_src)
    # print('The image is.........', img)
    size = img.size
    # size = img.shape
    # print('seze is.......', size)
    rangeX, rangeY = int(size[0]/numX), int(size[1]/numY)
    setX, setY = 0, 0
    for x in range(numX):
        for y in range(numY):
            fileName = (img_src.split('/')[-1]).split('.')[0]+'-Aidesign-'+str(x)+str(y)+'.'+img_src.split('.')[-1]
            # fileName = 'Aidesign-Splitter-'+str(x)+str(y)+'.'+img_src.split('.')[-1]
            # print('Manual Debugging (File name)= ', fileName)
            croppedImage = img.crop((setX, setY, setX + rangeX, setY + rangeY))
            # croppedImage = img[setY:setY+rangeY, setX:setX+rangeX]
            # cv2.imshow(fileName,croppedImage)
            # cv2.waitKey(0)
            # print((saveIn+fileName))
            croppedImage.save(saveIn+fileName)
            # cv2.imwrite((saveIn+fileName), croppedImage)
            setY += rangeY

        setY = 0
        setX += rangeX

# responsive("203 Infografis Hari Buruh.png",6,1)
