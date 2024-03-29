import cv2
import numpy as np

def my_get_Gaussian2D_mask(msize, sigma=1):
    #########################################
    # ToDo
    # 2D gaussian filter 만들기
    #########################################
    height, weight = msize
    y, x = np.mgrid[-(weight // 2):(weight // 2) + 1, -(height // 2):(height // 2) + 1]
    y, x
    '''
    y, x = np.mgrid[-1:2, -1:2]
    y = [[-1,-1,-1], // 열방향 중복
         [ 0, 0, 0],
         [ 1, 1, 1]]
    x = [[-1, 0, 1], // 행방향 중복
         [-1, 0, 1],
         [-1, 0, 1]]
    '''
    # 파이 => np.pi 를 쓰시면 됩니다.
    # 2차 gaussian mask 생성

    '''
    오류 : GAUSSIAN 식 썼을때, 시그마 값 높으면 값이 흐려짐 !
    해결 : 괄호 잘 해주기(식 잘 써주기)
    '''
    gaus2D = 1 / (2 * np.pi * sigma ** 2) * np.exp(-((x ** 2 + y ** 2) / (2 * sigma ** 2)))

    # mask의 총 합 = 1
    gaus2D /= np.sum(gaus2D)

    return gaus2D

def my_get_Gaussian1D_mask(msize, sigma=1):
    #########################################
    # ToDo
    # 1D gaussian filter 만들기
    #########################################
    x = np.full((1, msize), [range(-(msize // 2), (msize // 2) + 1)])
    '''
    x = np.full((1, 3), [-1, 0, 1])
    x = [[ -1, 0, 1]]

    x = np.array([[-1, 0, 1]])
    x = [[ -1, 0, 1]]
    '''

    # 파이 => np.pi 를 쓰시면 됩니다.

    '''
    ! 오류 및 해결 !
    단순한 괄호 여닫기 문제 였음. 특히 np.exp부분 괄호 잘 볼 것
    '''
    gaus1D = 1 / (((2 * np.pi) ** 1/2) * sigma) * np.exp(-(x ** 2) / (2 * sigma ** 2))

    # mask의 총 합 = 1
    gaus1D /= np.sum(gaus1D)
    return gaus1D

def my_mask(ftype, fshape, sigma=1):
    if ftype == 'average':
        print('average filtering')
        ###################################################
        # TODO                                            #
        # mask 완성                                       #
        ###################################################
        mask = np.ones(fshape)
        mask = mask / (fshape[0] * fshape[1])

        #mask 확인
        print(mask)

    elif ftype == 'sharpening':
        print('sharpening filtering')
        ##################################################
        # TODO                                           #
        # mask 완성                                      #
        ##################################################

        base_mask = np.zeros(fshape)
        base_mask[fshape[0] // 2, fshape[1] // 2] = 2
        aver_mask = np.ones(fshape)
        aver_mask = aver_mask / (fshape[0] * fshape[1])
        mask = base_mask - aver_mask

        #mask 확인
        print(mask)

    elif ftype == 'gaussian2D':
        print('gaussian filtering')
        ##################################################
        # TODO                                           #
        # mask 완성                                      #
        ##################################################
        mask = my_get_Gaussian2D_mask(fshape, sigma=sigma)
        #mask 확인
        print(mask)

    elif ftype == 'gaussian1D':
        print('gaussian filtering')
        ##################################################
        # TODO                                           #
        # mask 완성                                      #
        ##################################################
        mask = my_get_Gaussian1D_mask(fshape, sigma=sigma)
        #mask 확인
        print(mask)

    return mask

def my_zero_padding(src, pad_shape):
    (h, w) = src.shape
    (p_h, p_w) = pad_shape
    pad_img = np.zeros((h+2*p_h, w+2*p_w))
    pad_img[p_h:p_h+h, p_w:p_w+w] = src
    return pad_img

def my_filtering(src, mask):
    #########################################################
    # TODO                                                  #
    # dst 완성                                              #
    # dst : filtering 결과 image                            #
    #########################################################
    h, w = src.shape
    m_h, m_w = mask.shape
    pad_img = my_zero_padding(src, (m_h // 2, m_w // 2))
    dst = np.zeros((h, w))
    
    """
    반복문을 이용하여 filtering을 완성하기
    """
    for row in range(h):
        for col in range(w):
            val = np.sum(pad_img[row:row + m_h, col:col + m_w] * mask)
            val = np.clip(val, 0, 255) #범위를 0~255로 조정
            dst[row, col] = val

    dst = (dst+0.5).astype(np.uint8) #uint8의 형태로 조정

    return dst

if __name__ == '__main__':

    '''
    ! 오류 ! 및 해결
    
    처음 파일 경로 한글이라 cv2.imread가 에러를 내보냄
    파일 경로 영어로 수정했음에도 똑같은 오류 발생
    따로 'Lena.png'선언 후 사용함
    '''
    fname = 'Lena.png'
    src = cv2.imread(fname, cv2.IMREAD_GRAYSCALE)

    # 3x3 filter
    average_mask = my_mask('average', (5, 5))
    sharpening_mask = my_mask('sharpening', (5, 5))

    #원하는 크기로 설정
    #dst_average = my_filtering(src, 'average', (5,5))
    #dst_sharpening = my_filtering(src, 'sharpening', (5,5))

    # 11x13 filter
    #dst_average = my_filtering(src, 'average', (5,3), 'repetition')
    #dst_sharpening = my_filtering(src, 'sharpening', (5,3), 'repetition')
    #dst_average = my_filtering(src, 'average', (11,13))
    #dst_sharpening = my_filtering(src, 'sharpening', (11,13))


    dst_average = my_filtering(src, average_mask)
    dst_sharpening = my_filtering(src, sharpening_mask)

    # Gaussian filter
    gaussian2d_mask = my_mask('gaussian2D', (7, 7), sigma=0.1)
    gaussian1d_mask = my_mask('gaussian1D', 7, sigma=0.1)

    dst_gaussian2d = my_filtering(src, gaussian2d_mask)

    dst_gaussian1d = my_filtering(src, gaussian1d_mask.T)
    dst_gaussian1d = my_filtering(dst_gaussian1d, gaussian1d_mask)


    cv2.imshow('original', src)
    cv2.imshow('average filter', dst_average)
    cv2.imshow('sharpening filter', dst_sharpening)
    cv2.imshow('gaussian2D filter', dst_gaussian2d)
    cv2.imshow('gaussian1D filter', dst_gaussian1d)
    cv2.waitKey()
    cv2.destroyAllWindows()
