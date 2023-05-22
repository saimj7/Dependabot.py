# Dependabot.py
To easily check Python dependency conflicts/security vulnerabilities.

> NOTE: This is a simple ```Python only``` dependabot inspired by GitHub <a href="https://github.com/dependabot" target="_blank">Dependabot</a>

- Python package dependency conflicts and security vulnerabilities are easy to miss.
- The primary aim here is to integrate several Python libraries that look for them.
- E.g., pip, pipdeptree, safety, bandit etc., are considered for now.
- This can be further used in CI or whereever you would like it automated.

--- 

## Table of Contents

* [Install the dependencies](#install-the-dependencies)
* [Features](#features)
    - [Dependency conflicts](#dependency-conflicts)
    - [Security vulnerabilities](#security-vulnerabilities)
    - [Dependency tree](#dependency-tree)
    - [Script vulnerabilities](#script-vulnerabilities)
* [References](#references)

---

## Install the dependencies

First up, install all the required Python dependencies by running: ```
pip install -r requirements.txt ```

> NOTE: Supported Python version is 3.11.3 (there can always be version conflicts between the dependencies, OS, hardware etc.).

Then head into the source directory and run ```python dependabot.py```

---

## Features

The following features can be easily enabled/disabled in ```utils/config.json```:

```json
{
    "Dep_Conflicts": true,
    "Check_Vulnerabilities": true,
    "Dep_Tree": true,
    "Bandit_Vulnerabilities": true
}
```

### Dependency conflicts

We use pip's ```pip check``` command to check for potential issues or inconsistencies in installed Python packages. It involves:

- Verifying installed packages against their metadeta which ensures that the installed packages are in a consistent state and are compatible with the current environment.
- Checking for inconsistent dependencies to identify situations where different packages require conflicting versions of the same dependency.
- Validating package metadata of installed packages, including information like name, version, and dependencies. This ensures that the package metadata is correctly formatted and complies with the standards.
- To run it, simply enable ```"Dep_Conflicts": true``` in ```utils/config.json```.

Example output (enforced a conflict):

```cmd
[INFO] Dependency Conflicts:
[INFO] bandit 1.7.5 has requirement colorama>=0.3.9; platform_system == "Windows", but you have colorama 0.3.6.
```

### Security vulnerabilities

We use safety's ```safety check``` command to check for known security vulnerabilities in installed Python packages, ensuring the security of your Python environment. It is particularly useful when working with third-party packages or dependencies to stay informed about any known vulnerabilities and take appropriate actions to mitigate the risks. It involves:

- Security vulnerability database: It compares the versions of installed packages against a security vulnerability database, such as the National Vulnerability Database (NVD), to identify any known vulnerabilities.
- Checking if any installed packages have known vulnerabilities or have been associated with security advisories.
- Providing information about the identified vulnerabilities, including the severity level, the affected package versions, and links to additional resources or advisories.

- To run it, simply enable ```"Check_Vulnerabilities": true``` in ```utils/config.json```.

Example output (enforced a conflict):

```cmd
[INFO] Security Vulnerabilities:

Package: Pillow
Installed version: 8.3.1
Latest version: 8.4.0
Status: No known vulnerabilities found.

Package: flask
Installed version: 2.1.0
Latest version: 2.1.1
Status: Vulnerability found! Check the security advisory for more information:
        Advisory: https://example.com/security-advisory/flask-vulnerability
```

### Dependency tree

We use ```pipdeptree``` to generate a tree-like representation of the installed Python packages and their dependencies. 

- It analyzes the installed packages by inspecting their metadata and determines the package dependencies. It then generates a tree structure that shows the relationship between the packages, with the root package at the top and its dependencies branching out below.
- It helps us understand which packages are installed, their versions, and how they are interconnected. This information can be useful for managing package versions, identifying conflicting dependencies, or troubleshooting issues related to package compatibility.

Example output (enforced a conflict):

```cmd
Warning!!! Possibly conflicting dependencies found:
* bandit==1.7.5
 - colorama [required: >=0.3.9, installed: 0.3.6]
------------------------------------------------------------------------
argparse==1.4.0
bandit==1.7.5
  - colorama [required: >=0.3.9, installed: 0.3.6]
  - GitPython [required: >=1.0.1, installed: 3.1.31]
    - gitdb [required: >=4.0.1,<5, installed: 4.0.10]
      - smmap [required: >=3.0.1,<6, installed: 5.0.0]
```
```json
[INFO] Dependency Tree:
[INFO] [
    {
        "package": {
            "key": "argparse",
            "package_name": "argparse",
            "installed_version": "1.4.0"
        },
        "dependencies": []
    },
    {
        "package": {
            "key": "bandit",
            "package_name": "bandit",
            "installed_version": "1.7.5"
        },
        "dependencies": [
            {
                "key": "colorama",
                "package_name": "colorama",
                "installed_version": "0.3.6",
                "required_version": ">=0.3.9"
            },
            {
                "key": "gitpython",
                "package_name": "GitPython",
                "installed_version": "3.1.31",
                "required_version": ">=1.0.1"
            }]
```

### Script vulnerabilities

Last but not the least, I thought it is also important to perform a static code analysis of our main script (dependabot.py), so we use ```safety```. It analyzes our codebase and checks for potential security vulnerabilities and weaknesses by performing static code analysis (applies a set of predefined security rules to identify potential vulnerabilities). It scans for issues such as:

```
1. Use of insecure cryptographic algorithms
2. SQL injection vulnerabilities
3. Use of dangerous functions or modules
4. Insecure random number generation
5. Cross-Site Scripting (XSS) vulnerabilities
6. Code injection vulnerabilities
7. Insecure file permissions
8. Hardcoded sensitive information like passwords or API keys
9. Use of unsafe or deprecated modules or functions
```

Example output on dependabot.py:

```cmd
>> Issue: [B603:subprocess_without_shell_equals_true] subprocess call - check for execution of untrusted input.
   Severity: Low   Confidence: High
   CWE: CWE-78 (https://cwe.mitre.org/data/definitions/78.html)
   More Info: https://bandit.readthedocs.io/en/1.7.5/plugins/b603_subprocess_without_shell_equals_true.html
   Location: dependabot.py:77:20
76          # Run bandit command to check for security vulnerabilities
77          bandit_result = subprocess.run(['bandit', '-r', dep_script_dir], capture_output=True, text=True)
78          bandit_output = bandit_result.stdout

--------------------------------------------------

Code scanned:
        Total lines of code: 69
        Total lines skipped (#nosec): 0

Run metrics:
        Total issues (by severity):
                Undefined: 0
                Low: 11
                Medium: 0
                High: 0
        Total issues (by confidence):
                Undefined: 0
                Low: 0
                Medium: 0
                High: 11
Files skipped (0):
```

> NOTE: By regularly running bandit as part of our development or CI/CD process, we can proactively detect and address security vulnerabilities in our Python applications, improving the overall security posture of our software.

---

## References

- pip check: https://pypi.org/project/pip-check/
- safety check: https://pypi.org/project/safety/
- pipdeptree: https://pypi.org/project/pipdeptree/
- bandit: https://pypi.org/project/bandit/

---

*saimj7 / 22-05-2023 - ©<a href="http://saimj7.github.io" target="_blank">Sai_Mj</a>*
