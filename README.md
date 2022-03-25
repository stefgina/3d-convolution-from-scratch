# 3D Convolution 
```python

Author -> Stefanos Ginargyros

```
## 1. Environment Setupp
  
For the proper execution of the scripts there is an .yml anaconda environment with all the necessary dependencies
needed. All you have to do is to create a conda environment in your machine pointing in my .yml file. If you don't know how to do that
read [here](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html).



## 2. Theory Behind Convolution 
  
3D Convolution is a type of convolution where the kernel slides in 3 dimensions as opposed to 2 dimensions with 2D
convolutions. You can think of a video as a 3D Array where X Axis depicts the pixel rows, Y Axis depicts the pixel
columns and Z Axis depicts the time or in other words the total amount of the frames.

At the following illustration the light blue 3D Array depicts our video, the orange is our Kernel and the Green is the final convoluted video output.
As you can see the output of a single convolution is a single element in the (green) final convoluted video.

<img src="https://github.com/stefgina/3d-convolution-from-scratch/blob/main/convo.png" width="400" height="300">

## 3. Convolution Implementation

The essence of the 3D convolution are these 6 lines of python code bellow.  You have to
create a "window" (light red) in the video array (light blue) equal sized with your Kernel, flip your kernel and then perform elementwise multiplication and summation
of the results (the red little box). You have to note that if you don't flip your Kernel it is not Convolution but Correlation. Here the flipping happens before these lines of
code.
```python
for z in range(size_Az):
            print("## Processing frame", z, " ##")
            for y in range(size_Ay):
                for x in range(size_Ax):

                    # element-wise multiplication using (*), of the kernel and a kernel-sized window
                    output[z, y, x]=(kernel * A_padded[z: z+window_z, y: y+window_y, x: x+window_x]).sum()


```

## 4. Dimensionality

There are many convolutional variants out there, however in Computer Vision 'same' convolution is mostly used. In 'same' the output has the same dimensionality as the 
input. When we use convolutions as video filters, smoothing, noising etc., we need the dimensionality of the initial video to stay as is, so 'same' comes
handy. However I have included code for 'valid' types of convolutions too, you can parse it as an argument inside the convolution function.

In order to acomplish 'same' we use padding at the edges of the initial video (light blue) before any convolution, using the following formula:

```python
output size = input size - kernel size + 2∗padding
```



## 5. Convolution Results

A convolution between the video included in the repository (video.mp4) and a 3x3x3 Kernel with all values 1/3, shown at the figures bellow. Of course these two
are just screenshots, the input and the output are pure videos. For the Data I/O you can use opencv functions just as I did.
As a result the convoluted output was a 'smoothened' version of the initial video. I isolated the RGB channels in order to keep it simple and clean, but 
you can easily do the same thing in all 3 channels and encode it using opencv. Results shown bellow.

<img src="https://github.com/stefgina/3d-convolution-from-scratch/blob/main/in.png" width="400" height="300"> <img src="https://github.com/stefgina/3d-convolution-from-scratch/blob/main/out.png" width="400" height="300">
