import numpy as np
import image_op
"""
    knn to delete background
    idea from http://xueshu.baidu.com/s?wd=paperuri%3A%28b76c95ac5c98e1a7f76241e1875e0848%29&filter=sc_long_sign&tn=SE_xueshusource_2kduw22v&sc_vurl=http%3A%2F%2Fwww.cnki.com.cn%2FArticle%2FCJFDTotal-DZJI200805037.htm&ie=utf-8&sc_us=7560643762415027799
    基于聚类算法的彩色照片背景去除技术
"""
def background_del(image_x):
    image_x = image_x[0]
    H, W, D = image_x.shape
    # 4 kernals
    kn = 8
    kernals = np.random.randint(256,size=(kn, D))
    cluster = np.zeros((H, W))
    dist = np.zeros((H, W, kn))
    # cal distance and assign class[H][W]
    # todo: normalize x_image to avoid overflow of dist
    # todo: add dist to upper left and upper right to dist
    # now dist is not the real dist, but it doesn't matter
    while True:
        for k in xrange(kn):
            dist[:,:,k] =((image_x - kernals[k])**2).sum(axis=-1)
        cluster = dist.argmin(axis=2)
        # average
        prev_kernals = kernals.copy()
        for k in xrange(kn):
            if (cluster == k).sum() != 0:
                kernals[k] = image_x[cluster == k].sum(axis=0)
                kernals[k] /= (cluster == k).sum()
        print 'kernals = ', kernals
        # new kernals change label
        if (prev_kernals == kernals).all():
            break
    # converge and the kernal neartest to image_x[H/10][W/10](as background)
    background_color = image_x[H/10][W/10] # doubt
    dist_bg = range(kn)
    dist_bg = ((kernals - background_color) ** 2).sum(axis=-1)
    background_k = dist_bg.argmin()

    # image_x += 255 * (class == backkernal)(as white)
    changx = image_x.copy()
    changx[cluster == background_k] = 255
    # clip(image_x,0,255)
    changx = np.clip(changx, 0, 255)
    return changx














