# Test Documentation

This document provides an overview of the test files for the GitHub Organization Client project.

## test_utils.py

Unit tests for the utility functions in `utils.py`.

### TestAccessNestedMap

Tests the `access_nested_map` function which navigates through nested dictionaries using a key path.

**Methods:**

- `test_access_nested_map`: Tests successful navigation through nested dictionaries with parameterized inputs
- `test_access_nested_map_exception`: Tests that `KeyError` is raised for invalid paths

**Test Cases:**

- Access single-level keys: `{"a": 1}` with path `("a",)`
- Access nested dictionaries: `{"a": {"b": 2}}` with path `("a", "b")`
- Handle missing keys and invalid paths

### TestGetJson

Tests the `get_json` function which fetches JSON data from URLs.

**Methods:**

- `test_get_json`: Tests that the function correctly calls `requests.get` and returns JSON data

**Features:**

- Uses `unittest.mock.patch` to avoid actual HTTP requests
- Parameterized testing with different URLs and payloads
- Verifies both the return value and that `requests.get` is called correctly

### TestMemoize

Tests the `memoize` decorator which caches method results.

**Methods:**

- `test_memoize`: Tests that decorated methods cache their results and only call the underlying method once

**Features:**

- Uses mock patching to verify method call counts
- Tests that subsequent calls return cached results without re-execution

## test_client.py

Unit and integration tests for the `GithubOrgClient` class in `client.py`.

### TestGithubOrgClient (Unit Tests)

Unit tests for individual methods of the `GithubOrgClient` class.

**Methods:**

- `test_org`: Tests that the `org` property correctly fetches organization data
- `test_public_repos_url`: Tests that `_public_repos_url` property returns the correct URL
- `test_public_repos`: Tests that `public_repos` method returns expected repository names
- `test_has_license`: Tests the static `has_license` method for license checking

**Features:**

- Extensive use of mocking to isolate individual methods
- Parameterized testing for different scenarios
- Tests both successful operations and edge cases

### TestIntegrationGithubOrgClient (Integration Tests)

Integration tests that test the complete workflow of the `GithubOrgClient` class.

**Setup:**

- Uses `@parameterized_class` with fixture data
- `setUpClass`: Mocks `requests.get` with side effects to return appropriate fixture data
- `tearDownClass`: Cleans up the mock patcher

**Methods:**

- `test_public_repos`: Tests the complete flow of fetching all public repositories
- `test_public_repos_with_license`: Tests fetching repositories filtered by license

**Features:**

- Only mocks external HTTP requests, allowing internal code to run normally
- Uses realistic fixture data that simulates actual GitHub API responses
- Tests the complete integration between all components

## Key Testing Patterns

### Mocking

- **Unit tests**: Mock individual dependencies to isolate the code under test
- **Integration tests**: Only mock external dependencies (HTTP requests)

### Parameterization

- Uses `@parameterized.expand` for testing multiple input scenarios
- Uses `@parameterized_class` for class-level parameterization with fixtures

### Test Organization

- Separate test classes for each main class or function group
- Clear naming convention: `TestClassName` for the class being tested
- Descriptive method names that explain what is being tested

### Documentation

- All test classes and methods include docstrings
- Clear explanation of what each test verifies
- Comments explaining complex mock setups

## Running the Tests

```bash
# Run all tests
python -m unittest discover

# Run specific test file
python -m unittest test_utils.py
python -m unittest test_client.py

# Run specific test class
python -m unittest test_utils.TestAccessNestedMap

# Run specific test method
python -m unittest test_utils.TestAccessNestedMap.test_access_nested_map
```

## Dependencies

- `unittest`: Python's built-in testing framework
- `unittest.mock`: For mocking dependencies
- `parameterized`: For parameterized testing
- Custom modules: `utils`, `client`, `fixtures`
