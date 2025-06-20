const express = require('express');
const cors = require('cors');
const axios = require('axios');
const app = express();
app.use(cors());
app.use(express.json());

// Proxy endpoint to Python backend
app.post('/api/chat', async (req, res) => {
  try {
    const { message } = req.body;
    // Replace with your Python backend URL
    const response = await axios.post('http://localhost:7860/api/chat', { message });
    res.json(response.data);
  } catch (err) {
    res.status(500).json({ error: 'Backend error' });
  }
});

app.listen(3001, () => {
  console.log('Node.js API running on http://localhost:3001');
});
