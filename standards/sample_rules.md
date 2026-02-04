# Company Coding Standards and Best Practices

## Python Code Quality Standards

### 1. Code Style and Formatting

#### PEP 8 Compliance
- **Line Length**: Maximum 88 characters (Black formatter standard)
- **Indentation**: Use 4 spaces per indentation level
- **Imports**: 
  - Group imports in the following order: standard library, third-party, local
  - Use absolute imports when possible
  - One import per line for clarity
- **Naming Conventions**:
  - `snake_case` for functions and variables
  - `PascalCase` for class names
  - `UPPER_CASE` for constants
  - Prefix private methods/attributes with single underscore `_`

#### Example:
```python
# Good
def calculate_total_price(items: list) -> float:
    """Calculate total price of items."""
    return sum(item.price for item in items)

# Bad
def CalculateTotalPrice(items):
    total=0
    for item in items:total+=item.price
    return total
```

### 2. Type Hints and Documentation

#### Type Annotations
- **Required**: All function signatures must include type hints
- Use `typing` module for complex types
- Use `Optional` for nullable parameters
- Use `Union` sparingly; prefer specific types

#### Docstrings
- **Required**: All public functions, classes, and modules
- Use Google-style or NumPy-style docstrings
- Include: description, args, returns, raises

#### Example:
```python
from typing import List, Optional

def process_user_data(
    user_id: int,
    data: dict,
    validate: bool = True
) -> Optional[dict]:
    """
    Process user data with optional validation.
    
    Args:
        user_id: Unique identifier for the user
        data: User data dictionary
        validate: Whether to validate data before processing
        
    Returns:
        Processed data dictionary, or None if validation fails
        
    Raises:
        ValueError: If user_id is invalid
    """
    pass
```

### 3. Error Handling

#### Exception Handling Rules
- **Never** use bare `except:` clauses
- Catch specific exceptions
- Always log exceptions with context
- Use custom exceptions for business logic errors
- Clean up resources with `try-finally` or context managers

#### Example:
```python
# Good
try:
    result = risky_operation()
except ValueError as e:
    logger.error(f"Invalid value in operation: {e}")
    raise
except ConnectionError as e:
    logger.error(f"Connection failed: {e}")
    return None
finally:
    cleanup_resources()

# Bad
try:
    result = risky_operation()
except:
    pass
```

### 4. Security Best Practices

#### Input Validation
- **Always** validate and sanitize user input
- Use parameterized queries for database operations
- Avoid `eval()` and `exec()` with user input
- Validate file uploads (type, size, content)

#### Secrets Management
- **Never** hardcode credentials or API keys
- Use environment variables or secret management services
- Don't commit `.env` files to version control
- Rotate secrets regularly

#### Example:
```python
# Good
import os
from pathlib import Path

API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY environment variable not set")

# Bad
API_KEY = "sk-1234567890abcdef"  # NEVER DO THIS
```

### 5. Performance and Optimization

#### Efficiency Guidelines
- Use list comprehensions over loops when appropriate
- Prefer generators for large datasets
- Use `with` statements for file operations
- Avoid premature optimization
- Profile before optimizing

#### Example:
```python
# Good - Generator for memory efficiency
def process_large_file(filename: str):
    with open(filename, 'r') as f:
        for line in f:
            yield process_line(line)

# Bad - Loads entire file into memory
def process_large_file(filename: str):
    with open(filename, 'r') as f:
        lines = f.readlines()
    return [process_line(line) for line in lines]
```

### 6. Testing Requirements

#### Test Coverage
- **Minimum**: 80% code coverage
- Write unit tests for all public functions
- Include edge cases and error conditions
- Use mocking for external dependencies

#### Test Structure
- Follow AAA pattern: Arrange, Act, Assert
- One assertion per test when possible
- Use descriptive test names

#### Example:
```python
def test_calculate_total_price_with_valid_items():
    # Arrange
    items = [Item(price=10.0), Item(price=20.0)]
    
    # Act
    total = calculate_total_price(items)
    
    # Assert
    assert total == 30.0
```

### 7. Code Organization

#### Module Structure
- Keep modules focused and cohesive
- Maximum 500 lines per module
- Group related functionality
- Use `__init__.py` to expose public API

#### Function Length
- Maximum 50 lines per function
- Extract complex logic into helper functions
- Single Responsibility Principle

### 8. Common Anti-Patterns to Avoid

#### Mutable Default Arguments
```python
# Bad
def add_item(item, items=[]):
    items.append(item)
    return items

# Good
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

#### Global Variables
```python
# Bad
counter = 0

def increment():
    global counter
    counter += 1

# Good
class Counter:
    def __init__(self):
        self.value = 0
    
    def increment(self):
        self.value += 1
```

### 9. Logging Standards

#### Logging Levels
- **DEBUG**: Detailed diagnostic information
- **INFO**: General informational messages
- **WARNING**: Warning messages for potentially harmful situations
- **ERROR**: Error messages for serious problems
- **CRITICAL**: Critical messages for very serious errors

#### Example:
```python
import logging

logger = logging.getLogger(__name__)

def process_data(data):
    logger.info(f"Processing {len(data)} records")
    try:
        result = transform_data(data)
        logger.debug(f"Transformation result: {result}")
        return result
    except Exception as e:
        logger.error(f"Error processing data: {e}", exc_info=True)
        raise
```

### 10. Async/Await Best Practices

#### Asynchronous Code
- Use `async`/`await` for I/O-bound operations
- Don't mix sync and async code unnecessarily
- Use `asyncio.gather()` for concurrent operations
- Handle exceptions in async contexts

#### Example:
```python
import asyncio

async def fetch_data(url: str) -> dict:
    """Fetch data asynchronously."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

async def fetch_multiple(urls: list) -> list:
    """Fetch multiple URLs concurrently."""
    tasks = [fetch_data(url) for url in urls]
    return await asyncio.gather(*tasks)
```

---

## Review Checklist

When reviewing code, ensure:
- [ ] Code follows PEP 8 style guidelines
- [ ] All functions have type hints and docstrings
- [ ] Proper error handling with specific exceptions
- [ ] No hardcoded secrets or credentials
- [ ] Input validation is present
- [ ] Tests are included with good coverage
- [ ] No common anti-patterns
- [ ] Logging is appropriate
- [ ] Code is readable and maintainable
- [ ] Performance considerations are addressed
