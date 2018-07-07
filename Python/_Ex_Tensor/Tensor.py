# Source
# https://hackernoon.com/introduction-of-tensorflow-with-python-f4a9624f2ab2

import matplotlib.pyplot as plt
import tensorflow as tf
import time

gpu = "/GPU:0"
cpu = "/CPU:0"

def get_times(maximum_time):


    device_times = {}
    device_times[gpu] = []
#    device_times[cpu] = []

    matrix_sizes = range(500, 10000, 50)

    for size in matrix_sizes:
        for device_name in device_times.keys():

            print("####### Calculating on the " + device_name + " #######")

            shape = (size, size)
            data_type = tf.float16
            with tf.device(device_name):
                r1 = tf.random_uniform(shape=shape, minval=0, maxval=1, dtype=data_type)
                r2 = tf.random_uniform(shape=shape, minval=0, maxval=1, dtype=data_type)
                dot_operation = tf.matmul(r2, r1)


            with tf.Session(config=tf.ConfigProto(log_device_placement=True)) as session:
                    start_time = time.time()
                    result = session.run(dot_operation)
                    time_taken = time.time() - start_time
                    print(result)
                    device_times[device_name].append(time_taken)

            print(device_times)

            if time_taken > maximum_time:
                return device_times, matrix_sizes


device_times, matrix_sizes = get_times(10)
gpu_times = device_times[gpu]
cpu_times = device_times[cpu]

plt.plot(matrix_sizes[:len(gpu_times)], gpu_times, 'o-')
plt.plot(matrix_sizes[:len(cpu_times)], cpu_times, 'o-')
plt.ylabel('Time')
plt.xlabel('Matrix size')
plt.show()
