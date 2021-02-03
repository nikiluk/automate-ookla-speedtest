# running with PowerShell 7+
# open powershell in your terminal in this folder and type ".\test"
$outputfile = ".\internetspeed.json"
$interval = 5 #every x seconds
$numberoftests = 86400/$interval

Write-Host "Running test every " $interval "seconds"

for($i = 0; $i -lt $numberoftests; $i++){
    Write-Host "Running test #"$i
    .\speedtest --format=json-pretty --unit=Mbps| Out-File -FilePath $outputfile -Append -Encoding utf8
    ","| Out-File -FilePath $outputfile -Append -Encoding utf8
    Write-Host "Test #" $i" completed"
    Start-Sleep -Seconds $interval
}

Write-Host "Total tests:" $i

