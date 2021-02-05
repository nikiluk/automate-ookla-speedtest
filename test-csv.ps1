# running with PowerShell 7+
# open powershell in your terminal in this folder and type ".\test"

#options
$outputfile = ".\internetspeed.csv" #CSV file where the test results are stored
$testduration = 14 #in days
$interval = 1 #wait and restart after $interval seconds
$numberoftests = $testduration*24*60*60/$interval #calculated based on $testduration and the $interval

#execution
Write-Host "Running test every " $interval "seconds"
Write-Host "Tests to run:" $numberoftests
Write-Host "Writing test results to a file:"$outputfile


Write-Host ""
#$OutArray = @()
if (-not(Test-Path -Path $outputfile -PathType Leaf)) {
    #write headers on first launch
    $content = Get-Content ".\src\templates\headers.csv.tpl"
    $content | Set-Content $outputfile
}

$failed = 0
for($i = 0; $i -lt $numberoftests; $i++){


    try{
        Write-Host "---"
        Write-Host "Running test #"$($i+1)

        #running speedtest
        $response = .\speedtest --format=csv --unit=Mbps
        #$responseObj = $response | ConvertFrom-Json

        if ($response -Match "result") {

            #adjusting JSON formatting
            $response | Out-File -FilePath $outputfile -Append -Encoding utf8

            Write-Host "Test #"$($i+1)"completed"
        }
        else {
            Write-Error "Error"
            $failed+=1
        }

        
     }
     catch{
        #catch error
     }
    Write-Host "Total tests:" $($i+1) "(failed" $failed")"
    Write-Host "---"
    Write-Host ""

    Start-Sleep -Seconds $interval

}



