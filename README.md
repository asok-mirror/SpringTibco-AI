# Tibco to Java Migration Tool

This project provides a tool to assist in migrating Tibco BusinessWorks projects to Java Spring Boot applications. It leverages large language models (LLMs) to analyze Tibco projects and generate corresponding Java code.

## Prerequisites

*   Python 3.12+
*   Poetry (for dependency management)
*   A Gemini API Key (configured in your environment variables)
*   Optional: Windows Subsystem for Linux (WSL) (if running on Windows)
*   Use Conda or Venv for managing Python environments

## Installation

1.  Clone the repository:

    ```bash
    git clone <repository_url>
    cd tibco-to-java
    ```

2.  Install dependencies using Poetry:

    ```bash
    poetry install
    ```

## Configuration

1.  **API Keys:** Set the following environment variables:

    *   `GEMINI_API_KEY`: Your Gemini API key.

    ```bash
    export GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
    ```

    or

    * **Configure Environment**: Use `.env.example` to create `.env` file and set up the environment variables for [Gemini](https://aistudio.google.com/apikey)

2.  **WSL (Windows only):** Ensure that WSL is installed and configured correctly.

## Usage

1.  **Run the migration tool:**

    ```bash
    poetry run tibco_to_java
    ```

    This will:

    *   Analyze the Tibco project (defined in [tibco_credit_maintanence_project.txt](http://_vscodecontentref_/0)).
    *   Generate a Java Spring Boot project in the `outputs/springBootProject` directory.
    *   Create a `bash_script.sh` file in the `outputs/springBootProject` directory containing the commands to set up the project.
    *   Navigate to above folder and manually execute the `bash_script.sh` file using WSL (on Windows) or bash (on Linux/macOS).

2.  **Run the generated Spring Boot application:**

    Navigate to the `outputs/springBootProject` directory and execute the following commands:

    ```bash
    cd outputs/springBootProject
    ./bash_script.sh
    ```

    This will create the Spring Boot project.

    ## License
    This project is released under the MIT License.
