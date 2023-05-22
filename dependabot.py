import subprocess
import logging
import json
import os


# Setup logger
logging.basicConfig(level=logging.INFO, format="[INFO] %(message)s")
logger = logging.getLogger(__name__)

# Load the configuration
with open("utils/config.json", "r") as file:
    config = json.load(file)


def pip_packages():
    # Get a list of installed packages
    find_packages = subprocess.run(
        ["pip", "list", "--format", "json"], capture_output=True, text=True
    )
    installed_packages = json.loads(find_packages.stdout)
    return installed_packages


def dep_conflicts():
    # Check for dependency conflicts
    dependency_conflicts = subprocess.run(
        ["pip", "check"], capture_output=True, text=True
    )
    # Print the conflicts
    logger.info("Dependency Conflicts:")
    if dependency_conflicts.returncode != 0:
        logger.info(dependency_conflicts.stdout)
    else:
        logger.info("No dependency Conflicts")


def check_vulnerabilities(py_packages):
    # Check for security vulnerabilities
    vulnerabilities_data = []
    for package in py_packages:
        package_name = package["name"]
        try:
            safety_check = subprocess.run(
                ["safety", "check", "-r", package_name, "--json"],
                capture_output=True,
                text=True,
            )
            if safety_check.stdout:
                vulnerabilities = json.loads(safety_check.stdout)
                vulnerabilities_data += vulnerabilities
                logger.info(vulnerabilities_data)
        except (subprocess.CalledProcessError, json.JSONDecodeError):
            pass

    # Print the vulnerabilities
    logger.info("\nSecurity Vulnerabilities:")
    if vulnerabilities_data:
        for vulnerability in vulnerabilities_data:
            logger.info(
                f"- {vulnerability['advisory_id']}: {vulnerability['vulnerable_package']} ({vulnerability['installed_version']})"
            )
    else:
        logger.info("No security vulnerabilities")


def dep_tree():
    # Run pipdeptree command to get dependency tree
    pipdeptree_result = subprocess.run(
        ["pipdeptree", "--json"], capture_output=True, text=True
    )
    pipdeptree_output = pipdeptree_result.stdout

    # Parse the dependency tree JSON if it's not empty
    dependency_tree = {}
    if pipdeptree_output:
        try:
            dependency_tree = json.loads(pipdeptree_output)
        except json.JSONDecodeError:
            logger.info("Error: Failed to parse dependency tree JSON")

    # Print the dependency tree
    logger.info("\nDependency Tree:")
    logger.info(json.dumps(dependency_tree, indent=4))


def script_vulnerabilities(dep_script_dir):
    # Run bandit command to check for security vulnerabilities
    bandit_result = subprocess.run(
        ["bandit", "-r", dep_script_dir], capture_output=True, text=True
    )
    bandit_output = bandit_result.stdout

    # Print the bandit results
    if bandit_output:
        logger.info("\nBandit Results:")
        logger.info(bandit_output)
    else:
        logger.info("No bandit results")


def dependabot():
    # Main function for dependabot.py
    py_packages = pip_packages()
    if config["Dep_Conflicts"]:
        conflicts = dep_conflicts()
    if config["Check_Vulnerabilities"]:
        vulnerabilites = check_vulnerabilities(py_packages)
    if config["Dep_Tree"]:
        dependency_tree = dep_tree()
    if config["Bandit_Vulnerabilities"]:
        script_dir = f"{os.getcwd()}\dependabot.py"
        script_vul = script_vulnerabilities(script_dir)


if __name__ == "__main__":
    dependabot()
