import numpy as np
from scipy import signal
from scipy import ndimage
import skvideo.io
import cv2
import time


def create_smooth_kernel(size):

    # 3 for loops to make a 3d array of dim sizeXsizeXsize
    lists = [ [ [1/(pow(size,3)) for i in range(0, size)] for x in range(size)]for m in range(size)]
    ker = np.array(lists)
    return ker

def myConv3D(A, kernel, param='same'):

    # get the sizing of the array
    size_Az = A.shape[0]
    size_Ay = A.shape[1]
    size_Ax = A.shape[2]
    
    # if kernel is EVEN, make it ODD and then force odd 'same' convolution. 
    ## The scipy.ndimage.convolve uses the same behaviour for even kernels, got exhactly the same results with them. ###
    if(kernel.shape[0]%2 == 0):
        kernel = pad_even_kernel(kernel)
        param='same'
    
    # get kernel shapes
    window_z = kernel.shape[0]
    window_y = kernel.shape[1]
    window_x = kernel.shape[2]
    
    # flip all dimensions, doesnt really matter when kernel is equally valued. Otherwise if we dont do this, its correlation.
    kernel = kernel[::-1, ::-1, ::-1]
    

    if(param=='same'):
        
        # the array gets padded through the function pad_image! We set output size same as input size.
        output = np.zeros((size_Az,size_Ay,size_Ax))
        
        # padding the array A
        
        A_padded = pad_image(A,kernel.shape[0])
        print("Zero-Padding OK")
        

        # loop over every pixel of the video, Z are the frames.
        for z in range(size_Az):
            print("## Processing frame", z, " ##")
            for y in range(size_Ay):
                for x in range(size_Ax):

                    # element-wise multiplication using (*), of the kernel and a kernel-sized window
                    output[z, y, x]=(kernel * A_padded[z: z+window_z, y: y+window_y, x: x+window_x]).sum()
        
    
    if(param=='valid'):
        
        # the array stay as it is, no padding at all. The formula is, size = [(W-K+2P)/S]+1
        # where w is the input
        # k the kernel
        # p the padding
        # s the stride
        output = np.zeros((size_Az - window_z + 1, size_Ay - window_y + 1, size_Ax - window_x +1))
        
        # loop over every pixel of the image
        for z in range(size_Az - window_z + 1):
            print(z)
            for y in range(size_Ay - window_y + 1):
                for x in range(size_Ax - window_x +1):

                    # element-wise multiplication using (*), of the kernel and a kernel-sized window
                    output[z, y, x]=(kernel * A[z: z+window_z, y: y+window_y, x: x+window_x]).sum()
        
    

    return output

def pad_image(A,size):
    
    # size = [(W-K+2P)/S]+1, we can find the uknown Padding factor since we know all the other elements
    pad = size//2
    A_padded = np.zeros((A.shape[0] + 2*pad, A.shape[1] + 2*pad, A.shape[2] + 2*pad))
    
    # center original image in the zeros to construct the padding.
    A_padded[pad:-pad, pad:-pad, pad:-pad] = A
    
    return A_padded

def pad_even_kernel(kernel):
    
    ## in this function i construct odd kernels from even ones
    ## so when i have even kernels i can proceed with odd 'same' convolutions.
        
    #   ex.  k00 k01 0                   k00 k01
    #        k10 k11 0          =        k10 k11   
    #        0   0   0
    
    kernel_padded = np.zeros((kernel.shape[0]+1, kernel.shape[1]+1, kernel.shape[2]+1))
    kernel_padded[0:-1, 0:-1, 0:-1] = kernel
    
    return kernel_padded

def main():
    
    start_time = time.time()
    print("Setting the timer ... DONE ")
    
    kernel = create_smooth_kernel(3)
    print("Created smooth kernel of size = 3")
    
    video = skvideo.io.vread("video.mp4")
    print("Video loaded into np array ... DONE ... Shape : ", video.shape)
    
    video_gray = np.empty_like(video[...,:1])
    for i in range(video.shape[0]):
        video_gray[i,:,:,0] = cv2.cvtColor(videaki[i], cv2.COLOR_RGB2GRAY)
    print("Video processed to grayscale ... DONE")

    v = video_gray.reshape(150,360,640)
    print("Video reshaped in (150, 360, 640) ... DONE")
    
    print("Preparing Convolution with SAME size output")
    out = myConv3D(v, kernel, param='same')
    print("Convolution is succesfull")
    
    print("Writing video to outputvideo.mp4")
    skvideo.io.vwrite("outputvideo.mp4", out)
    
    print("DONE!")
    
    print(" ### Total program time %s seconds ###" % (time.time() - start_time))

    """
    ### TESTING ###
    A = np.random.rand(4,4,4)
    kernel = create_smooth_kernel(3)
    
    C1 = myConv3D(A,kernel,param='same')
    C2 = ndimage.convolve(A,kernel,mode = 'constant', cval=0.0)
    
    print()
    print("Array A is : ")
    print(A)
    print()
    
    print("Kernel is : ")
    print(kernel)
    print()
    
    print("My 3D 'valid' Convolution between A and Kernel : ")
    print(C1)
    
    print()
    print()
    
    print("Scipy.signal 'valid' convolution between A and Kernel :")
    print(C2)
    """
    
    
if __name__=="__main__":
    main()
