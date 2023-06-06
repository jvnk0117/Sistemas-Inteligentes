*Authors:* 
*Alejandro Perez Gonzalez A01746643*
*Lizbeth Paulina Ayala Parra A01747237*

# Final thoughts
We test diffetnt interpolation parameters and we found out, the one which gives fastest ETA and a bigger accurate response is the INTER_CUBIC, being a bicubic interpolation over 4×4 pixel neighborhood, also we played with different numbers of convolutional layers, playing with diferent filters, enabling padding flags and tampering with the kernel size and the model compiling parameters, such as some experimental Optimizers like nadam and AdamW, Overall we leave some of the settings we saw enhance the model 