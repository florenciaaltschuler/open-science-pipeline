from utils import validate_project

if __name__ == "__main__":
    project_name = input("Enter the project path to validate: ").strip()
    validate_project(project_name)