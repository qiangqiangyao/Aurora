cimport cython

import numpy as np
cimport numpy as np

@cython.boundscheck(False)
@cython.wraparound(False)
def max_pool_forward(np.float64_t[:, :, :, :] data, int filter_height, int filter_width, int stride_height, int stride_width):

    # Retrieve dimensions from the input shape
    #(m, n_H_prev, n_W_prev, n_C_prev) = A_prev.shape
    cdef int batch_size = data.shape[0]
    cdef int n_colr = data.shape[1]
    cdef int height = data.shape[2]
    cdef int width = data.shape[3]

    # Retrieve hyperparameters from "hparameters"
    #f = hparameters["f"]
    #stride = hparameters["stride"]

    # Define the dimensions of the output
    cdef int n_H = int(1 + (height - filter_height) / stride_height)
    cdef int n_W = int(1 + (width - filter_width) / stride_width)
    cdef int n_C = n_colr
    #print('n_H: {}'.format(n_H))
    #print('n_W: {}'.format(n_W))

    # Initialize output matrix A
    cdef np.float64_t[:, :, :, :] A = np.zeros((batch_size, n_C, n_H, n_W))

    ### START CODE HERE ###
    cdef int i, c, h, w
    cdef int vert_start, vert_end, horiz_start, horiz_end

    cdef float max_val = 1e-99
    cdef int ii, jj

    for i in range(batch_size):                         # loop over the training examples
        for c in range (n_C):            # loop over the channels of the output volume
            for h in range(n_H):                     # loop on the vertical axis of the output volume
                for w in range(n_W):                 # loop on the horizontal axis of the output volume

                    # Find the corners of the current "slice" (≈4 lines)
                    vert_start = h*stride_height
                    vert_end = h*stride_height + filter_height
                    horiz_start = w*stride_width
                    horiz_end = w*stride_width + filter_width

                    #assert vert_end <= data.shape[2]
                    #assert horiz_end <= data.shape[3]

                    # Use the corners to define the current slice on the ith training example of A_prev, channel c. (≈1 line)
                    max_val = 1e-99
                    for ii in range(vert_start, vert_end):
                        for jj in range(horiz_start, horiz_end):
                            if data[i, c, ii, jj] > max_val:
                                max_val = data[i, c, ii, jj]


                    # Compute the pooling operation on the slice. Use an if statment to differentiate the modes. Use np.max/np.mean.
                    A[i, c, h, w] = max_val

    return A

@cython.boundscheck(False)
@cython.wraparound(False)
cdef max_val(np.float64_t[:, :] arr):
    cdef float current_max = arr[0, 0]
    cdef int i, j
    cdef float current
    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            current = arr[i, j]
            if current > current_max:
                current_max = current
    return current_max

@cython.boundscheck(False)
@cython.wraparound(False)
cdef innter_xxx(np.float64_t[:, :, :, :] output_grad, np.float64_t[:, :, :, :] input_data,
              int batch_size, int channels, int height, int width,
              int filter_height, int filter_width, int stride_height, int stride_width):

    dA_prev = np.zeros_like(input_data)

    cdef np.float64_t[:, :, :]  a_prev
    cdef int h, w, c, vert_start, vert_end, horiz_start, horiz_end
    for i in range(batch_size):                       # loop over the training examples

        # select training example from A_prev (≈1 line)
        a_prev = input_data[i, :, :, :]


        for h in range(height):                   # loop on the vertical axis
            for w in range(width):               # loop on the horizontal axis
                for c in range(channels):           # loop over the channels (depth)

                    # Find the corners of the current "slice" (≈4 lines)
                    vert_start = h*stride_height
                    vert_end = h*stride_height + filter_height
                    horiz_start = w*stride_width
                    horiz_end = w*stride_width + filter_width

                    # Compute the backward propagation in both modes.

                    # Use the corners and "c" to define the current slice from a_prev (≈1 line)
                    a_prev_slice = a_prev[c, vert_start:vert_end, horiz_start:horiz_end]
                    # Create the mask from a_prev_slice (≈1 line)
                    mask = (a_prev_slice == max_val(a_prev_slice)) #create_mask_from_window(a_prev_slice)
                    dA_prev[i, c, vert_start: vert_end, horiz_start: horiz_end] += mask * output_grad[i, c, h, w]

    return dA_prev


@cython.boundscheck(False)
@cython.wraparound(False)
cdef innter_improved(np.float64_t[:, :, :, :] output_grad, np.float64_t[:, :, :, :] input_data,
              int batch_size, int channels, int height, int width,
              int filter_height, int filter_width, int stride_height, int stride_width):

    dA_prev = np.zeros_like(input_data)

    cdef np.float64_t[:, :, :]  a_prev
    cdef int h, w, c, vert_start, vert_end, horiz_start, horiz_end

    cdef int inner_i, inner_j
    cdef int max_i, max_j
    cdef float max_value
    cdef float cct

    for i in range(batch_size):                       # loop over the training examples

        # select training example from A_prev (≈1 line)
        a_prev = input_data[i, :, :, :]

        for h in range(height):                   # loop on the vertical axis
            for w in range(width):               # loop on the horizontal axis
                for c in range(channels):           # loop over the channels (depth)

                    # Find the corners of the current "slice" (≈4 lines)
                    vert_start = h*stride_height
                    vert_end = h*stride_height + filter_height
                    horiz_start = w*stride_width
                    horiz_end = w*stride_width + filter_width

                    # Compute the backward propagation in both modes.
                    max_value = -1.0e-10
                    for inner_i in range(vert_start, vert_end):
                        for inner_j in range(horiz_start, horiz_end):
                            cct = a_prev[c, inner_i, inner_j]
                            #print('cct: {}, max: {}'.format(cct, max_value))
                            if cct > max_value:
                                max_value = cct
                                max_i = inner_i
                                max_j = inner_j
                                #print(max_i, max_j)
                                #print()

                    dA_prev[i, c, max_i, max_j] = dA_prev[i, c, max_i, max_j] + output_grad[i, c, h, w]
    return dA_prev

@cython.boundscheck(False)
@cython.wraparound(False)
def max_pool_backward(np.float64_t[:, :, :, :] output_grad, np.float64_t[:, :, :, :] input_data,
                  int filter_height=2, int filter_width=2, int stride_height=2,
                  int stride_width=2):

    batch_size = output_grad.shape[0]
    channels = output_grad.shape[1]
    height = output_grad.shape[2]
    width = output_grad.shape[3]

    # Initialize dA_prev with zeros (≈1 line)


    # Making sure your output shape is correct
    #assert(dA_prev.shape == input_data.shape)
    return innter_improved(output_grad, input_data, batch_size, channels,height, width,
                      filter_height, filter_width, stride_height, stride_width)
