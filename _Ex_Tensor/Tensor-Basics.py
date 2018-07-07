import tensorflow as tf

print(tf.__version__)

a: object = tf.get_variable("a", initializer=tf.random_uniform([3,3], minval=1, maxval=10, dtype=tf.int32))

print(a)

b = tf.ones(shape=[3,3], dtype=tf.int32)

print(b)

sess = tf.Session()

sess.run(tf.global_variables_initializer())

print("\nA:\n", sess.run(a))
print("\nB:\n", sess.run(b))

ab = tf.matmul(a,b)

print("\nA*B:\n", sess.run(ab))

