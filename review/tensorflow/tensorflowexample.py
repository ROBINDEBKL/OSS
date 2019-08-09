import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

num_examples = 50
X = np.array([np.linspace(-2, 4, num_examples), \
  np.linspace(6, -18, num_examples)])
X += np.random.randn(2, num_examples)
x, y = X
bias_with_x = np.array([(1.0, a) for a in x]).astype(np.float32)

# Keep track of losses to plot later
losses = []
# How many iteration of training
training_steps = 50
# Learning rate (step size to control gradient descent). Too large
# and you may jump past minima, too small and it takes forever.
learning_rate = 0.002


with tf.Session() as sess:
  # Set up all the tensors. The input layer is x and bias
  input = tf.constant(bias_with_x)
  print("!!!!!!!!!!!!!!!!!!!!!\n\n\n")
  print(input.get_shape())
  print("!!!!!!!!!!!!!!!!!!!!!\n\n\n")
  # Our output are the y values as a column vector
  target = tf.constant(np.transpose([y]).astype(np.float32))
  # Weights are what we are changing. Initialize them to random
  # values (gaussian, mean 0, stddev 0.1)
  weights = tf.Variable(tf.random_normal([2, 1], 0, 0.1))
  # Now initialize the variables
  tf.global_variables_initializer().run()


# with tf.Session() as sess:
  #
  # Set up the operations that will run in the loop
  # For all x values, generate an estimate for y given our current
  # weights. I.e. y^ = w2 * x + w1 * bias
  yhat = tf.matmul(input, weights)
  # The error is our estimate minus the measured
  yerror = tf.subtract(yhat, target)
  # Use the L2 magnitude over all estimates as the error function
  loss = tf.nn.l2_loss(yerror)
  # Now do gradient descent to optimize the weights.
  update_weights = tf.train.GradientDescentOptimizer(learning_rate).\
  minimize(loss)

# with tf.Session() as sess:
  #
  # We have defined all the tensors, run the initialization and
  # set up the execution graph to run the training data. Now repeatedly
  # call the training operation to execute gradient descent and
  # optimize the weights.
  for _ in range(training_steps):
      # Run an iteration of gradient descent
      sess.run(update_weights)
      # Save our loss magnitude so we can plot it later.
      losses.append(loss.eval())
  # When we are done training, get the final values for the charts.
  betas = weights.eval()
  yhat = yhat.eval()

# Show the results
fig, (ax1, ax2) = plt.subplots(1,2)
plt.subplots_adjust(wspace=0.3)
fig.set_size_inches(10, 4)
ax1.scatter(x, y, alpha=0.7)
ax1.scatter(x, np.transpose(yhat)[0], c="g", alpha=0.6)
line_x_range = (-4, 6)
ax1.plot(line_x_range, [betas[0] + a * betas[1] \
  for a in line_x_range], "g", alpha=0.6)
ax2.plot(range(0, training_steps), losses)
ax2.set_ylabel("Loss")
ax2.set_xlabel("Training steps")
plt.show()
