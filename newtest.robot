*** Settings ***
Library     OperatingSystem
Library     Collections
Library     JSONLibrary

*** Variables ***
${INPUT_FILE}   logcat_file.txt
${WARNING_TIME}    30

*** Test Cases ***
Verify Lifespan of Applications
    [Documentation]     Verify that 75% of the applications have a lifespan less than 30 seconds
    [Tags]              lifespan
    ${json_data}=        Load JSON From File  ./output.json
    ${app_list}=        Set Variable    ${json_data["applications"]}
    ${total_apps}=      Get Length  ${app_list}
    ${short_lifespan_apps}=    Create List
    ${long_lifespan_apps}=     Create List
    FOR     ${app_dict}      IN      @{app_list}
        Log To Console    ${app_dict}
        ${app_name}=        Get From Dictionary     ${app_dict}     app_path
        ${app_data}=        Get From Dictionary     ${app_dict}     lifespan
        #${lifespan}=        Convert To Number   ${app_data["lifespan"][:-1]}    # remove "s" from lifespan value
        IF      ${app_data} < ${WARNING_TIME}
            Append To List  ${short_lifespan_apps}     ${app_name}
        ELSE
            Append To List  ${long_lifespan_apps}      ${app_name}
        END
    END

    Log To Console    ${long_lifespan_apps} Apps with a lifespan > 30

    ${num_short_lifespan_apps}=     Get Length  ${short_lifespan_apps}
    ${num_long_lifespan_apps}=      Get Length  ${long_lifespan_apps}
    ${num_passed}=      Evaluate    int(round(${num_short_lifespan_apps} / ${total_apps} * 100)) >= 75
    Run Keyword If       ${num_passed}    Log To Console  TC PASSED: 75% of applications had a lifespan less than ${WARNING_TIME} seconds.
    ...                 ELSE    Fail    TC FAILED: less than 75% of applications had a lifespan less than ${WARNING_TIME} seconds.
    ...                 Warn If     ${num_long_lifespan_apps} > 0     ${num_long_lifespan_apps}
