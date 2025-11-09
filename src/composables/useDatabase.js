import { ref } from 'vue';

const API_BASE_URL = import.meta.env.VITE_API_URL || '';

// Reactive state for current site
const currentSite = ref(null);
const sites = ref([]);
const currentRackName = ref(null); // Track loaded rack configuration name for auto-save

/**
 * Get CSRF token from cookie
 */
function getCsrfToken() {
  const name = 'csrftoken';
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

/**
 * Create fetch options with CSRF token for POST/PUT/PATCH/DELETE requests
 */
function createFetchOptions(method, body = null) {
  const options = {
    method,
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'same-origin',
  };

  if (['POST', 'PUT', 'PATCH', 'DELETE'].includes(method.toUpperCase())) {
    const csrfToken = getCsrfToken();
    if (csrfToken) {
      options.headers['X-CSRFToken'] = csrfToken;
    }
  }

  if (body) {
    options.body = JSON.stringify(body);
  }

  return options;
}

export function useDatabase() {
  const loading = ref(false);
  const error = ref(null);

  // ============================================================================
  // SITE OPERATIONS
  // ============================================================================

  /**
   * Fetch all sites from database
   */
  async function fetchSites() {
    loading.value = true;
    error.value = null;

    try {
      const response = await fetch(`${API_BASE_URL}/api/sites`, {
        credentials: 'same-origin',
      });

      if (!response.ok) {
        throw new Error(`Failed to fetch sites: ${response.statusText}`);
      }

      sites.value = await response.json();
      return sites.value;
    } catch (err) {
      error.value = err.message;
      console.error('Error fetching sites:', err);
      throw err;
    } finally {
      loading.value = false;
    }
  }

  /**
   * Create a new site
   */
  async function createSite(name, description = null) {
    loading.value = true;
    error.value = null;

    try {
      const response = await fetch(
        `${API_BASE_URL}/api/sites`,
        createFetchOptions('POST', { name, description })
      );

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to create site');
      }

      const site = await response.json();
      sites.value.push(site);
      return site;
    } catch (err) {
      error.value = err.message;
      console.error('Error creating site:', err);
      throw err;
    } finally {
      loading.value = false;
    }
  }

  /**
   * Update an existing site
   */
  async function updateSite(id, name, description = null) {
    loading.value = true;
    error.value = null;

    try {
      const response = await fetch(
        `${API_BASE_URL}/api/sites/${id}`,
        createFetchOptions('PUT', { name, description })
      );

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to update site');
      }

      // Update local sites array
      const index = sites.value.findIndex(s => s.id === id);
      if (index !== -1) {
        sites.value[index] = { ...sites.value[index], name, description };
      }

      return await response.json();
    } catch (err) {
      error.value = err.message;
      console.error('Error updating site:', err);
      throw err;
    } finally {
      loading.value = false;
    }
  }

  /**
   * Delete a site
   */
  async function deleteSite(id) {
    loading.value = true;
    error.value = null;

    try {
      const response = await fetch(
        `${API_BASE_URL}/api/sites/${id}`,
        createFetchOptions('DELETE')
      );

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to delete site');
      }

      // Remove from local sites array
      sites.value = sites.value.filter(s => s.id !== id);

      // Clear current site if it was deleted
      if (currentSite.value?.id === id) {
        currentSite.value = null;
      }

      return await response.json();
    } catch (err) {
      error.value = err.message;
      console.error('Error deleting site:', err);
      throw err;
    } finally {
      loading.value = false;
    }
  }

  /**
   * Set the current active site
   */
  function setCurrentSite(site) {
    currentSite.value = site;
    if (site) {
      localStorage.setItem('racksum-current-site', JSON.stringify(site));
    } else {
      localStorage.removeItem('racksum-current-site');
      currentRackName.value = null;
      localStorage.removeItem('racksum-current-rack-name');
    }
  }

  /**
   * Set the current rack configuration name (for auto-save)
   */
  function setCurrentRackName(rackName) {
    currentRackName.value = rackName;
    if (rackName) {
      localStorage.setItem('racksum-current-rack-name', rackName);
    } else {
      localStorage.removeItem('racksum-current-rack-name');
    }
  }

  /**
   * Load current site from localStorage
   */
  function loadCurrentSite() {
    try {
      const saved = localStorage.getItem('racksum-current-site');
      if (saved) {
        currentSite.value = JSON.parse(saved);
      }
      const savedRackName = localStorage.getItem('racksum-current-rack-name');
      if (savedRackName) {
        currentRackName.value = savedRackName;
      }
    } catch (err) {
      console.error('Error loading current site:', err);
    }
  }

  /**
   * Auto-save the current rack configuration (silent save without user interaction)
   */
  async function autoSaveRackConfiguration(configData) {
    // Only auto-save if we have both a current site and rack name
    if (!currentSite.value || !currentRackName.value) {
      return;
    }

    try {
      // Silent save - don't set loading state to avoid UI flicker
      await fetch(
        `${API_BASE_URL}/api/sites/${currentSite.value.id}/racks`,
        createFetchOptions('POST', {
          name: currentRackName.value,
          configData,
          description: null,
        })
      );
      // Don't throw errors or show notifications for auto-save
    } catch (err) {
      console.warn('Auto-save failed:', err);
    }
  }

  // ============================================================================
  // RACK CONFIGURATION OPERATIONS
  // ============================================================================

  /**
   * Save a rack configuration to the database
   */
  async function saveRackConfiguration(siteId, rackName, configData, description = null) {
    loading.value = true;
    error.value = null;

    try {
      const response = await fetch(
        `${API_BASE_URL}/api/sites/${siteId}/racks`,
        createFetchOptions('POST', {
          name: rackName,
          configData,
          description,
        })
      );

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to save rack configuration');
      }

      return await response.json();
    } catch (err) {
      error.value = err.message;
      console.error('Error saving rack configuration:', err);
      throw err;
    } finally {
      loading.value = false;
    }
  }

  /**
   * Load rack configurations for a site
   */
  async function loadRacksBySite(siteId) {
    loading.value = true;
    error.value = null;

    try {
      const response = await fetch(`${API_BASE_URL}/api/sites/${siteId}/racks`, {
        credentials: 'same-origin',
      });

      if (!response.ok) {
        throw new Error(`Failed to load rack configurations: ${response.statusText}`);
      }

      return await response.json();
    } catch (err) {
      error.value = err.message;
      console.error('Error loading rack configurations:', err);
      throw err;
    } finally {
      loading.value = false;
    }
  }

  /**
   * Load a specific rack configuration
   */
  async function loadRackConfiguration(siteId, rackName) {
    loading.value = true;
    error.value = null;

    try {
      const response = await fetch(
        `${API_BASE_URL}/api/sites/${siteId}/racks/${encodeURIComponent(rackName)}`
      );

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to load rack configuration');
      }

      return await response.json();
    } catch (err) {
      error.value = err.message;
      console.error('Error loading rack configuration:', err);
      throw err;
    } finally {
      loading.value = false;
    }
  }

  /**
   * Delete a rack configuration
   */
  async function deleteRackConfiguration(rackId) {
    loading.value = true;
    error.value = null;

    try {
      const response = await fetch(
        `${API_BASE_URL}/api/racks/${rackId}`,
        createFetchOptions('DELETE')
      );

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to delete rack configuration');
      }

      return await response.json();
    } catch (err) {
      error.value = err.message;
      console.error('Error deleting rack configuration:', err);
      throw err;
    } finally {
      loading.value = false;
    }
  }

  /**
   * Get all rack configurations across all sites
   */
  async function getAllRacks() {
    loading.value = true;
    error.value = null;

    try {
      const response = await fetch(`${API_BASE_URL}/api/racks`, {
        credentials: 'same-origin',
      });

      if (!response.ok) {
        throw new Error(`Failed to fetch rack configurations: ${response.statusText}`);
      }

      return await response.json();
    } catch (err) {
      error.value = err.message;
      console.error('Error fetching rack configurations:', err);
      throw err;
    } finally {
      loading.value = false;
    }
  }

  return {
    // State
    loading,
    error,
    currentSite,
    currentRackName,
    sites,

    // Site operations
    fetchSites,
    createSite,
    updateSite,
    deleteSite,
    setCurrentSite,
    loadCurrentSite,
    setCurrentRackName,

    // Rack operations
    saveRackConfiguration,
    loadRacksBySite,
    loadRackConfiguration,
    deleteRackConfiguration,
    getAllRacks,
    autoSaveRackConfiguration,
  };
}
