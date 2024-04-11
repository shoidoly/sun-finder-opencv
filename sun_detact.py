import cv2
import numpy as np

# Function to calculate circularity of a contour
def calculate_circularity(contour):
    perimeter = cv2.arcLength(contour, True)
    if perimeter == 0:
        return 0.0  # or any other special value to indicate inability to calculate circularity
    else:
        area = cv2.contourArea(contour)
        circularity = (4 * np.pi * area) / (perimeter ** 2)
        return circularity

# Load video
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Preprocessing (e.g., resize, color space conversion)
    # For demonstration, we'll convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Thresholding
    _, thresh = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY)
    
    # Contour detection
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filtering
    max_contour = None
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
        
        
        # Approximate contour to reduce number of points
        epsilon = 0.03 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        
        # Calculate circularity
        circularity = calculate_circularity(approx)
        
        # Filter contours based on circularity
        if area > 100 and max_contour is not None and circularity > 0.85:  # Adjust threshold as needed
            x, y, w, h = cv2.boundingRect(approx)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            # Add label at the bottom of the rectangle
            cv2.putText(frame, f"Area: {area}, Contour: {idx + 1}, Circularity: {round(circularity, 2)}", (x, y+h+20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            # Calculate midpoint of the rectangle
            mid_x = x + w // 2
            mid_y = y + h // 2
            
            # Draw a dot at the midpoint
            cv2.circle(frame, (mid_x, mid_y), 3, (0, 255, 0), -1)

            # Add label with x and y positions
            cv2.putText(frame, f"X: {mid_x}, Y: {mid_y}", (x, y+h+40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            # Get screen midpoint
            screen_mid_x = frame.shape[1] // 2
            screen_mid_y = frame.shape[0] // 2

            # Display camera direction based on the sun position
            if mid_x < screen_mid_x:
                cv2.putText(frame, "Move left", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            else:
                cv2.putText(frame, "Move right", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            if mid_y < screen_mid_y:
                cv2.putText(frame, "Move up", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            else:
                cv2.putText(frame, "Move down", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Display frame
    cv2.imshow('Sun Detection', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()