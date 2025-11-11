/**
 * Fetch wrapper with timeout support
 * Prevents hanging requests from freezing the UI
 */

const DEFAULT_TIMEOUT = 30000; // 30 seconds

/**
 * Fetch with timeout
 * @param {string} url - The URL to fetch
 * @param {Object} options - Fetch options
 * @param {number} timeout - Timeout in milliseconds (default: 30000)
 * @returns {Promise<Response>}
 */
export async function fetchWithTimeout(url, options = {}, timeout = DEFAULT_TIMEOUT) {
  const controller = new AbortController();
  const id = setTimeout(() => controller.abort(), timeout);

  try {
    const response = await fetch(url, {
      ...options,
      signal: controller.signal,
    });
    clearTimeout(id);
    return response;
  } catch (error) {
    clearTimeout(id);
    if (error.name === 'AbortError') {
      throw new Error(`Request timeout after ${timeout}ms`);
    }
    throw error;
  }
}

/**
 * Create a fetch function with a custom default timeout
 * @param {number} defaultTimeout - Default timeout in milliseconds
 * @returns {Function}
 */
export function createFetchWithTimeout(defaultTimeout) {
  return (url, options = {}, timeout = defaultTimeout) =>
    fetchWithTimeout(url, options, timeout);
}

export default fetchWithTimeout;
