Om Sri Sai Ram

First, I wrote up the load_data function. That was fairly straightforward using cv2 documentation and some stack overflow posts.

Then, I worked on the get_model function. First, I took some of the lecture code from handwriting.py.

Next, testing:
It was super fun!

On gtsrb-small:
Running the initial program, I got an accuracy of 0.05 with sigmoids as activators, and everything else identical to the lecture code.
I then took 2 layers with 128 units each, it gave 0.04, 3 layers, 16 units each gave 0.05 again. I even tried 6 layers. It took an
age, and again gave 0.05.

Then, I tried playing around in playground.tensorflow.org. This gave a lot of insight. Less layers were enough, more layers didn't do
anything much except making it slower. So I went back, took only two hidden layers, and increased the number of neurons. Still 0.05.

Then, the moment of triumph: I turned the sigmoids to relus and dropout to 0.3(neurons fixed at 1200+768 in two hidden layers) and
the accuracy shot up. It went to a 100% on the small set. I tried my code on the big set now.

On gtsrb:
My code gave me 90%, but it took a while: 42 sec/epoch. I then began experimenting with the dropout. 0.4, 0.5 dropout didn't seem to
work, so I stuck with 0.3. I then read a stack overflow post: the number of hidden layers required will hardly exceed 1, most problems
require only 1 hidden layer. I removed my second hidden layer, sure enough, it gave me 92% and took half as long(21s/epoch). The post
also said that a good number of neurons to use in the hidden layer was the avg of the input and output neurons = (675+43)/2 = 359 here.
This gave a 93%. To get a better view of saturation, I selected 20 epochs. Next, I modified the kernels to 4x4 kernels, it gave a
whopping 95%. 5x5 kernels and 3x3 kernels didn't give as much, about 93%. Next, the number of filters. I checked a lot of values,
24 worked very well, giving 95+ often. The time taken to run with this code was 13-14s/epoch. I again tried some values for dropout,
25% gave the best accuracy, giving 96% too. Now, I modified the pooling algorithm. AveragePooling worked better than MaxPooling.

Now, the goal was to get the 95+ within 10 epochs. I again modified the number of neurons. 400 gave me an average(avg of 6th to 10th
epoch accuracies) of 95.63. 444 gave me a 96 in the 7th epoch itself! (please note that the numbers chosen were a little arbitrary, I just
chose 444 for something close to 450) Doing a hill-climb type search in 400-444 gave 403 as the best choice. Time: 13s/epoch. Now I
experimented on the other side of 359 in a similar way. 337 was the pick.

Finally, I experimented with what had not yet been explored: size of regions in the pooling. 3x3 worked superbly.

Now, the final code consistently gives 95-96% accuracy, and takes only 9s/epoch!
