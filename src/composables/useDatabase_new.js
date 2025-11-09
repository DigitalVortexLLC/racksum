import { ref } from 'vue';

const API_BASE_URL = import.meta.env.VITE_API_URL || '';

// Reactive state for current site
const currentSite = ref(null);
const sites = ref([]);

/**
 * Get CSRF token from cookie
 */
function getCsrfToken() {
  const name = 'csrftoken';
  let cookieValue = null;
  if (document.cookie && document.cookie \!== '') {
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
    credentials: 'same-origin', // Include cookies in same-origin requests
  };

  // Add CSRF token for state-changing requests
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
