$CodeRootfolder= "C:\Users\demo\PycharmProjects\Modular pythonProject\"


$GlobLWSSO_COOKIE_KEY=""
$ClientIdKey='I_KEY_74cd7d5d-cec6-4f30-8e41-29d5b8bbd2b5'
$ClientSecretKey='S_KEY_f240c524-d2b4-4cf9-991a-3394a5ec4a53'
#Write-Host "LWSSO cookie key:"$LWSSO_COOKIE_KEY


function Authenticate{
param(
    [string]$ClientIdKey,
    [string]$ClientSecretKey
)

python $CodeRootfolder"Authenticate.py" -ClientIdKey $ClientIdKey -ClientSecretKey $ClientSecretKey | ConvertFrom-Json
}

function RunTest{
    param (
        [string]$post_run_action = "Collate And Analyze", # Default value
        [string]$test_id = "177",                         # Default value
        [string]$test_instance_id = "8",                  # Default value
        [int]$hours = 1,                                  # Default value
        [int]$minutes = 30,                               # Default value
        [bool]$vuds_mode = $false,                        # Default value
        [string]$LWSSO_COOKIE_KEY= "IFdzNFM09vmSNtS9WVz2H9NtUE9-JmTyGCnqdqroQcYtz1vFKIbplE2DA4ny6WEOm162hXbA7FI6oh6nEsARTe0rHBRk6yGfTRob_C4yQKXxI4IbXpNfg0du0_RvVv4J2UfxpxmQmM_hshGiKkOJGGOWijz94-FlK1dZ0MZYw06MDvCfMkvsDfCiG0luEJubGTHDBylc7IuJlEXk-2JTdVOh-BA741WjYdL5AUr0t84."                        # Default value
    )
    python $CodeRootfolder"RunTest.py" -testid $test_id -testinstanceid $test_instance_id -LWSSO_COOKIE_KEY $GlobLWSSO_COOKIE_KEY| ConvertFrom-Json
}

function monitor_run_status{
param
([string]$run_id, [int]$wait_seconds, [int]$max_attempts, [string]$LWSSO_COOKIE_KEY)
python $CodeRootfolder"MonitorRrunStatus.py" -run_id $run_id -wait_seconds $wait_seconds -max_attempts $max_attempts -LWSSO_COOKIE_KEY $LWSSO_COOKIE_KEY

}

function CheckRunSLAStatusById{
param
([string]$run_id, [string]$LWSSO_COOKIE_KEY)
python $CodeRootfolder"CheckRunSLAStatusbyId.py" -run_id $run_id -LWSSO_COOKIE_KEY $LWSSO_COOKIE_KEY

}

Write-Host "Authenitcating..."
$AuthResponse = Authenticate -ClientIdKey $ClientIdKey -ClientSecretKey $ClientSecretKey
if($AuthResponse.StatusCode -eq 200){
    Write-Host "Authentication Sucess!"
    $GlobLWSSO_COOKIE_KEY = $AuthResponse.LWSSO_COOKIE_KEY
}
else {
    Write-Host "Authentication Failed. Status Code: $($AuthResponse.StatusCode)"
    exit 1
  
}

Write-Host "Trying to run test..."
$RunTestResponse = RunTest -LWSSO_COOKIE_KEY $GlobLWSSO_COOKIE_KEY
if($RunTestResponse.StatusCode -eq 201){
    Write-Host "Test run initiated Sucessfully!"
    $TestRunId = $RunTestResponse.RunId
    Write-Host "Test Run Id: "$TestRunId
}
else {
    Write-Host "Run Test Failed. Status Code: $($RunTestResponse.StatusCode)"
    exit 1
  
}

Write-Host("Please wait while the test run is in progress. This process might take a while...!")
Start-Sleep -Seconds 30  # Waits for 30 seconds for test run entity
$TestMonitorResponse = monitor_run_status -run_id $TestRunId -wait_seconds 10 -max_attempts 200 -LWSSO_COOKIE_KEY $GlobLWSSO_COOKIE_KEY

if ($TestMonitorResponse -eq "Finished") {
    $TestSLAResponse = CheckRunSLAStatusById -run_id $TestRunId -LWSSO_COOKIE_KEY $GlobLWSSO_COOKIE_KEY
    if ($TestSLAResponse -eq "Passed"){
        Write-Host "Happy days! Test finished, SLA Result is:"
        Write-Host "Passed" -ForegroundColor Green
    }
    else{
    Write-Host "Test finished! SLA Result: "
    Write-Host $TestSLAResponse -ForegroundColor Red
    
    }
} else{
    Write-Host "Something Went wrong!"
    exit 1
}

