*** Settings ***
Documentation    Test to check if 75% of applications had a lifespan less than 30 seconds
Library          Collections
Library          yaml
Library          OperatingSystem
Library          JSONLibrary

*** Variables ***
${output.yml}    D:\pythonProject\RobotFrameworkExercise\output.yml

*** Test Cases ***
Test Application Lifespan
    ${app_lifetimes}=    Load JSON From File  ./output.json
    ${test1}=  Set Variable  ${app_lifetimes["applications"]}
    ${test2}=  Evaluate  len(${test1})
    ${total_time}=    Set Variable    0
    ${over_30_sec}=    Create List
    FOR    ${app}    IN    ${test1}
        FOR     ${apps2}   IN    ${app}
            ${test3}=  Get From List  ${test1}  3
            #Log To Console  ${apps2}
            ${test4}=  Get From Dictionary  ${test3}   lifespan
            Log To Console  ${test4}

        #${lifespan}=    Set Variable    ${app.get('lifespan', 0)}
        #${total_time}=    Evaluate    ${total_time} + ${lifespan}
        #IF    ${lifespan} > 30
           #Append To List    ${over_30_sec}    ${app.get('name')}
        #END
       END
   END

    #Log To Console    ${test3} This is a test