import sys
from tibco_to_java.crew import TibcoToJavaCrew, JavaSpringBoot
from pathlib import Path
import os, json, subprocess


def run():
    try:
        # Get crew output
        crew_output = TibcoToJavaCrew().crew().kickoff()
        #crew_output = get_dummy_output()  # For testing

        # Handle different output formats
        if isinstance(crew_output, str):
            try:
                crew_output = json.loads(crew_output)
            except json.JSONDecodeError:
                crew_output = {"bash": crew_output}

        # Create model instance with properly formatted input
        java_spring_boot = JavaSpringBoot(bash=crew_output["bash"])

        # Create output directory
        output_dir = Path("outputs")
        output_dir.mkdir(exist_ok=True)

        # Create springBootProject directory inside outputs
        spring_boot_dir = output_dir / "springBootProject"
        spring_boot_dir.mkdir(exist_ok=True)

        # Write bash script to the springBootProject directory
        bash_file = spring_boot_dir / "bash_script.sh"
        bash_file.write_text(java_spring_boot.bash, encoding="utf-8")
        if os.name != "nt":  # Not Windows
            bash_file.chmod(bash_file.stat().st_mode | 0o755)

        # # Write feedback JSON
        # feedback_file = output_dir / "feedback.json"
        # feedback_file.write_text(java_spring_boot.feedback, encoding='utf-8')

        print(f"Files created successfully in {output_dir.absolute()}")

        # # Execute bash script
        # try:
        #     if os.name == "nt":
        #         # Windows: Use WSL bash
        #         command = ["wsl", "bash", "bash_script.sh"] 
        #     else:
        #         # Linux/macOS: Execute directly with bash
        #         command = ["bash", "bash_script.sh"]

        #     process = subprocess.Popen(
        #         command,
        #         cwd=str(spring_boot_dir.absolute()),
        #         stdout=subprocess.PIPE,
        #         stderr=subprocess.PIPE,
        #     )
        #     stdout, stderr = process.communicate()

        #     print("Bash script output:\n", stdout.decode())
        #     if stderr:
        #         print("Bash script errors:\n", stderr.decode())
        #     if process.returncode != 0:
        #         print(f"Bash script failed with return code: {process.returncode}")

        # except FileNotFoundError:
        #     print("WSL not found. Please install WSL and ensure bash is available.")
        #     return False  # Indicate failure
        # except Exception as e:
        #     print(f"Error executing bash script: {e}")
        #     return False #Indicate failure

        return True

    except KeyError as e:
        raise ValueError(f"Missing required field in crew output: {e}")
    except Exception as e:
        raise IOError(f"Error processing output: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """

    try:
        TibcoToJavaCrew().crew().train(n_iterations=int(sys.argv[1]))

    except Exception as e:
        raise RuntimeError(f"An error occurred while training the crew: {e}")


def get_dummy_output():
    """Returns dummy output for testing purposes"""
    return {
        "bash": """#!/bin/bash
            # Create Spring Boot project structure
            mkdir -p myapp/src/main/java/com/example/demo
            cd myapp || exit

            # Initialize Spring Boot project
            echo 'Creating Spring Boot project...'""",
        "feedback": """{
                "status": "success",
                "message": "Spring Boot project structure created successfully",
                "details": {
                    "projectName": "demo 1",
                    "springBootVersion": "2.7.0",
                    "javaVersion": "11"
                }
            }""",
    }
