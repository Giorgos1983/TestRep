*** Settings ***
Library    RequestsLibrary
Library    Process
Library    Collections
Library    OperatingSystem


Suite Setup       Start server
Suite Teardown    Stop server
Test Setup        Create Session    Swapi    http://localhost:8090

*** Test Cases ***
Person Happy Path
    [Documentation]    Verify that an existing person can be retrieved
    [Tags]    functional
    ${resp}=    GET On Session    Swapi    /people/1/       expected_status=200
    ${json}=    Set Variable    ${resp.json()}
    Should Be Equal As Strings    ${json['name']}    Luke Skywalker

Person Not Found
    [Documentation]    Verify that a non-existent person returns a 404 error
    [Tags]    functional
    ${resp}=    GET On Session    Swapi    /people/101/     expected_status=404
    ${json}=    Set Variable    ${resp.json()}
    Dictionary Should Contain Value    ${json}    404 Not Found: people with ID 101 not found

Planet Happy Path
    [Documentation]    Verify that an existing planet can be retrieved
    [Tags]    functional
    ${resp}=    GET On Session    Swapi    /planets/1/       expected_status=200
    ${json}=    Set Variable    ${resp.json()}
    Should Be Equal As Strings    ${json['name']}    Tatooine

Planet Not Found
    [Documentation]    Verify that a non-existent planet returns a 404 error
    [Tags]    functional
    ${resp}=    GET On Session    Swapi    /planets/101/     expected_status=404
    ${json}=    Set Variable    ${resp.json()}
    Dictionary Should Contain Value    ${json}    404 Not Found: planets with ID 101 not found

Starship Happy Path
    [Documentation]    Verify that an existing starship can be retrieved
    [Tags]    functional
    ${resp}=    GET On Session    Swapi    /starships/1/       expected_status=200
    ${json}=    Set Variable    ${resp.json()}
    Should Be Equal As Strings    ${json['name']}    X-wing

Starship Not Found
    [Documentation]    Verify that a non-existent starship returns a 404 error
    [Tags]    functional
    ${resp}=    GET On Session    Swapi    /starships/101/     expected_status=404
    ${json}=    Set Variable    ${resp.json()}
    Dictionary Should Contain Value    ${json}    404 Not Found: starships with ID 101 not found

*** Keywords ***
Start server
    ${server_path}=    Join Path    ${CURDIR}    ../server/server.py
    Start Process    python    ${server_path}
    Sleep    2s

Stop server
    Terminate All Processes