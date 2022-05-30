# Networking
GUI for FRC Vision 

## How to run

Git clone this repository and then run the network.py file. You should see a gui window open up. 

## How to use

Swap frames by pressing the three buttons on the left. The sliders underneath the frame are for HSV. First three are low values and second group of three are high values. Play around with these sliders until you find the right color detection. Make sure to adjust sliders on the right to accurately detect the object. To take screenshots, enter path and click on the screenshot button. If no path is specified, image will be saved to current directory. 

## Sample run

Launch screen 

![image](https://user-images.githubusercontent.com/74515743/170805004-0817ec0c-4e9a-445f-adc5-9ddb0467b3fe.png)

Frame with debug mode (outlines contours)

![image](https://user-images.githubusercontent.com/74515743/170805024-7f19ce53-3611-40c6-a1bc-fc5e9d40a6b1.png)



## Dependencies

- OpenCV
- Numpy
- Os
- PIL
- tkinter
- customtkinter 
- time
- sys

## Credits

https://github.com/TomSchimansky/CustomTkinter




## Testing in-progreess 

Still need to add and modify websocket handlers... 
