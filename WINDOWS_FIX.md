# 🪟 Windows Fix Guide - Cerebro Galaxy

## 🔧 **Quick Fix for Windows Users**

The user is experiencing these issues:
1. **Backend error**: `Could not import module "main_working"`
2. **Missing dependency**: `No module named 'langgraph'`
3. **Windows commands**: Linux commands don't work on Windows

## 🚀 **Complete Windows Solution**

### **Step 1: Install Dependencies**
```cmd
# Install Python dependencies
pip install fastapi uvicorn websockets pydantic langgraph

# Or install all at once
pip install -r requirements.txt
```

### **Step 2: Fix Backend Import Error**
The backend is trying to import "main_working" instead of "main". 

**Quick Fix:**
```cmd
# Navigate to app directory
cd app

# Edit main.py and change the uvicorn.run line:
# FROM: uvicorn.run("main_working:app", ...)
# TO:   uvicorn.run("main:app", ...)
```

### **Step 3: Start Backend (Windows)**
```cmd
# Navigate to app directory
cd app

# Start backend
python main.py
```

### **Step 4: Start Frontend (Windows)**
```cmd
# Open NEW command prompt
# Navigate to frontend directory
cd src-tauri

# Start frontend
npm run dev
```

### **Step 5: Open Browser**
- **Frontend**: http://localhost:5179 (or whatever port Vite shows)
- **Backend**: http://localhost:8000

## 🛠️ **Windows Commands Reference**

### **Instead of Linux commands, use:**
```cmd
# Instead of: pkill -f "python main.py"
# Use: taskkill /f /im python.exe

# Instead of: ls
# Use: dir

# Instead of: ps aux | grep
# Use: tasklist | findstr
```

## 🎯 **Expected Result**

Once both servers are running:
1. **Backend**: Shows "Uvicorn running on http://0.0.0.0:8000"
2. **Frontend**: Shows "Local: http://localhost:5179/"
3. **Browser**: Galaxy interface loads with Cerebro
4. **Connection**: "Connected" instead of "Backend not connected"

## 🔧 **If Still Having Issues**

### **Backend Won't Start:**
```cmd
# Check if port 8000 is in use
netstat -an | findstr :8000

# Kill any process using port 8000
netstat -ano | findstr :8000
taskkill /PID [PID_NUMBER] /F
```

### **Frontend Won't Start:**
```cmd
# Clear npm cache
npm cache clean --force

# Reinstall dependencies
npm install --legacy-peer-deps
```

### **Dependencies Missing:**
```cmd
# Install all Python dependencies
pip install fastapi uvicorn websockets pydantic langgraph python-multipart

# Install Node.js dependencies
npm install --legacy-peer-deps
```

## 🎉 **Success Indicators**

You'll know it's working when:
- ✅ Backend shows: `INFO: Uvicorn running on http://0.0.0.0:8000`
- ✅ Frontend shows: `Local: http://localhost:5179/`
- ✅ Browser loads the galaxy interface
- ✅ Status shows "Connected" instead of "Backend not connected"
- ✅ Chat responds when you type messages

## 🚀 **Quick Test**

1. **Test Backend**: Visit http://localhost:8000 in browser
2. **Test Frontend**: Visit http://localhost:5179 in browser  
3. **Test Chat**: Type "Hello Cerebro" and watch for response

**The Cerebro Galaxy should now work perfectly on Windows!** 🧠🌌✨
