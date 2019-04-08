*** Settings ***
Library  OperatingSystem
Library  Collections

*** Keywords ***
User Wait For ${waiting_time} Seconds
  Sleep   ${waiting_time}

Convert Arguments To Dictionary Values
  [Arguments]  @{args}
  ${return_dictionary} =  Create Dictionary
  ${count} =  Get Length  ${args}
  :FOR  ${INDEX}  IN RANGE   0  ${count}
  \  Set To Dictionary  ${return_dictionary}  key${INDEX}  @{args}[${INDEX}]
  [Return]  ${return_dictionary}
