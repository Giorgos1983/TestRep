*** Settings ***
Library           RequestsLibrary
Library           Collections
Library           OperatingSystem
Library     Process
Suite Setup       Start server
Suite Teardown    Stop server
Test Setup        Create Session    Swapi    http://localhost:8090

*** Test Cases ***

Performance Test
    [Documentation]    Measures the response time for accessing an endpoint continuously
    [Tags]    performance

    ${start_time}=    Get Time    epoch
    ${end_time}=    Evaluate    ${start_time} + 60  # Run the test for 60 seconds
    @{response_times}=    Create List

    FOR    ${current_time}    IN RANGE    ${start_time}    ${end_time}
        ${start_request_time}=    Get Time    epoch
        ${response}    GET On Session    Swapi    /people/1/
        ${end_request_time}=    Get Time    epoch
        ${response_time}=    Evaluate    ${end_request_time} - ${start_request_time}
        Append To List    ${response_times}    ${response_time}
    END
    Calculate Mean And Standard Deviation    @{response_times}

*** Keywords ***
Start server
    ${server_path}=    Join Path    ${CURDIR}    ../server/server.py
    Start Process    python    ${server_path}
    Sleep    2s

Stop server
    Terminate All Processes

Calculate Mean And Standard Deviation
    [Arguments]    @{response_times}
    ${mean}=    Evaluate    sum(${response_times}) / len(${response_times})
    @{squared_differences}=    Create List
    FOR    ${response_time}    IN    @{response_times}
        ${difference}=    Evaluate    ${response_time} - ${mean}
        ${squared_difference}=    Evaluate    ${difference} ** 2
        Append To List    ${squared_differences}    ${squared_difference}
    END
    ${variance}=    Evaluate    sum(${squared_differences}) / len(${squared_differences})
    ${std_dev}=    Evaluate    ${variance} ** 0.5
    Log    Mean response time: ${mean}s
    Log    Standard deviation: ${std_dev}s