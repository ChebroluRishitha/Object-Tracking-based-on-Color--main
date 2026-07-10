# 🎥 Object Tracking Based on Color

Real-time **live object detection** and tracking using **HSV color detection** with a **web interface**. Track colored objects (Red, Green, Blue, Orange, Yellow) through your webcam and see directional commands in real-time!

---

## 🚀 **QUICK START - COPY & PASTE COMMANDS**

### **Step 1: Open PowerShell**
Press **Windows Key + R**, type `powershell`, press Enter

### **Step 2: Copy and Paste This Command**
```powershell
cd c:\Users\rishi\OneDrive\Desktop\Object-Tracking-based-on-Color--main ; (Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned) ; (& .\.venv\Scripts\Activate.ps1) ; python web_tracker_app.py
```

Press Enter ↩️

### **Step 3: Wait for Startup Message**
You should see:
```
✓ Camera OK

==================================================
OBJECT TRACKER WEB APP
==================================================

Color Range: HSV (0, 50, 50) to (10, 255, 255)

🌐 Open: http://127.0.0.1:5000
🛑 Stop: Ctrl+C

==================================================
```

### **Step 4: Open Browser**
Copy and paste in browser address bar:
```
http://127.0.0.1:5000
```

Press Enter ↩️

### **Step 5: Test It!**
Hold a **RED, ORANGE, GREEN, BLUE, or YELLOW** object in front of camera. Watch the website show:
- 🟢 **Green circle** around object
- ✅ **"✓ DETECTED"** status in green
- 🧭 **Direction**: LEFT / RIGHT / FRONT / STOP

---

## 📋 **Features**

✅ **Live Webcam Streaming** - Real-time video feed  
✅ **Color Detection** - HSV-based object detection  
✅ **Direction Tracking** - Identifies object movement (Left/Right/Front/Stop)  
✅ **Web Interface** - Beautiful, responsive design  
✅ **Object Size** - Shows radius in pixels  
✅ **Instant Updates** - Smooth 30 FPS performance  

---

## 🎯 **Supported Colors**

| Color | HSV Range | To Use |
|-------|-----------|--------|
| 🔴 **RED** | (0,50,50)-(10,255,255) | Default (already set) |
| 🟠 **ORANGE** | (5,100,100)-(25,255,255) | Edit `web_tracker_app.py` |
| 🟢 **GREEN** | (35,50,50)-(90,255,255) | Edit `web_tracker_app.py` |
| 🔵 **BLUE** | (100,50,50)-(130,255,255) | Edit `web_tracker_app.py` |
| 🟡 **YELLOW** | (20,100,100)-(35,255,255) | Edit `web_tracker_app.py` |

---

## 🔧 **How to Change Color**

1. **Open** `web_tracker_app.py` in VS Code
2. **Find** lines 11-12:
```python
LOWER_HSV = (0, 50, 50)
UPPER_HSV = (10, 255, 255)
```

3. **Replace** with your color (see table above)
4. **Save** (Ctrl+S)
5. **Restart** app (Ctrl+C and run command from Step 2 again)

---

## 📁 **Project Structure**

```
Object-Tracking-based-on-Color--main/
├── .venv/                      # Virtual environment (dependencies)
├── web_tracker_app.py          # ⭐ Main Flask web app (RECOMMENDED)
├── simple_calibration.py       # 🎨 Color calibration tool
├── simple_tracking.py          # 📺 Terminal-based tracking
├── templates/
│   └── index.html              # 🌐 Web interface
└── README.md                   # 📖 Documentation
```

**Only 6 essential files!** 🎯

---

## 📚 **How It Works**

```
1. Webcam captures frame
   ↓
2. Convert BGR → HSV color space
   ↓
3. Create mask (isolate target color)
   ↓
4. Clean mask (erosion/dilation)
   ↓
5. Find object contours
   ↓
6. Calculate position & size
   ↓
7. Determine direction:
   • Radius > 250px → "STOP"
   • X < 150px → "LEFT"
   • X > 450px → "RIGHT"
   • Otherwise → "FRONT"
   ↓
8. Stream to browser in real-time
```

---

## 🛠️ **Troubleshooting**

### **Website shows blank screen**
- Wait 3-5 seconds for browser to fully load
- Press F5 to refresh browser
- Make sure PowerShell app is still running

### **"Camera not found" error**
- Check webcam is connected
- Go to Settings → Privacy → Camera → Allow apps
- Close other apps using camera (Teams, Zoom, etc.)

### **Object not detected**
- Ensure good lighting
- Hold object 20-50cm from camera
- Check if HSV values are correct for your object color

### **"Port 5000 already in use"**
- Close the old PowerShell window
- Or edit `web_tracker_app.py` line 146, change `port=5000` to `port=8080`
- Then open `http://127.0.0.1:8080`

---

## 📊 **Color Calibration Tool**

To find exact HSV values for your object:

```powershell
cd c:\Users\rishi\OneDrive\Desktop\Object-Tracking-based-on-Color--main ; (& .\.venv\Scripts\Activate.ps1) ; python simple_calibration.py
```

- Adjust sliders until only your color shows WHITE
- Press Q to see final HSV values
- Copy those values to `web_tracker_app.py`

---

## 🎓 **What is HSV?**

**HSV** = Hue, Saturation, Value

- **Hue (0-179)**: Color type (Red, Green, Blue, etc.)
- **Saturation (0-255)**: Color purity (how "pure" the color is)
- **Value (0-255)**: Brightness (how light or dark)

HSV is better than RGB for color detection because it separates color from lighting!

---

## ✅ **System Requirements**

- **Python 3.7+**
- **Webcam**
- **Windows/Mac/Linux**
- **Packages**: opencv-python, flask, imutils, numpy, pillow

---

## 📝 **Files Included**

| File | Purpose | Status |
|------|---------|--------|
| `web_tracker_app.py` | Main web app with Flask | ⭐ **USE THIS** |
| `simple_calibration.py` | Find HSV values for your colors | Optional |
| `simple_tracking.py` | Terminal-based tracking | Optional |
| `templates/index.html` | Beautiful web interface | Auto-used |
| `README.md` | Complete documentation | This file |

**Removed unnecessary files:**
- ❌ `colorCalibrationforHSV.py` (old version)
- ❌ `ObjectTrackingBasedOnColor.py` (old version)
- ❌ `Media/` folder (sample videos)
- ❌ `output.mp4` (output files)

---

## 🛑 **To Stop the App**

Press **Ctrl + C** in PowerShell

---

## 📸 **Output Examples**

When object is detected, website shows:
- ✅ Status: "✓ DETECTED"
- 📍 Direction: "LEFT", "RIGHT", "FRONT", or "STOP"
- 📏 Size: Object radius in pixels
- 🎥 Live video with green circle and red dot

---

## 💡 **Tips for Best Results**

1. **Good lighting** - Bright, consistent lighting helps detection
2. **Solid colors** - Pure colors work better than patterns
3. **Correct distance** - Hold object 20-50cm from camera
4. **Test slowly** - Move object slowly to see all directions
5. **Save HSV values** - Write down good HSV ranges for reuse

---

## 🎯 **Example Usage**

```
User: Points RED object at camera

System detects:
├─ Status: ✓ DETECTED
├─ Direction: ⬆️ FRONT
└─ Size: 120 px

User: Moves object LEFT

System detects:
├─ Status: ✓ DETECTED
├─ Direction: ⬅️ LEFT
└─ Size: 95 px

User: Moves object VERY CLOSE

System detects:
├─ Status: ✓ DETECTED
├─ Direction: ⚠️ STOP
└─ Size: 280 px
```

---

## 📞 **Quick Reference**

| Task | Command |
|------|---------|
| Start app | See Step 2 above |
| Open browser | `http://127.0.0.1:5000` |
| Stop app | Ctrl + C in PowerShell |
| Calibrate colors | `python simple_calibration.py` |
| Change port | Edit line 146 in `web_tracker_app.py` |

---

## 🔗 **Formulas Used**

- **Minimum Enclosing Circle**: `cv2.minEnclosingCircle(contourArea)`
- **Object Center**: `M = cv2.moments(c); center = (M["m10"]/M["m00"], M["m01"]/M["m00"])`
- **Color Mask**: `cv2.inRange(HSV, lower, upper)`

---

## 📄 **License**

Open source - Free to use and modify

---

**Ready? Follow the Quick Start section above!** 🚀
