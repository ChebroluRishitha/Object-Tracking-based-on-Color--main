import cv2
import numpy as np

# Create trackbars for HSV range
cv2.namedWindow('Color Calibration')

# Hue trackbars
cv2.createTrackbar('Hue Low', 'Color Calibration', 0, 179, lambda x: None)
cv2.createTrackbar('Hue High', 'Color Calibration', 179, 179, lambda x: None)

# Saturation trackbars
cv2.createTrackbar('Sat Low', 'Color Calibration', 100, 255, lambda x: None)
cv2.createTrackbar('Sat High', 'Color Calibration', 255, 255, lambda x: None)

# Value trackbars
cv2.createTrackbar('Val Low', 'Color Calibration', 100, 255, lambda x: None)
cv2.createTrackbar('Val High', 'Color Calibration', 255, 255, lambda x: None)

# Open camera
cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cam.set(cv2.CAP_PROP_FPS, 30)

print("\n" + "="*60)
print("SIMPLE COLOR CALIBRATION TOOL")
print("="*60)
print("\nInstructions:")
print("1. Hold your colored object in front of camera")
print("2. Adjust sliders until ONLY your color is WHITE")
print("3. Copy the HSV values printed at bottom")
print("4. Press Q to close and see final values")
print("\nHSV Color Ranges (for reference):")
print("  Red:    H=0-10, S=50-100, V=50-100")
print("  Orange: H=5-25, S=100-200, V=100-150")
print("  Yellow: H=20-35, S=100-200, V=100-150")
print("  Green:  H=35-90, S=50-150, V=50-150")
print("  Blue:   H=100-130, S=50-150, V=50-150")
print("="*60 + "\n")

while True:
    ret, frame = cam.read()
    if not ret:
        print("ERROR: Cannot read from camera")
        break
    
    # Flip frame horizontally for better view
    frame = cv2.flip(frame, 1)
    
    # Get trackbar values
    h_low = cv2.getTrackbarPos('Hue Low', 'Color Calibration')
    h_high = cv2.getTrackbarPos('Hue High', 'Color Calibration')
    s_low = cv2.getTrackbarPos('Sat Low', 'Color Calibration')
    s_high = cv2.getTrackbarPos('Sat High', 'Color Calibration')
    v_low = cv2.getTrackbarPos('Val Low', 'Color Calibration')
    v_high = cv2.getTrackbarPos('Val High', 'Color Calibration')
    
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Create mask with current values
    lower = np.array([h_low, s_low, v_low])
    upper = np.array([h_high, s_high, v_high])
    mask = cv2.inRange(hsv, lower, upper)
    
    # Show results side by side
    combined = np.hstack((frame, cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)))
    
    # Add text showing current values
    text = f"Low: ({h_low}, {s_low}, {v_low})   High: ({h_high}, {s_high}, {v_high})"
    cv2.putText(combined, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(combined, "LEFT SIDE: Original | RIGHT SIDE: Detected Color (White)", 
                (10, 470), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    
    cv2.imshow('Color Calibration', combined)
    
    # Press Q to quit
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        print("\n" + "="*60)
        print("FINAL HSV VALUES - COPY THESE!")
        print("="*60)
        print(f"\nLower = ({h_low}, {s_low}, {v_low})")
        print(f"Upper = ({h_high}, {s_high}, {v_high})")
        print("\n" + "="*60 + "\n")
        break

cam.release()
cv2.destroyAllWindows()
