import React, { useState } from 'react';
import { Container, Typography, Box, TextField, Button, Paper, Avatar } from '@mui/material';
import axios from 'axios';
import logo from '../assets/gorqai_logo.png';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const sendMessage = async () => {
    if (!input) return;
    setMessages([...messages, { sender: 'user', text: input }]);
    setInput('');
    const res = await axios.post('http://localhost:7860/api/chat', { message: input });
    setMessages(msgs => [...msgs, { sender: 'bot', text: res.data.response }]);
  };
  return (
    <Container maxWidth="sm">
      <Box display="flex" alignItems="center" mt={4} mb={2}>
        <Avatar src={logo} sx={{ width: 56, height: 56, mr: 2 }} />
        <Typography variant="h4">Gorq AI Chat</Typography>
      </Box>
      <Paper elevation={3} sx={{ p: 2, minHeight: 300 }}>
        {messages.map((msg, i) => (
          <Box key={i} textAlign={msg.sender === 'user' ? 'right' : 'left'}>
            <Typography color={msg.sender === 'user' ? 'primary' : 'secondary'}>{msg.text}</Typography>
          </Box>
        ))}
      </Paper>
      <Box mt={2} display="flex">
        <TextField fullWidth value={input} onChange={e => setInput(e.target.value)} label="Type your message..." />
        <Button variant="contained" onClick={sendMessage} sx={{ ml: 2 }}>Send</Button>
      </Box>
      <Box mt={2} textAlign="center">
        <Typography variant="caption">Powered by <a href="https://gorqai.digital" target="_blank" rel="noopener noreferrer">GorqAiPlatforms</a></Typography>
      </Box>
    </Container>
  );
}
export default App;
