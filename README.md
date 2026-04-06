# OrangeHRM Login Automation Framework

A robust Selenium-based test automation framework for testing the [OrangeHRM demo site](https://opensource-demo.orangehrmlive.com/). Built with Java, TestNG, and Allure reporting.

## Features

- **Page Object Model (POM)** - Clean separation of page elements and test logic
- **Thread-Safe WebDriver** - `ThreadLocal` support for parallel test execution
- **TestNG Integration** - Advanced test configuration with data providers
- **Allure Reporting** - Beautiful, detailed test reports with steps and attachments
- **Configurable** - Properties-based configuration for environments
- **Data-Driven Testing** - Support for multiple data sources
- **AssertJ Fluent Assertions** - Readable, expressive assertions
- **CI/CD Ready** - Maven-based build and execution

## Project Structure

```
.
├── pom.xml
├── src/main/java/com/orangehrm/
│   ├── base/
│   │   └── BaseTest.java          # Base class with setup/teardown
│   ├── config/
│   │   └── Constants.java         # Shared constants and tags
│   ├── driver/
│   │   └── DriverManager.java     # Thread-safe WebDriver management
│   ├── pages/
│   │   └── LoginPage.java         # Page Object for login page
│   └── utils/
│       └── ConfigReader.java      # Properties file reader
├── src/test/java/com/orangehrm/tests/
│   ├── LoginTests.java            # Main login test suite with 10 test cases
│   └── DataDrivenLoginTests.java  # Data-driven tests with various scenarios
└── src/test/resources/
    ├── config.properties          # Configuration (URL, credentials, timeouts)
    ├── testng.xml                 # TestNG suite configuration
    └── allure.properties         # Allure reporter configuration
```

## Prerequisites

- **Java 8 or higher**
- **Maven 3.6+**
- **Chrome Browser** (for local execution)
- **Docker** (optional, for Selenoid grid execution)

## Setup & Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd seleniumOrange
   ```

2. **Verify Maven dependencies**
   ```bash
   mvn clean compile
   ```

3. **Update configuration** (optional)
   Edit `src/test/resources/config.properties`:
   ```properties
   base.url=https://opensource-demo.orangehrmlive.com/web/index.php/auth/login
   browser=chrome
   # Change credentials if needed
   username=Admin
   password=admin123
   ```

## Running Tests

### Run all tests
```bash
mvn test -Dsurefire.suiteXmlFiles=testng.xml
```

### Run specific test class
```bash
mvn test -Dsurefire.suiteXmlFiles=testng.xml -Dtest=LoginTests
```

### Run data-driven tests only
```bash
mvn test -Dsurefire.suiteXmlFiles=testng.xml -Dtest=DataDrivenLoginTests
```

### Run in parallel (increase thread count)
Edit `pom.xml` -> `maven-surefire-plugin` -> `<threadCount>3</threadCount>`

### Run with specific browser
In `config.properties`, change:
```properties
browser=chrome   # or add support for firefox, edge
```

## Generating Allure Reports

### After test execution, generate HTML report:
```bash
mvn allure:serve
```
or standalone:
```bash
allure serve target/allure-results
```

This opens a local server with interactive test results.

### Report Features
- Test execution timeline
- Step-by-step Allure steps
- Categories (passed/failed/broken/skipped)
- Environment properties
- Attachments (screenshots, logs)

## Test Cases Included

### LoginTests
1. **testSuccessfulLogin** - Valid credentials (Smoke test)
2. **testLoginWithInvalidUsername** - Invalid username
3. **testLoginWithInvalidPassword** - Invalid password
4. **testLoginWithBothInvalidCredentials** - Both credentials invalid
5. **testLoginWithEmptyUsername** - Missing username
6. **testLoginWithEmptyPassword** - Missing password
7. **testLoginWithBothEmptyFields** - Both fields empty
8. **testLoginPageElements** - UI elements verification
9. **testLoginWithSpacesInUsername** - Whitespace handling
10. **testLogoutFlow** - Logout verification

### DataDrivenLoginTests
- Invalid credential combinations
- Edge case variations (case sensitivity)
- Special character injection tests

## Configuration

### `config.properties`

| Key | Description | Default |
|-----|-------------|---------|
| base.url | Base URL of the application | OrangeHRM demo |
| browser | Browser to run tests on | chrome |
| username | Default username for testing | Admin |
| password | Password for testing | admin123 |
| implicit.wait | Implicit wait time (seconds) | 15 |
| explicit.wait | Explicit wait time (seconds) | 20 |
| headless | Run browser in headless mode | false |
| screenshot.dir | Screenshots directory | target/screenshots |

### `testng.xml`

Configure test suites, groups, and parallel execution:
- Defines which test classes to run
- Sets parallel execution (methods/classes/tests)
- Can be customized for different test runs

## Framework Patterns

### Thread Safety
- `DriverManager` uses `ThreadLocal<WebDriver>`
- Each test thread gets its own WebDriver instance
- No interference between parallel tests

### Page Object Model
```java
LoginPage loginPage = new LoginPage(driver);
loginPage.login(username, password);
```

### Allure Annotations
- `@Epic` / `@Feature` / `@Story` - Organize tests hierarchically
- `@Step` - Document action steps in reports
- `@Severity` - Priority levels (BLOCKER, CRITICAL, NORMAL, MINOR, TRIVIAL)

## Extending the Framework

### Adding a New Page
1. Create class in `src/main/java/com/orangehrm/pages/`
2. Use `@FindBy` for locators
3. Initialize with `PageFactory.initElements(driver, this)`

### Adding a New Test
1. Create class in `src/test/java/com/orangehrm/tests/`
2. Extend `BaseTest`
3. Add TestNG methods with `@Test`
4. (Optional) Use Allure annotations for better reporting

### Adding Data-Driven Tests
- Use `@DataProvider` to supply test data
- Reference with `dataProvider = "name"` in `@Test`

## CI/CD Integration

### GitHub Actions Example
```yaml
- name: Run tests
  run: mvn test -Dsurefire.suiteXmlFiles=testng.xml
- name: Generate Allure Report
  run: mvn allure:report
```

### Jenkins Pipeline
```groovy
stage('Test') {
    steps {
        sh 'mvn clean test -Dsurefire.suiteXmlFiles=testng.xml'
    }
}
stage('Report') {
    steps {
        allure includeProperties: false, jdk: '11', results: [[path: 'target/allure-results']]
    }
}
```

## Troubleshooting

**Tests fail with "Session not created"**
- Chrome and ChromeDriver version mismatch
- Solution: Update ChromeDriver or use WebDriverManager

**OutOfMemoryError**
- Increase threadCount gradually
- Add JVM args: `mvn test -Xmx2g`

**Allure report empty**
- Ensure `allure-results` directory exists and contains JSON files
- Run `mvn allure:report` to generate report

## Future Enhancements

- [ ] Selenoid Docker Grid integration
- [ ] Excel-based data provider
- [ ] Retry analyzer for flaky tests
- [ ] Custom logger with Log4j/SLF4J
- [ ] Screenshot on failure
- [ ] Email report notifications
- [ ] API testing module
- [ ] Database validation utilities

## Contributing

1. Follow existing coding standards
2. Write tests for new functionality
3. Update Allure tags appropriately
4. Ensure all tests pass before committing

## License

[Include your license here]
