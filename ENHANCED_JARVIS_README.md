# 🤖 Enhanced Jarvis AI - Multi-Agent Orchestrator

A powerful, customizable UI for multi-agent orchestration with real-time workflow visualization, performance metrics, and advanced interactivity.

## 🌟 Features

### 🌌 **Galaxy Model Visualization**
- **Hierarchical Workflow View**: Visualize agent workflows as an interactive galaxy
- **Real-time Updates**: Watch workflows evolve in real-time via WebSocket
- **Performance-based Visual Feedback**: Branches thin based on performance metrics
- **Interactive Nodes**: Click, drag, and interact with workflow components

### 💬 **Enhanced Chat Interface**
- **Multiple Chat Modes**: Chat, Research, and Agent modes
- **Customizable Settings**: Font size, themes, message limits
- **Persistent Preferences**: Settings saved across sessions
- **Sound Notifications**: Audio feedback for new messages
- **Export Functionality**: Save chat history as JSON

### 💀 **Dead-End Shelf Management**
- **Failed Task Tracking**: Monitor and manage stalled workflows
- **Priority System**: High, medium, low priority categorization
- **Retry Mechanisms**: One-click task retry with progress tracking
- **Detailed Analysis**: View original inputs and attempted solutions

### 🎛️ **Multi-View Layout System**
- **Galaxy View**: High-level overview of all workflows
- **Crew View**: Detailed agent crew coordination
- **Agent View**: Individual agent monitoring
- **Dead-End View**: Stalled task management
- **Layout Modes**: Default, Focus, and Split view options

### ⚡ **Real-Time Communication**
- **WebSocket Integration**: Instant updates without page refresh
- **Connection Monitoring**: Visual connection status indicators
- **Event-Driven Architecture**: Responsive to system changes
- **Multi-Session Support**: Handle multiple concurrent sessions

### 📊 **Performance Metrics**
- **Live Statistics**: Real-time workflow performance data
- **Task Tracking**: Monitor completion rates and timing
- **System Health**: Connection and resource monitoring
- **Visual Indicators**: Color-coded status representations

## 🚀 Quick Start

### Option 1: Automated Startup (Recommended)

```bash
# Run the automated startup script
python start_jarvis_enhanced.py
```

This script will:
- ✅ Check and install dependencies
- 🚀 Start the backend server (FastAPI)
- 🎨 Start the frontend server (React)
- 🌐 Open your browser automatically
- 📊 Display system status and URLs

### Option 2: Manual Startup

#### Prerequisites
```bash
# Python dependencies
pip install fastapi uvicorn websockets redis pydantic

# Node.js dependencies (in src-tauri directory)
cd src-tauri
npm install
```

#### Start Backend Server
```bash
cd app
python main.py
```
- 📡 API: http://localhost:8000
- 📚 Docs: http://localhost:8000/docs

#### Start Frontend Server
```bash
cd src-tauri
npm run dev
```
- 🌐 UI: http://localhost:5173

## 🎯 Usage Guide

### 1. **Galaxy View Navigation**
- **Default Layout**: Four-pane view with chat, workflow, logs, and HITL
- **Focus Mode**: Full-screen workflow visualization
- **Split View**: Side-by-side chat and workflow
- **Layout Switching**: Use buttons in the view header

### 2. **Chat Customization**
- Click the ⚙️ settings icon in the chat header
- **Theme**: Switch between Dark and Light modes
- **Font Size**: Adjust from 10px to 24px
- **Chat Mode**: Choose Chat, Research, or Agent mode
- **Notifications**: Enable/disable sound alerts

### 3. **Workflow Interaction**
- **Node Selection**: Click nodes to view details
- **Status Monitoring**: Color-coded node states
- **Real-time Updates**: Watch workflows evolve live
- **Simulation**: Use "Simulate" button for testing

### 4. **Dead-End Management**
- Navigate to Dead-End view from sidebar
- **Priority Indicators**: Visual priority levels
- **Retry Tasks**: Click "Retry Task" for failed items
- **Export Data**: Copy task details for analysis

### 5. **HITL (Human-in-the-Loop)**
- Receive approval requests in real-time
- **Approve/Deny**: Make decisions on workflow actions
- **Context Information**: View detailed request context

## 🎨 Customization Options

### **Chat Interface**
- **Themes**: Dark (default) or Light mode
- **Font Sizes**: 10px - 24px range
- **Message Limits**: 10 - 1000 messages
- **Auto-scroll**: Enable/disable automatic scrolling
- **Timestamps**: Show/hide message timestamps
- **Compact Mode**: Space-efficient layout

### **Layout Preferences**
- **View Selection**: Galaxy, Crew, Agent, Dead-End
- **Layout Modes**: Default, Focus, Split
- **Sidebar**: Collapsible navigation panel
- **Persistent Settings**: Preferences saved automatically

### **Workflow Visualization**
- **Node Types**: Start, Agent, Task, Decision, End
- **Status Colors**: Completed (green), Running (blue), Failed (red)
- **Animations**: Pulse for running, blink for HITL required
- **Interactive Elements**: Hover effects and click handlers

## 🔧 Configuration

### **Backend Configuration**
Edit `app/main.py` for:
- **CORS Settings**: Allowed origins for frontend
- **Redis Configuration**: Optional for production scaling
- **WebSocket Settings**: Connection management
- **Logging Levels**: Debug, Info, Warning, Error

### **Frontend Configuration**
Edit `src-tauri/src/socket.js` for:
- **WebSocket URL**: Backend connection endpoint
- **Reconnection Settings**: Automatic reconnection logic
- **Event Handlers**: Custom event processing

## 📊 API Endpoints

### **Workflow Management**
- `GET /api/workflow/{session_id}` - Get workflow state
- `POST /api/workflow/{session_id}/update` - Update workflow
- `POST /api/workflow/{session_id}/simulate` - Trigger simulation

### **Mission Management**
- `POST /api/missions` - Create new mission
- `GET /api/missions/{mission_id}` - Get mission details

### **HITL Management**
- `GET /api/hitl/pending` - Get pending requests
- `POST /api/hitl/request` - Create HITL request
- `POST /api/hitl/{request_id}/approve` - Approve request
- `POST /api/hitl/{request_id}/deny` - Deny request

### **Dead-End Management**
- `GET /api/dead-ends` - Get dead-end tasks
- `POST /api/dead-ends` - Add dead-end task
- `POST /api/dead-ends/{task_id}/retry` - Retry task

### **Agent Management**
- `GET /api/agents` - Get all agents
- `GET /api/agents/{agent_id}` - Get agent details

### **Logging**
- `GET /api/logs` - Stream logs with filters
- `POST /api/logs` - Add log entry

## 🔌 WebSocket Events

### **Client → Server**
- `ping` - Connection health check
- `subscribe` - Subscribe to session updates
- `task_progress` - Report task progress
- `chat_message` - Send chat message

### **Server → Client**
- `pong` - Health check response
- `workflow_updated` - Workflow state changed
- `task_progress` - Task status update
- `hitl_request` - Human input required
- `dead_end_added` - Task moved to dead-end shelf
- `chat_response` - Chat message response

## 🛠️ Development

### **Project Structure**
```
jarvis-ai/
├── app/                    # FastAPI backend
│   └── main.py            # Main server file
├── src-tauri/             # React frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── styles.css     # Global styles
│   │   └── socket.js      # WebSocket client
│   └── package.json       # Node dependencies
├── start_jarvis_enhanced.py # Startup script
└── README.md              # This file
```

### **Adding New Features**

#### **New Workflow Node Types**
1. Add node type to `WorkflowPane.jsx` nodeTypes
2. Create custom component in `components/`
3. Update backend models in `app/main.py`

#### **New Chat Modes**
1. Add mode to `ChatPane.jsx` settings
2. Update backend chat handling
3. Add mode-specific UI elements

#### **New API Endpoints**
1. Add endpoint to `app/main.py`
2. Update frontend API calls
3. Add WebSocket events if needed

### **Testing**
```bash
# Backend testing
cd app
python -m pytest

# Frontend testing
cd src-tauri
npm test

# Integration testing
python test_enhanced_interface.py
```

## 🐛 Troubleshooting

### **Common Issues**

#### **Backend Won't Start**
```bash
# Check Python dependencies
pip install -r requirements.txt

# Check port availability
lsof -i :8000

# Check logs
cd app && python main.py
```

#### **Frontend Won't Start**
```bash
# Reinstall dependencies
cd src-tauri
rm -rf node_modules
npm install

# Check Node.js version
node --version  # Should be 16+
```

#### **WebSocket Connection Issues**
- Check firewall settings
- Verify backend is running on port 8000
- Check browser console for errors
- Try refreshing the page

#### **Chat Not Working**
- Verify WebSocket connection status
- Check backend logs for errors
- Clear browser localStorage
- Try different chat mode

### **Performance Issues**
- **Large Workflows**: Use Focus mode for better performance
- **Memory Usage**: Adjust message limits in chat settings
- **Connection Lag**: Check network connectivity
- **Browser Performance**: Try different browser or clear cache

## 📈 Performance Optimization

### **Backend Optimization**
- **Redis**: Enable for production scaling
- **Connection Pooling**: Configure for high concurrency
- **Logging**: Adjust levels for production
- **Caching**: Implement response caching

### **Frontend Optimization**
- **React Flow**: Optimized for large graphs
- **Virtual Scrolling**: For large message lists
- **Lazy Loading**: Components loaded on demand
- **Memory Management**: Automatic cleanup

## 🔒 Security Considerations

### **Production Deployment**
- **HTTPS**: Use SSL certificates
- **Authentication**: Implement user management
- **CORS**: Restrict allowed origins
- **Rate Limiting**: Prevent abuse
- **Input Validation**: Sanitize all inputs

### **Development Security**
- **Environment Variables**: Store secrets securely
- **Dependencies**: Keep packages updated
- **Code Review**: Review all changes
- **Testing**: Include security tests

## 🤝 Contributing

1. **Fork** the repository
2. **Create** a feature branch
3. **Make** your changes
4. **Test** thoroughly
5. **Submit** a pull request

### **Code Style**
- **Python**: Follow PEP 8
- **JavaScript**: Use ESLint configuration
- **CSS**: Follow BEM methodology
- **Comments**: Document complex logic

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **FastAPI**: Modern Python web framework
- **React Flow**: Powerful workflow visualization
- **Tauri**: Desktop app framework
- **WebSocket**: Real-time communication
- **Redis**: High-performance data store

---

## 🚀 Ready to Get Started?

Run the enhanced Jarvis AI system:

```bash
python start_jarvis_enhanced.py
```

Visit http://localhost:5173 and explore the galaxy of possibilities! 🌌
