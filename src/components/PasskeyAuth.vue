<template>
  <div
    v-if="visible"
    class="fixed inset-0 flex items-center justify-center z-50 transition-opacity duration-200"
    style="background-color: rgba(0, 0, 0, 0.3); backdrop-filter: blur(4px);"
    @click.self="close"
  >
    <div class="rounded-xl shadow-2xl w-full max-w-md transform transition-all duration-200" style="background-color: var(--bg-primary);">
      <div class="flex items-center justify-between mb-6 p-6 rounded-t-xl" style="background-color: var(--color-primary);">
        <h2 class="text-2xl font-bold" style="color: #0c0c0d;">{{ isRegistering ? 'Register Passkey' : 'Login with Passkey' }}</h2>
        <button
          @click="close"
          class="transition-colors"
          style="color: rgba(12, 12, 13, 0.7);"
          @mouseover="$event.target.style.color = '#0c0c0d'"
          @mouseout="$event.target.style.color = 'rgba(12, 12, 13, 0.7)'"
        >
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <div class="px-6 pb-6">
        <!-- Current User Display -->
        <div v-if="currentUser" class="mb-4 p-4 rounded" style="background-color: rgba(132, 204, 22, 0.1); border: 1px solid var(--color-primary);">
          <div class="flex items-center justify-between">
            <div>
              <div class="font-medium" style="color: var(--text-primary);">Welcome, {{ currentUser.username }}!</div>
              <div class="text-sm" style="color: var(--text-secondary);">{{ currentUser.email }}</div>
            </div>
            <button
              @click="handleLogout"
              class="px-3 py-1 rounded text-sm transition-colors"
              style="background-color: var(--color-accent); color: white;"
              @mouseover="$event.target.style.opacity = '0.9'"
              @mouseout="$event.target.style.opacity = '1'"
            >
              Logout
            </button>
          </div>
        </div>

        <!-- Error Display -->
        <div v-if="error" class="mb-4 p-3 rounded" style="background-color: #fee2e2; border: 1px solid #fecaca; color: #991b1b;">
          {{ error }}
        </div>

        <!-- Passkey not supported warning -->
        <div v-if="!passkeySupported" class="mb-4 p-3 rounded" style="background-color: #fef3c7; border: 1px solid #fde68a; color: #92400e;">
          Passkeys are not supported on this device or browser. Please use a modern browser with WebAuthn support.
        </div>

        <!-- Username Input (for registration or username-based login) -->
        <div v-if="!currentUser" class="mb-4">
          <label class="block text-sm font-medium mb-2" style="color: var(--text-primary);">
            Username
          </label>
          <input
            v-model="username"
            type="text"
            placeholder="Enter your username"
            class="w-full px-3 py-2 rounded focus:outline-none transition-colors"
            style="border: 1px solid var(--border-color); background-color: var(--bg-secondary); color: var(--text-primary);"
            @focus="$event.target.style.borderColor = 'var(--color-primary)'; $event.target.style.boxShadow = '0 0 0 2px rgba(132, 204, 22, 0.2)'"
            @blur="$event.target.style.borderColor = 'var(--border-color)'; $event.target.style.boxShadow = 'none'"
            @keyup.enter="isRegistering ? handleRegister() : handleLogin()"
          />
        </div>

        <!-- Passkey Name Input (for registration only) -->
        <div v-if="!currentUser && isRegistering" class="mb-4">
          <label class="block text-sm font-medium mb-2" style="color: var(--text-primary);">
            Passkey Name (Optional)
          </label>
          <input
            v-model="passkeyName"
            type="text"
            placeholder="e.g., My MacBook, iPhone, etc."
            class="w-full px-3 py-2 rounded focus:outline-none transition-colors"
            style="border: 1px solid var(--border-color); background-color: var(--bg-secondary); color: var(--text-primary);"
            @focus="$event.target.style.borderColor = 'var(--color-primary)'; $event.target.style.boxShadow = '0 0 0 2px rgba(132, 204, 22, 0.2)'"
            @blur="$event.target.style.borderColor = 'var(--border-color)'; $event.target.style.boxShadow = 'none'"
          />
        </div>

        <!-- Info Text -->
        <div v-if="!currentUser" class="mb-6 text-sm" style="color: var(--text-secondary);">
          {{ isRegistering 
            ? 'Create a new passkey for passwordless authentication. You\'ll use your device\'s biometric sensor or PIN.' 
            : 'Use your passkey to sign in securely without a password.' 
          }}
        </div>

        <!-- Action Buttons -->
        <div v-if="!currentUser" class="flex flex-col gap-3">
          <button
            v-if="isRegistering"
            @click="handleRegister"
            :disabled="!username.trim() || loading || !passkeySupported"
            class="w-full px-4 py-3 text-white rounded transition-colors font-medium"
            :style="{
              backgroundColor: (!username.trim() || loading || !passkeySupported) ? 'var(--color-primary-light)' : 'var(--color-primary)',
              opacity: (!username.trim() || loading || !passkeySupported) ? '0.5' : '1',
              cursor: (!username.trim() || loading || !passkeySupported) ? 'not-allowed' : 'pointer'
            }"
          >
            <span v-if="loading">
              <svg class="w-4 h-4 inline animate-spin mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              Creating Passkey...
            </span>
            <span v-else>Create Passkey</span>
          </button>

          <button
            v-else
            @click="handleLogin"
            :disabled="loading || !passkeySupported"
            class="w-full px-4 py-3 text-white rounded transition-colors font-medium"
            :style="{
              backgroundColor: (loading || !passkeySupported) ? 'var(--color-primary-light)' : 'var(--color-primary)',
              opacity: (loading || !passkeySupported) ? '0.5' : '1',
              cursor: (loading || !passkeySupported) ? 'not-allowed' : 'pointer'
            }"
          >
            <span v-if="loading">
              <svg class="w-4 h-4 inline animate-spin mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              Authenticating...
            </span>
            <span v-else>Sign In with Passkey</span>
          </button>

          <!-- Toggle between login and register -->
          <div class="text-center text-sm" style="color: var(--text-secondary);">
            {{ isRegistering ? 'Already have a passkey?' : 'Need to create a passkey?' }}
            <button
              @click="isRegistering = !isRegistering; error = null"
              class="font-medium transition-colors"
              style="color: var(--color-primary);"
              @mouseover="$event.target.style.textDecoration = 'underline'"
              @mouseout="$event.target.style.textDecoration = 'none'"
            >
              {{ isRegistering ? 'Sign In' : 'Register' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import { usePasskey } from '../composables/usePasskey';
import { useToast } from '../composables/useToast';

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['update:modelValue', 'authenticated']);

const { loading, error, currentUser, isSupported, register, login, getCurrentUser, logout } = usePasskey();
const { showToast } = useToast();

const visible = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
});

const username = ref('');
const passkeyName = ref('');
const isRegistering = ref(false);
const passkeySupported = ref(false);

onMounted(async () => {
  passkeySupported.value = isSupported();
  await getCurrentUser();
});

watch(visible, (isVisible) => {
  if (!isVisible) {
    username.value = '';
    passkeyName.value = '';
    error.value = null;
  }
});

function close() {
  visible.value = false;
}

async function handleRegister() {
  if (!username.value.trim()) return;

  try {
    await register(username.value.trim(), passkeyName.value.trim() || 'My Passkey');
    showToast('success', 'Passkey created successfully!');
    emit('authenticated', currentUser.value);
    close();
  } catch (err) {
    // Error already set in composable
    showToast('error', 'Failed to create passkey');
  }
}

async function handleLogin() {
  try {
    await login(username.value.trim() || null);
    showToast('success', 'Signed in successfully!');
    emit('authenticated', currentUser.value);
    close();
  } catch (err) {
    // Error already set in composable
    showToast('error', 'Failed to sign in');
  }
}

async function handleLogout() {
  await logout();
  showToast('success', 'Logged out successfully');
  close();
}
</script>

<style scoped>
@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.animate-spin {
  animation: spin 1s linear infinite;
}
</style>
