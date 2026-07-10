import cv2
import numpy as np
import imutils

# ===== ENTER YOUR HSV VALUES HERE =====
# Adjust these based on your object color

# Red objects (catches dark/light reds)
LOWER_HSV = (0, 50, 50)
UPPER_HSV = (10, 255, 255)

# For other colors, uncomment below and comment RED above:

# ORANGE objects
# LOWER_HSV = (5, 100, 100)
# UPPER_HSV = (25, 255, 255)

# GREEN objects
# LOWER_HSV = (35, 50, 50)
# UPPER_HSV = (90, 255, 255)

# BLUE objects
# LOWER_HSV = (100, 50, 50)
# UPPER_HSV = (130, 255, 255)

# YELLOW objects
# LOWER_HSV = (20, 100, 100)
# UPPER_HSV = (35, 255, 255)

# =====================================

print("\n" + "="*60)
print("OBJECT TRACKING - LIVE")
print("="*60)
print(f"\nTracking HSV Range:")
print(f"  Lower: {LOWER_HSV}")
print(f"  Upper: {UPPER_HSV}")
print("\nWatch the window for:")
print("  - WHITE CIRCLE = Your object detected")
print("  - RED DOT = Object center")
print("  - Console prints = Direction (Left/Right/Front/Stop)")
print("\nPress Q to exit")
print("="*60 + "\n")

# Open camera
cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cam.set(cv2.CAP_PROP_FPS, 30)
cam.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Reduce buffer to prevent freezing

frame_count = 0

while True:
    ret, frame = cam.read()
    if not ret:
        print("ERROR: Cannot read from camera")
        break
    
    frame_count += 1
    
    # Skip every other frame for performance
    if frame_count % 2 == 0:
        continue
    
    # Resize for faster processing
    frame = imutils.resize(frame, width=600)
    
    # Flip horizontally for mirror effect
    frame = cv2.flip(frame, 1)
    
    # Smooth the image
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    
    # Convert to HSV
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    
    # Create mask
    mask = cv2.inRange(hsv, LOWER_HSV, UPPER_HSV)
    
    # Clean up mask
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    
    # Find contours
    contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    
    # Process if object found
    if len(contours) > 0:
        # Get largest contour
        c = max(contours, key=cv2.contourArea)
        
        # Get circle around object
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        
        # Get center of object
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        
        # Only track if object is big enough
        if radius > 5:
            # Draw circle
            cv2.circle(frame, (int(x), int(y)), int(radius), (255, 255, 255), 2)
            
            # Draw center dot
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
            
            # Determine direction
            if radius > 250:
                direction = "STOP"
            elif center[0] < 150:
                direction = "LEFT"
            elif center[0] > 450:
                direction = "RIGHT"
            else:
                direction = "FRONT"
            
            # Print direction
            print(direction)
            
            # Show direction on screen
            cv2.putText(frame, direction, (center[0] - 40, center[1] - 40), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f"R:{int(radius)}", (int(x), int(y) - 20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 1)
    
    # Show frame
    cv2.imshow("Object Tracking", frame)
    
    # Exit on Q
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        print("\n" + "="*60)
        print("Tracking stopped. Goodbye!")
        print("="*60 + "\n")
        break

cam.release()
cv2.destroyAllWindows()
