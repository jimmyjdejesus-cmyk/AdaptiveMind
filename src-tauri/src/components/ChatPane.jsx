import React, { useState, useEffect, useRef, useCallback } from 'react';
import { socket } from '../socket';
import API_CONFIG, { getApiUrl } from '../config';
import Neo4jConfigForm from './Neo4jConfigForm';

// Chat customization settings with defaults
const DEFAULT_SETTINGS = {
  fontSize: 14,
  theme: 'dark',
  messageLimit: 100,
  autoScroll: true,
  showTimestamps: true,
  soundEnabled: true,
  compactMode: false,
  chatMode: 'chat', // 'chat', 'research', 'agent'
};

// Load settings from localStorage, excluding sensitive Neo4j credentials
const loadSettings = () => {
  try {
    const saved = localStorage.getItem('jarvis-chat-settings');
    const loaded = saved ? { ...DEFAULT_SETTINGS, ...JSON.parse(saved) } : DEFAULT_SETTINGS;
    loaded.neo4jPassword = '';
    return loaded;
  } catch (e) {
    console.error('Failed to load chat settings:', e);
    return DEFAULT_SETTINGS;
  }
};

// Save settings to localStorage without Neo4j credentials
const saveSettings = (settings) => {
  try {
    const { neo4jPassword, ...persistable } = settings;
    localStorage.setItem('jarvis-chat-settings', JSON.stringify(persistable));
  } catch (e) {
    console.error('Failed to save chat settings:', e);
  }
};

const ChatPane = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [settings, setSettings] = useState(loadSettings);
  const [showSettings, setShowSettings] = useState(false);
  const [isConnected, setIsConnected] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const [sessionId] = useState('default-session');
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // Apply settings to the chat pane
  const applySettings = useCallback((newSettings) => {
    setSettings(newSettings);
    saveSettings(newSettings);
    
    // Apply CSS custom properties for dynamic styling
    const chatPane = document.querySelector('.chat-pane');
    if (chatPane) {
      chatPane.style.setProperty('--chat-font-size', `${newSettings.fontSize}px`);
      chatPane.classList.toggle('theme-light', newSettings.theme === 'light');
      chatPane.classList.toggle('theme-dark', newSettings.theme === 'dark');
      chatPane.classList.toggle('compact-mode', newSettings.compactMode);
    }
  }, []);

  // Initialize settings on mount
  useEffect(() => {
    applySettings(settings);
  }, [settings, applySettings]);

  // WebSocket connection management
  useEffect(() => {
    const onConnect = () => {
      setIsConnected(true);
      const systemMessage = {
        // (rest of the component code)
      };
    };
    // ... (rest of useEffect)
  }, []);

  // ... (rest of the component)
};

export default ChatPane;