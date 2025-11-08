import express from 'express';
import cors from 'cors';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import fs from 'fs';
import dotenv from 'dotenv';
import { testConnection } from './src/db/connection.js';
import { siteService, rackService } from './src/db/services.js';

dotenv.config();

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json({ limit: '10mb' }));

// Test database connection on startup
testConnection().catch(err => {
  console.warn('⚠ Database connection unavailable - file operations will not be persisted');
});

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

// ============================================================================
// SITE ENDPOINTS
// ============================================================================

// Get all sites
app.get('/api/sites', async (req, res) => {
  try {
    const sites = await siteService.getAllSites();
    res.json(sites);
  } catch (error) {
    console.error('Error fetching sites:', error);
    res.status(500).json({
      error: 'Failed to fetch sites',
      details: error.message
    });
  }
});

// Get a single site by ID
app.get('/api/sites/:id', async (req, res) => {
  try {
    const site = await siteService.getSiteById(req.params.id);
    if (!site) {
      return res.status(404).json({ error: 'Site not found' });
    }
    res.json(site);
  } catch (error) {
    console.error('Error fetching site:', error);
    res.status(500).json({
      error: 'Failed to fetch site',
      details: error.message
    });
  }
});

// Create a new site
app.post('/api/sites', async (req, res) => {
  try {
    const { name, description } = req.body;

    if (!name || typeof name !== 'string' || name.trim().length === 0) {
      return res.status(400).json({ error: 'Site name is required' });
    }

    const site = await siteService.createSite(name.trim(), description || null);
    res.status(201).json(site);
  } catch (error) {
    console.error('Error creating site:', error);
    if (error.code === 'ER_DUP_ENTRY') {
      return res.status(409).json({
        error: 'A site with this name already exists'
      });
    }
    res.status(500).json({
      error: 'Failed to create site',
      details: error.message
    });
  }
});

// Update a site
app.put('/api/sites/:id', async (req, res) => {
  try {
    const { name, description } = req.body;

    if (!name || typeof name !== 'string' || name.trim().length === 0) {
      return res.status(400).json({ error: 'Site name is required' });
    }

    const success = await siteService.updateSite(
      req.params.id,
      name.trim(),
      description || null
    );

    if (!success) {
      return res.status(404).json({ error: 'Site not found' });
    }

    res.json({ success: true, message: 'Site updated successfully' });
  } catch (error) {
    console.error('Error updating site:', error);
    if (error.code === 'ER_DUP_ENTRY') {
      return res.status(409).json({
        error: 'A site with this name already exists'
      });
    }
    res.status(500).json({
      error: 'Failed to update site',
      details: error.message
    });
  }
});

// Delete a site
app.delete('/api/sites/:id', async (req, res) => {
  try {
    const success = await siteService.deleteSite(req.params.id);

    if (!success) {
      return res.status(404).json({ error: 'Site not found' });
    }

    res.json({ success: true, message: 'Site deleted successfully' });
  } catch (error) {
    console.error('Error deleting site:', error);
    res.status(500).json({
      error: 'Failed to delete site',
      details: error.message
    });
  }
});

// ============================================================================
// RACK CONFIGURATION ENDPOINTS
// ============================================================================

// Get all rack configurations for a site
app.get('/api/sites/:siteId/racks', async (req, res) => {
  try {
    const racks = await rackService.getRacksBySite(req.params.siteId);
    res.json(racks);
  } catch (error) {
    console.error('Error fetching racks:', error);
    res.status(500).json({
      error: 'Failed to fetch rack configurations',
      details: error.message
    });
  }
});

// Get a specific rack configuration
app.get('/api/sites/:siteId/racks/:rackName', async (req, res) => {
  try {
    const rack = await rackService.getRackConfiguration(
      req.params.siteId,
      req.params.rackName
    );

    if (!rack) {
      return res.status(404).json({ error: 'Rack configuration not found' });
    }

    res.json(rack);
  } catch (error) {
    console.error('Error fetching rack configuration:', error);
    res.status(500).json({
      error: 'Failed to fetch rack configuration',
      details: error.message
    });
  }
});

// Save a rack configuration
app.post('/api/sites/:siteId/racks', async (req, res) => {
  try {
    const { name, configData, description } = req.body;

    if (!name || typeof name !== 'string' || name.trim().length === 0) {
      return res.status(400).json({ error: 'Rack name is required' });
    }

    if (!configData || typeof configData !== 'object') {
      return res.status(400).json({ error: 'Configuration data is required' });
    }

    const rack = await rackService.saveRackConfiguration(
      req.params.siteId,
      name.trim(),
      configData,
      description || null
    );

    res.status(201).json(rack);
  } catch (error) {
    console.error('Error saving rack configuration:', error);
    if (error.code === 'ER_NO_REFERENCED_ROW_2') {
      return res.status(404).json({ error: 'Site not found' });
    }
    res.status(500).json({
      error: 'Failed to save rack configuration',
      details: error.message
    });
  }
});

// Delete a rack configuration
app.delete('/api/racks/:id', async (req, res) => {
  try {
    const success = await rackService.deleteRackConfiguration(req.params.id);

    if (!success) {
      return res.status(404).json({ error: 'Rack configuration not found' });
    }

    res.json({ success: true, message: 'Rack configuration deleted successfully' });
  } catch (error) {
    console.error('Error deleting rack configuration:', error);
    res.status(500).json({
      error: 'Failed to delete rack configuration',
      details: error.message
    });
  }
});

// Get all rack configurations (across all sites)
app.get('/api/racks', async (req, res) => {
  try {
    const racks = await rackService.getAllRacks();
    res.json(racks);
  } catch (error) {
    console.error('Error fetching all racks:', error);
    res.status(500).json({
      error: 'Failed to fetch rack configurations',
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
  console.log(`🏢 Sites API: http://localhost:${PORT}/api/sites`);
  console.log(`🗄️  Racks API: http://localhost:${PORT}/api/racks`);
});