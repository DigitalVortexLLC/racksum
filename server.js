import express from 'express';
import cors from 'cors';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import fs from 'fs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json({ limit: '10mb' }));

// Serve static files from the dist directory (production)
app.use(express.static(join(__dirname, 'dist')));

// API endpoint to load rack configuration via POST
app.post('/api/load', (req, res) => {
  try {
    const rackConfig = req.body;

    // Validate that the body contains rack configuration data
    if (!rackConfig || typeof rackConfig !== 'object') {
      return res.status(400).json({
        error: 'Invalid rack configuration data'
      });
    }

    // Return the configuration with instructions for the client
    // The client will handle loading this into the application state
    res.json({
      success: true,
      message: 'Configuration received successfully',
      config: rackConfig,
      redirectUrl: `/?loadConfig=true`
    });

  } catch (error) {
    console.error('Error processing rack configuration:', error);
    res.status(500).json({
      error: 'Failed to process rack configuration',
      details: error.message
    });
  }
});

// Serve devices.json
app.get('/api/devices', (req, res) => {
  try {
    const devicesPath = join(__dirname, 'src', 'data', 'devices.json');
    const devices = JSON.parse(fs.readFileSync(devicesPath, 'utf8'));
    res.json(devices);
  } catch (error) {
    console.error('Error loading devices:', error);
    res.status(500).json({
      error: 'Failed to load devices',
      details: error.message
    });
  }
});

// All other routes serve the Vue app
app.get('*', (req, res) => {
  res.sendFile(join(__dirname, 'dist', 'index.html'));
});

app.listen(PORT, () => {
  console.log(`🚀 RackSum server running on http://localhost:${PORT}`);
  console.log(`📊 API endpoint: POST http://localhost:${PORT}/api/load`);
  console.log(`📦 Devices API: GET http://localhost:${PORT}/api/devices`);
});