import sys
from tibco_to_java.crew import TibcoToJavaCrew, JavaSpringBoot
from pathlib import Path
import os

def run():
    output = TibcoToJavaCrew().crew().kickoff()
    #output = get_dummy_output() #//testing purposes

    java_spring_boot = JavaSpringBoot(bash=output["bash"], feedback=output["feedback"])

    try:
        output_dir = Path("outputs")
        output_dir.mkdir(exist_ok=True)

        # Write bash script with executable permissions on Unix
        bash_file = output_dir / "bash_script.sh"
        bash_file.write_text(java_spring_boot.bash, encoding='utf-8')
        # Make the script executable on Unix systems
        if os.name != 'nt':  # Not Windows
            bash_file.chmod(bash_file.stat().st_mode | 0o755)

        # Write feedback as formatted JSON
        feedback_file = output_dir / "feedback.json"
        feedback_file.write_text(java_spring_boot.feedback, encoding='utf-8')
        
    except Exception as e:
        raise IOError(f"Error writing output files: {e}")


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
            }"""
    }
