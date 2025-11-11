/**
 * Composable for WebAuthn/Passkey authentication
 */
import { ref } from 'vue';
import { logError, logWarn, logInfo, logDebug } from '../utils/logger';

const API_BASE_URL = import.meta.env.VITE_API_URL || '';

// Get CSRF token from cookie
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

// Base64 URL encode/decode helpers
function bufferToBase64URLString(buffer) {
  const bytes = new Uint8Array(buffer);
  let str = '';
  for (const charCode of bytes) {
    str += String.fromCharCode(charCode);
  }
  const base64String = btoa(str);
  return base64String.replace(/\+/g, '-').replace(/\//g, '_').replace(/=/g, '');
}

function base64URLStringToBuffer(base64URLString) {
  const base64 = base64URLString.replace(/-/g, '+').replace(/_/g, '/');
  const padLength = (4 - (base64.length % 4)) % 4;
  const padded = base64.padEnd(base64.length + padLength, '=');
  const binary = atob(padded);
  const bytes = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i++) {
    bytes[i] = binary.charCodeAt(i);
  }
  return bytes.buffer;
}

export function usePasskey() {
  const loading = ref(false);
  const error = ref(null);
  const currentUser = ref(null);
  const authRequired = ref(false);

  /**
   * Check if WebAuthn is supported
   */
  function isSupported() {
    return window.PublicKeyCredential !== undefined;
  }


  /**
   * Get authentication configuration
   */
  async function getAuthConfig() {
    try {
      const response = await fetch(`${API_BASE_URL}/api/auth/config`, {
        credentials: 'same-origin',
      });

      if (response.ok) {
        const data = await response.json();
        authRequired.value = data.require_auth;
        return data;
      }
    } catch (err) {
      logError('Failed to get auth config', err);
    }
    return { require_auth: false, passkey_supported: true };
  }

  /**
   * Register a new passkey
   */
  async function register(username, passkeyName = 'My Passkey') {
    if (!isSupported()) {
      error.value = 'Passkeys are not supported on this device/browser';
      throw new Error(error.value);
    }

    loading.value = true;
    error.value = null;

    try {
      // Step 1: Begin registration (get options from server)
      const beginResponse = await fetch(`${API_BASE_URL}/api/auth/passkey/register/begin`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCsrfToken(),
        },
        credentials: 'same-origin',
        body: JSON.stringify({ username }),
      });

      if (!beginResponse.ok) {
        const data = await beginResponse.json();
        throw new Error(data.error || 'Failed to begin registration');
      }

      const { options, user_id } = await beginResponse.json();
      
      // Parse the options
      const publicKeyOptions = JSON.parse(options);
      
      // Convert base64url strings to ArrayBuffers
      publicKeyOptions.challenge = base64URLStringToBuffer(publicKeyOptions.challenge);
      publicKeyOptions.user.id = base64URLStringToBuffer(publicKeyOptions.user.id);
      
      if (publicKeyOptions.excludeCredentials) {
        publicKeyOptions.excludeCredentials = publicKeyOptions.excludeCredentials.map(cred => ({
          ...cred,
          id: base64URLStringToBuffer(cred.id)
        }));
      }

      // Step 2: Create credential using WebAuthn API
      const credential = await navigator.credentials.create({
        publicKey: publicKeyOptions
      });

      if (!credential) {
        throw new Error('Failed to create credential');
      }

      // Step 3: Send credential to server for verification
      const credentialJSON = {
        id: credential.id,
        rawId: bufferToBase64URLString(credential.rawId),
        response: {
          attestationObject: bufferToBase64URLString(credential.response.attestationObject),
          clientDataJSON: bufferToBase64URLString(credential.response.clientDataJSON),
        },
        type: credential.type,
      };

      const completeResponse = await fetch(`${API_BASE_URL}/api/auth/passkey/register/complete`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCsrfToken(),
        },
        credentials: 'same-origin',
        body: JSON.stringify({
          user_id,
          credential: credentialJSON,
          name: passkeyName,
        }),
      });

      if (!completeResponse.ok) {
        const data = await completeResponse.json();
        throw new Error(data.error || 'Failed to complete registration');
      }

      const result = await completeResponse.json();
      currentUser.value = result.user;
      
      return result;
    } catch (err) {
      error.value = err.message;
      logError('Passkey registration failed', err);
      throw err;
    } finally {
      loading.value = false;
    }
  }

  /**
   * Authenticate with a passkey
   */
  async function login(username = null) {
    if (!isSupported()) {
      error.value = 'Passkeys are not supported on this device/browser';
      throw new Error(error.value);
    }

    loading.value = true;
    error.value = null;

    try {
      // Step 1: Begin authentication (get options from server)
      const beginResponse = await fetch(`${API_BASE_URL}/api/auth/passkey/login/begin`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCsrfToken(),
        },
        credentials: 'same-origin',
        body: JSON.stringify({ username }),
      });

      if (!beginResponse.ok) {
        const data = await beginResponse.json();
        throw new Error(data.error || 'Failed to begin authentication');
      }

      const { options } = await beginResponse.json();
      
      // Parse the options
      const publicKeyOptions = JSON.parse(options);
      
      // Convert base64url strings to ArrayBuffers
      publicKeyOptions.challenge = base64URLStringToBuffer(publicKeyOptions.challenge);
      
      if (publicKeyOptions.allowCredentials) {
        publicKeyOptions.allowCredentials = publicKeyOptions.allowCredentials.map(cred => ({
          ...cred,
          id: base64URLStringToBuffer(cred.id)
        }));
      }

      // Step 2: Get credential using WebAuthn API
      const credential = await navigator.credentials.get({
        publicKey: publicKeyOptions
      });

      if (!credential) {
        throw new Error('Failed to get credential');
      }

      // Step 3: Send credential to server for verification
      const credentialJSON = {
        id: credential.id,
        rawId: bufferToBase64URLString(credential.rawId),
        response: {
          authenticatorData: bufferToBase64URLString(credential.response.authenticatorData),
          clientDataJSON: bufferToBase64URLString(credential.response.clientDataJSON),
          signature: bufferToBase64URLString(credential.response.signature),
          userHandle: credential.response.userHandle ? bufferToBase64URLString(credential.response.userHandle) : null,
        },
        type: credential.type,
      };

      const completeResponse = await fetch(`${API_BASE_URL}/api/auth/passkey/login/complete`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCsrfToken(),
        },
        credentials: 'same-origin',
        body: JSON.stringify({
          credential: credentialJSON,
        }),
      });

      if (!completeResponse.ok) {
        const data = await completeResponse.json();
        throw new Error(data.error || 'Failed to complete authentication');
      }

      const result = await completeResponse.json();
      currentUser.value = result.user;
      
      return result;
    } catch (err) {
      error.value = err.message;
      logError('Passkey authentication failed', err);
      throw err;
    } finally {
      loading.value = false;
    }
  }

  /**
   * Get current authenticated user
   */
  async function getCurrentUser() {
    try {
      const response = await fetch(`${API_BASE_URL}/api/auth/user`, {
        credentials: 'same-origin',
      });

      if (response.ok) {
        const data = await response.json();
        currentUser.value = data.user;
        return data.user;
      }
    } catch (err) {
      logError('Failed to get current user', err);
    }
    return null;
  }

  /**
   * Logout
   */
  async function logout() {
    try {
      const response = await fetch(`${API_BASE_URL}/api/auth/logout`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': getCsrfToken(),
        },
        credentials: 'same-origin',
      });

      if (response.ok) {
        currentUser.value = null;
      }
    } catch (err) {
      logError('Logout failed', err);
    }
  }

  return {
    loading,
    error,
    currentUser,
    authRequired,
    isSupported,
    getAuthConfig,
    register,
    login,
    getCurrentUser,
    logout,
  };
}
