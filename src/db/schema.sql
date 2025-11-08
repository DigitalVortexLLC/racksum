-- RackSum Database Schema
-- Creates tables for storing sites and rack configurations

-- Create database if it doesn't exist
CREATE DATABASE IF NOT EXISTS racksum;
USE racksum;

-- Sites table - represents a physical location/datacenter
CREATE TABLE IF NOT EXISTS sites (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL UNIQUE,
  description TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Rack configurations table - stores complete rack layouts for a site
CREATE TABLE IF NOT EXISTS rack_configurations (
  id INT AUTO_INCREMENT PRIMARY KEY,
  site_id INT NOT NULL,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  config_data JSON NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (site_id) REFERENCES sites(id) ON DELETE CASCADE,
  UNIQUE KEY unique_site_rack (site_id, name),
  INDEX idx_site_id (site_id),
  INDEX idx_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Add comments to tables
ALTER TABLE sites COMMENT = 'Stores site/datacenter information';
ALTER TABLE rack_configurations COMMENT = 'Stores rack configuration data in JSON format';
