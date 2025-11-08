import pool from './connection.js';

// Site Services
export const siteService = {
  // Create a new site
  async createSite(name, description = null) {
    const [result] = await pool.query(
      'INSERT INTO sites (name, description) VALUES (?, ?)',
      [name, description]
    );
    return { id: result.insertId, name, description };
  },

  // Get all sites
  async getAllSites() {
    const [rows] = await pool.query(
      'SELECT id, name, description, created_at, updated_at FROM sites ORDER BY name'
    );
    return rows;
  },

  // Get a single site by ID
  async getSiteById(id) {
    const [rows] = await pool.query(
      'SELECT id, name, description, created_at, updated_at FROM sites WHERE id = ?',
      [id]
    );
    return rows[0] || null;
  },

  // Get a single site by name
  async getSiteByName(name) {
    const [rows] = await pool.query(
      'SELECT id, name, description, created_at, updated_at FROM sites WHERE name = ?',
      [name]
    );
    return rows[0] || null;
  },

  // Update a site
  async updateSite(id, name, description = null) {
    const [result] = await pool.query(
      'UPDATE sites SET name = ?, description = ? WHERE id = ?',
      [name, description, id]
    );
    return result.affectedRows > 0;
  },

  // Delete a site (will cascade delete all rack configurations)
  async deleteSite(id) {
    const [result] = await pool.query('DELETE FROM sites WHERE id = ?', [id]);
    return result.affectedRows > 0;
  }
};

// Rack Configuration Services
export const rackService = {
  // Save a rack configuration
  async saveRackConfiguration(siteId, name, configData, description = null) {
    const [result] = await pool.query(
      `INSERT INTO rack_configurations (site_id, name, config_data, description)
       VALUES (?, ?, ?, ?)
       ON DUPLICATE KEY UPDATE
       config_data = VALUES(config_data),
       description = VALUES(description),
       updated_at = CURRENT_TIMESTAMP`,
      [siteId, name, JSON.stringify(configData), description]
    );
    return {
      id: result.insertId || result.affectedRows,
      siteId,
      name,
      description
    };
  },

  // Get all rack configurations for a site
  async getRacksBySite(siteId) {
    const [rows] = await pool.query(
      `SELECT id, site_id, name, description, config_data, created_at, updated_at
       FROM rack_configurations
       WHERE site_id = ?
       ORDER BY name`,
      [siteId]
    );
    return rows.map(row => ({
      ...row,
      config_data: typeof row.config_data === 'string'
        ? JSON.parse(row.config_data)
        : row.config_data
    }));
  },

  // Get a specific rack configuration
  async getRackConfiguration(siteId, rackName) {
    const [rows] = await pool.query(
      `SELECT id, site_id, name, description, config_data, created_at, updated_at
       FROM rack_configurations
       WHERE site_id = ? AND name = ?`,
      [siteId, rackName]
    );
    if (rows.length === 0) return null;

    const row = rows[0];
    return {
      ...row,
      config_data: typeof row.config_data === 'string'
        ? JSON.parse(row.config_data)
        : row.config_data
    };
  },

  // Get rack configuration by ID
  async getRackById(id) {
    const [rows] = await pool.query(
      `SELECT id, site_id, name, description, config_data, created_at, updated_at
       FROM rack_configurations
       WHERE id = ?`,
      [id]
    );
    if (rows.length === 0) return null;

    const row = rows[0];
    return {
      ...row,
      config_data: typeof row.config_data === 'string'
        ? JSON.parse(row.config_data)
        : row.config_data
    };
  },

  // Delete a rack configuration
  async deleteRackConfiguration(id) {
    const [result] = await pool.query(
      'DELETE FROM rack_configurations WHERE id = ?',
      [id]
    );
    return result.affectedRows > 0;
  },

  // Get all rack configurations (across all sites)
  async getAllRacks() {
    const [rows] = await pool.query(
      `SELECT rc.id, rc.site_id, rc.name, rc.description, rc.config_data,
              rc.created_at, rc.updated_at, s.name as site_name
       FROM rack_configurations rc
       JOIN sites s ON rc.site_id = s.id
       ORDER BY s.name, rc.name`
    );
    return rows.map(row => ({
      ...row,
      config_data: typeof row.config_data === 'string'
        ? JSON.parse(row.config_data)
        : row.config_data
    }));
  }
};
