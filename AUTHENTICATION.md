# Passkey Authentication

RackSum supports optional passwordless authentication using WebAuthn/FIDO2 passkeys.

## Features

- **Passwordless Login**: Use your device's biometric sensor (Touch ID, Face ID, Windows Hello) or PIN
- **Multiple Passkeys**: Register multiple passkeys per user
- **Optional**: Authentication can be enabled or disabled based on your needs
- **Secure**: Uses industry-standard WebAuthn/FIDO2 protocol
- **No Password Management**: No passwords to remember or manage

## Configuration

Authentication is controlled by the `REQUIRE_AUTH` environment variable in your `.env` file:

```bash
# Disable authentication (default)
REQUIRE_AUTH=false

# Enable authentication
REQUIRE_AUTH=true
```

### When Authentication is Disabled (`REQUIRE_AUTH=false`)

- The passkey button is **hidden** from the interface
- All API endpoints are accessible without authentication
- Users can freely save/load configurations without logging in
- Ideal for personal/local use or trusted environments

### When Authentication is Enabled (`REQUIRE_AUTH=true`)

- The passkey button (key icon) appears in the header
- Users must register and authenticate with a passkey
- Protected API endpoints require authentication
- Ideal for multi-user or production environments

## How to Use Passkeys

### First Time Setup (Registration)

1. Click the key icon in the header
2. Enter a username
3. Optionally name your passkey (e.g., "My MacBook", "iPhone")
4. Click "Create Passkey"
5. Follow your device's prompts to register your biometric or PIN

### Signing In

1. Click the key icon in the header
2. Click "Sign In with Passkey" (or toggle from Register)
3. Enter your username (or leave blank for discoverable credentials)
4. Click "Sign In with Passkey"
5. Authenticate with your device's biometric or PIN

### Managing Passkeys

- Each user can register multiple passkeys (different devices)
- View your passkeys in the Django admin at `/admin`
- Delete passkeys you no longer use

## WebAuthn Configuration

You can customize the WebAuthn settings in your `.env` file:

```bash
# Relying Party ID (usually your domain)
WEBAUTHN_RP_ID=localhost

# Relying Party Name (displayed to users)
WEBAUTHN_RP_NAME=RackSum

# Origin (must match your application URL)
WEBAUTHN_ORIGIN=http://localhost:3000
```

### For Production

When deploying to production:

1. Update `WEBAUTHN_RP_ID` to your domain (e.g., `racksum.example.com`)
2. Update `WEBAUTHN_ORIGIN` to your HTTPS URL (e.g., `https://racksum.example.com`)
3. Set `SESSION_COOKIE_SECURE=True` in Django settings
4. Set `CSRF_COOKIE_SECURE=True` in Django settings

## Browser/Device Support

Passkeys work on:

- **macOS/iOS**: Touch ID, Face ID
- **Windows**: Windows Hello (fingerprint, facial recognition, PIN)
- **Android**: Fingerprint, facial recognition, screen lock
- **Hardware Keys**: YubiKey, Titan Security Key, etc.

## Database Models

Two models store passkey data:

### Passkey
- User's registered passkey credentials
- Public key, credential ID, signature counter
- User-friendly name for each passkey

### PasskeyChallenge
- Temporary challenges during registration/authentication
- Automatically cleaned up after use
- Expires after 5 minutes

## Security Notes

- Passkeys use public-key cryptography (private key never leaves your device)
- Phishing-resistant (tied to specific domain)
- Replay-resistant (signature counter prevents reuse)
- No shared secrets (unlike passwords)
- CSRF protection enabled for all authentication endpoints

## Troubleshooting

### Passkey button doesn't appear

- Check that `REQUIRE_AUTH=true` in your `.env` file
- Restart the Django server to apply environment changes
- Rebuild the Vue app: `npm run build`

### "Passkeys not supported" message

- Use a modern browser (Chrome 109+, Safari 16+, Firefox 119+)
- Ensure you're accessing via `http://localhost` or HTTPS
- Some browsers require HTTPS for production domains

### Authentication fails

- Clear browser cookies and try again
- Check that `WEBAUTHN_ORIGIN` matches your URL exactly
- Verify your device/browser supports WebAuthn

### Can't access admin

- Create a superuser: `python manage.py createsuperuser`
- Or use an existing passkey-authenticated user
- Access admin at: `http://localhost:3000/admin`

## API Endpoints

All authentication endpoints are under `/api/auth/`:

- `GET /api/auth/config` - Get authentication configuration
- `POST /api/auth/passkey/register/begin` - Start passkey registration
- `POST /api/auth/passkey/register/complete` - Complete passkey registration
- `POST /api/auth/passkey/login/begin` - Start passkey authentication
- `POST /api/auth/passkey/login/complete` - Complete passkey authentication
- `GET /api/auth/passkey/list` - List user's passkeys (authenticated)
- `DELETE /api/auth/passkey/<id>` - Delete a passkey (authenticated)
- `POST /api/auth/logout` - Logout current session
- `GET /api/auth/user` - Get current authenticated user

## Disabling Authentication

To disable authentication entirely:

1. Edit `.env` and set `REQUIRE_AUTH=false`
2. Restart the server: `./start_server.sh`
3. The passkey button will be hidden from the UI
4. All endpoints become publicly accessible

This is useful for:
- Development and testing
- Personal single-user deployments
- Trusted network environments
- When you want to manage access control at the network level
