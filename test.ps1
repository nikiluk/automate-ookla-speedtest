# running with PowerShell 7+
# open powershell in your terminal in this folder and type ".\test"

#options
$outputfile = ".\internetspeed.json" #JSON file where the test results are stored
$testduration = 14 #in days
$interval = 1 #wait and restart after $interval seconds
$numberoftests = $testduration*24*60*60/$interval #calculated based on $testduration and the $interval

#execution
Write-Host "Running test every " $interval "seconds"
Write-Host "Tests to run:" $numberoftests

Write-Host ""
#$OutArray = @()
if (-not(Test-Path -Path $outputfile -PathType Leaf)) {
   "[" | Out-File -FilePath $outputfile -Append -Encoding utf8
}

$failed = 0
for($i = 0; $i -lt $numberoftests; $i++){


    try{
        Write-Host "---"
        Write-Host "Running test #"$($i+1)

        #running speedtest
        $response = .\speedtest --format=json-pretty --unit=Mbps
        $responseObj = $response | ConvertFrom-Json

        if ("result" -eq $responseObj.type) {
            #appeding result to the output file
            $content = Get-Content $outputfile
            $content[-1] = $content[-1].Substring(0,$content[-1].Length-1)+","
            $content | Set-Content $outputfile

            #adjusting JSON formatting
            $response+"]"| Out-File -FilePath $outputfile -Append -Encoding utf8

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



