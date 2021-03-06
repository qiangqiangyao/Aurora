from __future__ import absolute_import

import ctypes
from ._base import _LIB
from . import ndarray as _nd


def array_set(arr, value):
    assert isinstance(arr, _nd.NDArray)
    _LIB.DLGpuArraySet(arr.handle, ctypes.c_float(value))


def broadcast_to(in_arr, out_arr):
    assert isinstance(in_arr, _nd.NDArray)
    assert isinstance(out_arr, _nd.NDArray)
    _LIB.DLGpuBroadcastTo(in_arr.handle, out_arr.handle)


def reduce_sum_axis_zero(in_arr, out_arr):
    assert isinstance(in_arr, _nd.NDArray)
    assert isinstance(out_arr, _nd.NDArray)
    _LIB.DLGpuReduceSumAxisZero(in_arr.handle, out_arr.handle)


def matrix_elementwise_add(matA, matB, matC):
    assert isinstance(matA, _nd.NDArray)
    assert isinstance(matB, _nd.NDArray)
    assert isinstance(matC, _nd.NDArray)
    _LIB.DLGpuMatrixElementwiseAdd(matA.handle, matB.handle, matC.handle)


def matrix_elementwise_add_by_const(in_mat, val, out_mat):
    assert isinstance(in_mat, _nd.NDArray)
    assert isinstance(out_mat, _nd.NDArray)
    _LIB.DLGpuMatrixElementwiseAddByConst(
        in_mat.handle, ctypes.c_float(val), out_mat.handle)


def matrix_elementwise_subtract(matA, matB, matC):
    assert isinstance(matA, _nd.NDArray)
    assert isinstance(matB, _nd.NDArray)
    assert isinstance(matC, _nd.NDArray)
    _LIB.DLGpuMatrixElementwiseSubtract(matA.handle, matB.handle, matC.handle)


def matrix_elementwise_subtract_by_const(in_mat, val, out_mat):
    assert isinstance(in_mat, _nd.NDArray)
    assert isinstance(out_mat, _nd.NDArray)
    _LIB.DLGpuMatrixElementwiseSubtractByConst(
        in_mat.handle, ctypes.c_float(val), out_mat.handle)


def matrix_elementwise_multiply(matA, matB, matC):
    assert isinstance(matA, _nd.NDArray)
    assert isinstance(matB, _nd.NDArray)
    assert isinstance(matC, _nd.NDArray)
    _LIB.DLGpuMatrixElementwiseMultiply(
        matA.handle, matB.handle, matC.handle)


def matrix_elementwise_multiply_by_const(in_mat, val, out_mat):
    assert isinstance(in_mat, _nd.NDArray)
    assert isinstance(out_mat, _nd.NDArray)
    _LIB.DLGpuMatrixMultiplyByConst(
        in_mat.handle, ctypes.c_float(val), out_mat.handle)


def matrix_elementwise_division(matA, matB, matC):
    assert isinstance(matA, _nd.NDArray)
    assert isinstance(matB, _nd.NDArray)
    assert isinstance(matC, _nd.NDArray)
    _LIB.DLGpuMatrixElementwiseDiv(
        matA.handle, matB.handle, matC.handle)


def matrix_elementwise_div_by_const(in_mat, val, out_mat):
    assert isinstance(in_mat, _nd.NDArray)
    assert isinstance(out_mat, _nd.NDArray)
    _LIB.DLGpuMatrixElementwiseDivByConst(
        in_mat.handle, ctypes.c_float(val), out_mat.handle)


def matrix_elementwise_sqrt(in_mat, out_mat):
    assert isinstance(in_mat, _nd.NDArray)
    assert isinstance(out_mat, _nd.NDArray)
    _LIB.DLGpuMatrixElementwiseSqrt(in_mat.handle, out_mat.handle)


def matrix_multiply(matA, transA, matB, transB, matC):
    assert isinstance(matA, _nd.NDArray)
    assert isinstance(matB, _nd.NDArray)
    assert isinstance(matC, _nd.NDArray)
    _LIB.DLGpuMatrixMultiply(
        matA.handle, transA, matB.handle, transB, matC.handle)


def relu(in_arr, out_arr):
    assert isinstance(in_arr, _nd.NDArray)
    assert isinstance(out_arr, _nd.NDArray)
    _LIB.DLGpuRelu(in_arr.handle, out_arr.handle)


def relu_gradient(in_arr, in_grad_arr, out_arr):
    assert isinstance(in_arr, _nd.NDArray)
    assert isinstance(in_grad_arr, _nd.NDArray)
    assert isinstance(out_arr, _nd.NDArray)
    _LIB.DLGpuReluGradient(in_arr.handle, in_grad_arr.handle, out_arr.handle)


def softmax(in_arr, out_arr):
    assert isinstance(in_arr, _nd.NDArray)
    assert isinstance(out_arr, _nd.NDArray)
    _LIB.DLGpuSoftmax(in_arr.handle, out_arr.handle)


def softmax_cross_entropy(in_arr_a, in_arr_b, out_arr):
    assert isinstance(in_arr_a, _nd.NDArray)
    assert isinstance(in_arr_b, _nd.NDArray)
    assert isinstance(out_arr, _nd.NDArray)
    _LIB.DLGpuSoftmaxCrossEntropy(
        in_arr_a.handle, in_arr_b.handle, out_arr.handle)


def cudnn_relu_forward(in_array, out_array):
    assert isinstance(in_array, _nd.NDArray)
    assert isinstance(out_array, _nd.NDArray)
    _LIB.cudnnReLUForward(in_array.handle, out_array.handle)


def cudnn_conv2d_forward(input, filter, bias, stride_height, stride_width, padding_height, padding_width, output):
    assert isinstance(input, _nd.NDArray)
    assert isinstance(filter, _nd.NDArray)
    assert isinstance(bias, _nd.NDArray)
    assert isinstance(stride_height, int)
    assert isinstance(stride_width, int)
    assert isinstance(padding_height, int)
    assert isinstance(padding_width, int)
    assert isinstance(output, _nd.NDArray)
    _LIB.cudnnConv2DForward(input.handle, filter.handle,
                            bias.handle,
                            stride_height, stride_width,
                            padding_height, padding_width,
                            output.handle)


def cudnn_pool_forward(input,
                       pooling_height, pooling_width,
                       stride_height, stride_width,
                       mode,
                       output):
    assert isinstance(input, _nd.NDArray)
    assert isinstance(stride_height, int)
    assert isinstance(stride_width, int)
    assert isinstance(pooling_height, int)
    assert isinstance(pooling_width, int)
    assert isinstance(mode, str)
    assert isinstance(output, _nd.NDArray)

    mode = mode.encode('utf-8')

    _LIB.cudnnPoolForward(input.handle,
                          stride_height, stride_width,
                          pooling_height, pooling_width,
                          ctypes.c_char_p(mode),
                          output.handle)


def cudnn_pool_backward(input,
                        output_grads,
                        output,
                        pooling_height, pooling_width,
                        stride_height, stride_width,
                        mode,
                        pool_grad):
    assert isinstance(input, _nd.NDArray)
    assert isinstance(output_grads, _nd.NDArray)
    assert isinstance(output, _nd.NDArray)
    assert isinstance(pool_grad, _nd.NDArray)

    assert isinstance(pooling_height, int)
    assert isinstance(pooling_width, int)
    assert isinstance(stride_height, int)
    assert isinstance(stride_width, int)

    mode = mode.encode('utf-8')

    _LIB.cudnnPoolBackward(input.handle,
                           output_grads.handle,
                           output.handle,
                           pooling_height, pooling_width,
                           stride_height, stride_width,
                           mode,
                           pool_grad.handle)


def cudnn_conv2d_backward_filter(input,
                                 output_grads,
                                 stride_height,
                                 stride_width,
                                 padding_height,
                                 padding_width,
                                 filter_grad):
    assert isinstance(input, _nd.NDArray)
    assert isinstance(output_grads, _nd.NDArray)
    assert isinstance(stride_height, int)
    assert isinstance(stride_width, int)
    assert isinstance(padding_height, int)
    assert isinstance(padding_width, int)
    assert isinstance(filter_grad, _nd.NDArray)
    _LIB.cudnnConv2DBackwardFilter(input.handle,
                                   output_grads.handle,
                                   stride_height, stride_width,
                                   padding_height, padding_width,
                                   filter_grad.handle)


def cudnn_conv2d_backward_data(filter,
                               output_grad,
                               stride_height,
                               stride_width,
                               padding_height,
                               padding_width,
                               data_grad):
    assert isinstance(filter, _nd.NDArray)
    assert isinstance(output_grad, _nd.NDArray)
    assert isinstance(stride_height, int)
    assert isinstance(stride_width, int)
    assert isinstance(padding_height, int)
    assert isinstance(padding_width, int)
    assert isinstance(data_grad, _nd.NDArray)
    _LIB.cudnnConv2DBackwardData(filter.handle,
                                 output_grad.handle,
                                 stride_height,
                                 stride_width,
                                 padding_height,
                                 padding_width,
                                 data_grad.handle)


def cudnn_conv2d_backward_bias(output_grads, bias_grads):
    assert isinstance(output_grads, _nd.NDArray)
    assert isinstance(bias_grads, _nd.NDArray)
    _LIB.cudnnConv2DBackwardBias(output_grads.handle, bias_grads.handle)
