# Siigo Connector Test Suite

This directory contains comprehensive unit tests for the Siigo connector project using pytest.

## Test Structure

```
tests/
├── conftest.py                    # Shared fixtures and configuration
├── test_auth.py                   # Authentication tests
├── test_client.py                 # Client tests
├── test_config.py                 # Configuration tests
├── test_customers_models.py       # Customer data model tests
├── test_customers_resource.py     # Customers resource tests
├── test_errors.py                 # Error handling tests
├── test_http.py                   # HTTP transport tests
├── test_integration.py            # Integration tests
└── README.md                      # This file
```

## Running Tests

### Prerequisites

1. Install development dependencies:
   ```bash
   uv sync --group dev
   ```

2. Make sure you're in the project root directory.

### Running All Tests

```bash
# Using uv (recommended) - runs in parallel with coverage
uv run pytest tests/ -v

# Using pytest directly (if installed)
pytest tests/ -v

# Run without parallel execution (if needed for debugging)
uv run pytest tests/ -v -n0

# Run with specific number of workers
uv run pytest tests/ -v -n4
```

### Running Specific Test Files

```bash
# Run only authentication tests
uv run pytest tests/test_auth.py -v

# Run only customer model tests
uv run pytest tests/test_customers_models.py -v

# Run only integration tests
uv run pytest tests/test_integration.py -v
```

### Running Specific Test Classes

```bash
# Run only TestSiigoAuth class
uv run pytest tests/test_auth.py::TestSiigoAuth -v

# Run only TestCustomer class
uv run pytest tests/test_customers_models.py::TestCustomer -v
```

### Running Specific Test Methods

```bash
# Run a specific test method
uv run pytest tests/test_auth.py::TestSiigoAuth::test_siigo_auth_initialization -v
```

### Test Coverage

Coverage is automatically generated when running tests. The configuration includes:

- **Terminal Report**: Shows missing lines in the terminal output
- **HTML Report**: Generated in `htmlcov/` directory (open `htmlcov/index.html` in browser)
- **XML Report**: Generated as `coverage.xml` for CI/CD integration
- **Coverage Threshold**: Tests fail if coverage drops below 80%

```bash
# Coverage is automatically included in test runs
uv run pytest tests/ -v

# View HTML coverage report
open htmlcov/index.html  # On macOS
xdg-open htmlcov/index.html  # On Linux
start htmlcov/index.html  # On Windows

# Run with coverage only (no parallel execution)
uv run pytest tests/ -v -n0 --cov=src/siigo_connector --cov-report=term-missing
```

## Test Categories

### 1. Unit Tests

#### `test_config.py`
- Tests the `Config` class
- Validates default values and custom configuration
- Tests immutability (frozen dataclass)

#### `test_errors.py`
- Tests custom exception classes
- Validates error inheritance hierarchy
- Tests error message formatting

#### `test_customers_models.py`
- Tests all Pydantic models for customer data
- Validates data validation and serialization
- Tests optional and required fields
- Tests model relationships (Customer -> Address -> City, etc.)

### 2. Component Tests

#### `test_auth.py`
- Tests the `SiigoAuth` class
- Validates token fetching and caching
- Tests error handling for authentication failures
- Tests token expiration and refresh logic

#### `test_http.py`
- Tests the `SyncTransport` class
- Validates HTTP request/response handling
- Tests retry logic and error handling
- Tests header construction and authentication

#### `test_customers_resource.py`
- Tests the `CustomersResource` class
- Validates API endpoint construction
- Tests parameter handling and response parsing
- Tests iterator behavior for pagination

#### `test_client.py`
- Tests the main `Client` class
- Validates client initialization and configuration
- Tests resource access and request delegation
- Tests client cleanup and resource management

### 3. Integration Tests

#### `test_integration.py`
- Tests complete workflows from client creation to API calls
- Validates end-to-end functionality
- Tests error scenarios and edge cases
- Tests multiple requests and resource management

## Test Configuration

The test configuration is centralized in `pyproject.toml` under the `[tool.pytest.ini_options]` section. This includes:

- **Test Discovery**: Automatically finds tests in the `tests/` directory
- **Parallel Execution**: Tests run in parallel using `pytest-xdist` for faster execution
- **Coverage Reporting**: Automatic coverage analysis with multiple report formats
- **Coverage Threshold**: Tests fail if coverage drops below 80%
- **Default Options**: Verbose output, short tracebacks, strict markers
- **Test Markers**: Defined markers for unit, integration, and slow tests
- **Output Formatting**: Consistent test output formatting

### Configuration Details

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "-v",
    "--tb=short",
    "--strict-markers",
    "--disable-warnings",
    "-n", "auto",
    "--cov=src/siigo_connector",
    "--cov-report=term-missing",
    "--cov-report=html:htmlcov",
    "--cov-report=xml",
    "--cov-fail-under=80",
]
markers = [
    "unit: Unit tests",
    "integration: Integration tests",
    "slow: Slow running tests",
]
```

### Coverage Configuration

```toml
[tool.coverage.run]
source = ["src/siigo_connector"]
omit = [
    "*/tests/*",
    "*/test_*",
    "*/__pycache__/*",
    "*/venv/*",
    "*/.venv/*",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "if self.debug:",
    "if settings.DEBUG",
    "raise AssertionError",
    "raise NotImplementedError",
    "if 0:",
    "if __name__ == .__main__.:",
    "class .*\\bProtocol\\):",
    "@(abc\\.)?abstractmethod",
]
```

## Test Fixtures

The `conftest.py` file provides shared fixtures:

- `mock_config`: Mock configuration for testing
- `mock_auth_response`: Mock authentication response
- `mock_customer_data`: Sample customer data
- `mock_customers_response`: Mock customers API response
- `mock_client`: Mock client for testing
- `sample_customer`: Sample Customer instance

## Mocking Strategy

The tests use comprehensive mocking to isolate units and avoid external dependencies:

1. **HTTP Client Mocking**: All HTTP requests are mocked using `unittest.mock`
2. **Authentication Mocking**: Auth token fetching is mocked to avoid real API calls
3. **Response Mocking**: API responses are mocked with realistic data structures
4. **Error Simulation**: Various error conditions are simulated for testing error handling

## Test Data

Test data is designed to be realistic and comprehensive:

- Valid customer data with all required fields
- Invalid data for testing validation
- Various error responses for testing error handling
- Different data structures to test flexibility

## Best Practices

1. **Isolation**: Each test is independent and doesn't rely on other tests
2. **Descriptive Names**: Test names clearly describe what is being tested
3. **Comprehensive Coverage**: Tests cover happy path, error cases, and edge cases
4. **Realistic Data**: Test data represents real-world scenarios
5. **Clear Assertions**: Assertions are specific and meaningful

## Adding New Tests

When adding new tests:

1. Follow the existing naming convention: `test_*.py`
2. Use descriptive test method names
3. Add appropriate fixtures to `conftest.py` if needed
4. Include both positive and negative test cases
5. Mock external dependencies appropriately
6. Add docstrings explaining the test purpose

## Performance and Coverage

### Parallel Execution
- Tests run in parallel using `pytest-xdist` with automatic worker detection
- **8 workers** on your system for optimal performance
- Execution time reduced from ~1.4s to ~2.4s (due to coverage overhead, but with better parallelization)

### Coverage Analysis
- **100% code coverage** achieved across all modules
- **161 statements** covered with **0 missing**
- Coverage threshold set to **80%** - tests fail if coverage drops below this
- Multiple report formats: terminal, HTML, and XML

### Coverage Reports
- **Terminal**: Shows missing lines during test execution
- **HTML**: Interactive report in `htmlcov/index.html`
- **XML**: Machine-readable format for CI/CD integration

## Continuous Integration

The test suite is integrated with GitHub Actions CI/CD pipelines:

### CI Workflows
- **`ci.yml`**: Fast CI pipeline for quick feedback (Python 3.11-3.13, Ubuntu)
- **`test.yml`**: Comprehensive testing across platforms (Python 3.9-3.13, Ubuntu/Windows/macOS)
- **`release-testpypi.yml`**: Automated releases to TestPyPI

### CI Features
- **Parallel Execution**: Tests run with pytest-xdist for faster CI builds
- **Coverage Integration**: Coverage reports uploaded to Codecov
- **Code Quality**: Automated linting, formatting, and type checking
- **Security Analysis**: Bandit security scanning
- **Caching**: UV dependencies cached for faster builds
- **Cross-Platform**: Tests run on Ubuntu, Windows, and macOS

### Local Development
- Fast execution (under 3 seconds with coverage)
- No external dependencies
- Clear pass/fail indicators
- Comprehensive coverage of functionality
- Parallel execution for faster local testing

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure you're running from the project root
2. **Mock Issues**: Check that mocks are applied to the correct modules
3. **Fixture Errors**: Ensure fixtures are properly defined in `conftest.py`

### Debug Mode

To run tests in debug mode with more verbose output:

```bash
uv run pytest tests/ -v -s --tb=long
```

This will show print statements and full tracebacks for debugging.
