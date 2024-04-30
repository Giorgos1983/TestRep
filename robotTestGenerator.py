# Automatic generation of robot test file based on the endpoints located in swagger.yaml
# Creation of get request for every endpoint in yaml and checking the returned status code
# python .\robotTestGenerator.py .\swagger.yaml output.robot
# robot .\output.robot

import yaml
import sys


def create_test_cases(swagger_file, output_file):
    try:
        with open(swagger_file, 'r') as file:
            swagger_data = yaml.safe_load(file)
        paths = swagger_data['paths']
    except FileNotFoundError:
        print("Error: The specified swagger file does not exist.")
        sys.exit(1)
    except KeyError:
        print("Error: The swagger file does not contain 'paths'.")
        sys.exit(1)

    try:
        with open(output_file, 'w') as file:
            file.write("*** Settings ***\n")
            file.write("Library           RequestsLibrary\n")
            file.write("Library           Collections\n\n")
            file.write("Suite Setup       Create Session    Swapi    http://localhost:8090\n")
            file.write("Test Setup        Set Test Variable    ${base_url}    http://localhost:8090\n\n")

            file.write("*** Test Cases ***\n")
            for path, methods in paths.items():
                for method in methods:
                    if method == 'get':
                        formatted_path = path.replace('{id}', '1')
                        test_name = formatted_path.replace('/', ' ').strip().title().replace(' ', '_')
                        file.write(f"{test_name}\n")
                        file.write("    [Documentation]    Test GET request for endpoint\n")
                        file.write("    ${response}=    GET On Session    Swapi" f"    {formatted_path}    expected_status=200\n")
                        file.write("    Should Be Equal As Numbers    ${response.status_code}    200\n")
                        file.write("    Log To Console    ${response.json()}\n\n")
    except IOError as e:
        print(f"Error writing to file: {e}")
        sys.exit(1)


def main():
    if len(sys.argv) != 3:
        print("Usage: python generate_robot_tests.py <swagger.yaml> <output.robot>")
        sys.exit(1)

    swagger_file = sys.argv[1]
    output_file = sys.argv[2]
    create_test_cases(swagger_file, output_file)


if __name__ == "__main__":
    main()
