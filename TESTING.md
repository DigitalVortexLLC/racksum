# Testing Guide

This document explains the testing setup and how to run tests for the Racker project.

## Overview

Racker uses a comprehensive testing setup with:
- **Frontend**: Vitest + Vue Test Utils for component and unit tests
- **Backend**: Django TestCase for API and model tests
- **Linting**: ESLint for JavaScript/Vue, Flake8/Black/Pylint for Python
- **CI/CD**: GitHub Actions for automated testing

## Frontend Testing

### Setup

The frontend uses Vitest as the test runner with Vue Test Utils for component testing.

Dependencies:
- `vitest` - Fast unit test framework
- `@vue/test-utils` - Vue component testing utilities
- `jsdom` - DOM implementation for Node.js
- `@vitest/ui` - UI for viewing test results

### Running Tests

```bash
# Run all tests once
npm test

# Run tests in watch mode (auto-rerun on file changes)
npm run test:watch

# Run tests with coverage report
npm run test:coverage

# View test UI in browser
npm run test:ui
```

### Writing Tests

Tests are located in `src/tests/` directory.

Example test:
```javascript
import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import MyComponent from '../components/MyComponent.vue';

describe('MyComponent', () => {
  it('renders properly', () => {
    const wrapper = mount(MyComponent, {
      props: { msg: 'Hello' }
    });
    expect(wrapper.text()).toContain('Hello');
  });
});
```

### Test Coverage

Coverage reports are generated in the `coverage/` directory:
- `coverage/index.html` - HTML coverage report
- `coverage/coverage-final.json` - JSON coverage data

## Backend Testing

### Setup

The backend uses Django's built-in TestCase framework.

Dependencies:
- `pytest` - Modern Python testing framework
- `pytest-django` - Django plugin for pytest
- `pytest-cov` - Coverage plugin

### Running Tests

```bash
# Run all Django tests
cd backend
python manage.py test

# Run with verbosity
python manage.py test --verbosity=2

# Run specific test module
python manage.py test api.tests.SiteModelTest

# Run specific test method
python manage.py test api.tests.SiteModelTest.test_site_creation
```

### Writing Tests

Tests are located in `backend/api/tests.py`.

Example test:
```python
from django.test import TestCase
from .models import Site

class SiteModelTest(TestCase):
    def setUp(self):
        self.site = Site.objects.create(name="Test Site")

    def test_site_creation(self):
        self.assertEqual(self.site.name, "Test Site")
        self.assertIsNotNone(self.site.uuid)
```

## Linting

### Frontend Linting

**ESLint** checks JavaScript/Vue code quality:

```bash
# Check for linting errors
npm run lint:check

# Fix auto-fixable linting errors
npm run lint
```

**Prettier** formats code consistently:

```bash
# Check formatting
npm run format:check

# Format files
npm run format
```

### Backend Linting

**Flake8** checks Python code style:

```bash
cd backend
flake8 api/ backend/ --max-line-length=120
```

**Black** formats Python code:

```bash
cd backend

# Check formatting
black --check .

# Format files
black .
```

**Pylint** provides additional code quality checks:

```bash
cd backend
pylint api/ backend/ --disable=C0111,R0903,C0103
```

## CI/CD Pipeline

GitHub Actions automatically runs tests on every push and pull request.

### Workflow Jobs

1. **Frontend Tests** (`frontend`)
   - Runs on Node.js 20.x and 22.x
   - Executes ESLint
   - Runs Vitest tests
   - Builds the frontend
   - Uploads build artifacts

2. **Backend Tests** (`backend`)
   - Runs on Python 3.10, 3.11, and 3.12
   - Spins up MySQL test database
   - Runs Black, Flake8, and Pylint
   - Executes Django system checks
   - Runs Django tests

3. **Documentation Build** (`docs`)
   - Validates MkDocs can build successfully
   - Uploads documentation artifacts

4. **Security Scan** (`security`)
   - Runs `npm audit` for frontend dependencies
   - Runs `safety check` for Python dependencies

### Viewing CI Results

1. Go to the **Actions** tab on GitHub
2. Select the workflow run
3. View individual job results
4. Download artifacts (builds, coverage reports)

### Local CI Simulation

To run tests similar to CI locally:

```bash
# Frontend
npm ci
npm run lint
npm test
npm run build

# Backend
cd backend
pip install -r ../requirements.txt
pip install flake8 black pylint pytest pytest-django
black --check .
flake8 api/ backend/
python manage.py test
```

## Test Database

### Frontend

Frontend tests use mocked APIs and don't require a database.

### Backend

Backend tests use Django's test database which:
- Creates a temporary database for each test run
- Destroys the database after tests complete
- Isolates tests from your development data

For CI, tests use MySQL 8.0:
- Database: `racker_test`
- User: `root`
- Password: `test_password`

## Best Practices

### Writing Good Tests

1. **Test one thing at a time**: Each test should verify one specific behavior
2. **Use descriptive names**: Test names should explain what they test
3. **Setup and teardown**: Use `setUp()`/`beforeEach()` for common test setup
4. **Don't test implementation details**: Test public interfaces, not internals
5. **Mock external dependencies**: Don't rely on external services in tests

### Code Coverage Goals

- **Aim for 80%+ coverage** for critical business logic
- **100% coverage** for utility functions and composables
- **Focus on meaningful tests** over just hitting coverage targets

### Test Organization

- **Frontend**: Organize tests by component/composable in `src/tests/`
- **Backend**: Keep tests close to the code they test (in app's `tests.py`)
- **Integration tests**: Test interactions between components
- **Unit tests**: Test individual functions/methods in isolation

## Troubleshooting

### Tests Failing Locally But Pass in CI

- Check Node.js/Python versions match CI
- Ensure all dependencies are installed
- Clear caches: `npm ci` (frontend) or `pip install --force-reinstall` (backend)

### Tests Pass Locally But Fail in CI

- Check environment variables
- Verify database configuration
- Look for hardcoded paths or assumptions

### Slow Tests

- Use test doubles (mocks/stubs) instead of real dependencies
- Minimize database queries
- Run tests in parallel when possible

## Additional Resources

- [Vitest Documentation](https://vitest.dev/)
- [Vue Test Utils Guide](https://test-utils.vuejs.org/)
- [Django Testing Documentation](https://docs.djangoproject.com/en/5.0/topics/testing/)
- [ESLint Rules](https://eslint.org/docs/rules/)
- [Flake8 Documentation](https://flake8.pycqa.org/)
