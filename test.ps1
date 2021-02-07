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
Write-Host "Writing test results to a file:"$outputfile

Write-Host ""
#$OutArray = @()
if (-not(Test-Path -Path $outputfile -PathType Leaf)) {
   "[]" | Out-File -FilePath $outputfile -Append -Encoding utf8
}

$failed = 0
for($i = 0; $i -lt $numberoftests; $i++){
	Write-Host "---"
	Write-Host "Running speed test #"$($i+1)

	#running speedtest
	$response = .\speedtest --format=json-pretty --unit=Mbps
	$responseObj = $response | ConvertFrom-Json

	if ("result" -eq $responseObj.type) {
		#appeding result to the output file
		$content = Get-Content $outputfile -Raw
		
		$separator = ""
		if($content.Length -gt 4) {
			$separator = ","
		}
		
		$content = $content.Substring(0,$content.Length-3)+$separator+"`r`n"+$response+"]"
		$content | Set-Content $outputfile
		
    Write-Host "Download:"$($responseObj.download.bandwidth*8/1000000)"Mbps"
    Write-Host "Upload:"$($responseObj.upload.bandwidth*8/1000000)"Mbps"
		Write-Host "Test #"$($i+1)"completed"
	}
	else {
		Write-Error "Error"
		$failed+=1
	}

  Write-Host "Total tests:" $($i+1) "(failed" $failed")"
  Write-Host "---"
  Write-Host ""

  Start-Sleep -Seconds $interval

}