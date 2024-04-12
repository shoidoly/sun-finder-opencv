# sun-finder-opencv



## Getting started

Run sun_detact. 
```
$ python sun_detact.py
```
## opencv
OpenCV, which stands for Open Source Computer Vision Library, is an open-source computer vision and machine learning software library. It provides a wide range of tools and functionalities for processing, analyzing, and understanding images and videos. Originally developed by Intel in 1999, OpenCV has since grown into one of the most widely used libraries in the field of computer vision.

- URL: https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html

### Filters
- Area of contours: The area filter is applied to contours detected in the thresholded image. It helps remove small contours that are likely to be noise or irrelevant to the object of interest, which in this case is the sun. Here's how the area filter is implemented in the provided code:
```
for idx, contour in enumerate(contours):
    area = cv2.contourArea(contour)
    # Filter contours based on area
    if area > 100: 
```
- Intensity: intensity filter is used to further refine the selection of contours based on their intensity or brightness. This filter helps identify contours that represent bright regions in the image, which may correspond to the sun or other important features.
```
max_intensity = 0
    for idx, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        # Filter contours based on area
        if area > 100:  # Adjust threshold as needed
            # Calculate intensity of the contour
            mask = np.zeros_like(gray)
            cv2.drawContours(mask, [contour], -1, (255), thickness=cv2.FILLED)
            intensity = cv2.mean(gray, mask=mask)[0]
            
            # Update max contour based on intensity
            if intensity > max_intensity:
                max_intensity = intensity
                max_contour = contour
```
- Circulation: Circularity filtering is a technique used in image processing and computer vision to identify and isolate contours that closely resemble circular shapes. This filter is particularly useful when the objects of interest in an image or video exhibit circular or near-circular characteristics, such as detecting coins, cells, or, in this case, the sun.

```
# Function to calculate circularity of a contour
def calculate_circularity(contour):
    perimeter = cv2.arcLength(contour, True)
    if perimeter == 0:
        return 0.0  # or any other special value to indicate inability to calculate circularity
    else:
        area = cv2.contourArea(contour)
        circularity = (4 * np.pi * area) / (perimeter ** 2)
        return circularity

# Filter contours based on circularity
        if area > 100 and max_contour is not None and circularity > 0.85:  # Adjust threshold as needed
```

## Key operation

1. Q : Close the app. 

## Demo images
![with_flash_light_01.PNG](https://gitlab.galvanize.com/ryan.song.f032/sun-finder-opencv/-/raw/main/images/demo/with_flash_light_01.PNG)

![with_flash_light_02.PNG](https://gitlab.galvanize.com/ryan.song.f032/sun-finder-opencv/-/raw/main/images/demo/with_flash_light_02.PNG)

![with_flash_light_03.PNG](https://gitlab.galvanize.com/ryan.song.f032/sun-finder-opencv/-/raw/main/images/demo/with_flash_light_03.PNG)

![with_flash_light_04.PNG](https://gitlab.galvanize.com/ryan.song.f032/sun-finder-opencv/-/raw/main/images/demo/with_flash_light_04.PNG)

![with_sun_01.PNG](https://gitlab.galvanize.com/ryan.song.f032/sun-finder-opencv/-/raw/main/images/demo/with_sun_01.PNG)

![with_sun_02.PNG](https://gitlab.galvanize.com/ryan.song.f032/sun-finder-opencv/-/raw/main/images/demo/with_sun_02.PNG)
