# Automate ookla speedtest

## Measurement
1. Download Speedtest CLI from [here](https://www.speedtest.net/apps/cli) and unpack exe file in the repo folder.
2. Open powershell in your terminal in this folder and type `.\test`

> Attention: PowerShell 5.1 and 6 save in UTF8 with BOM Encoding, so need to reconvert or install PowerShell 7+. 
> 
> To do that, Fire up PowerShell and copy/paste the following cmdlet into the window:

```powershell
iex "& { $(irm https://aka.ms/install-powershell.ps1) } -UseMSI"
```

## Analysis
1. Save `internetspeed.json` as a new file `snap.json` and make sure the file has the standard format of the object list of tests, wrapped in `[ ]`
2. Make sure `snap.json` has UTF8 encoding
3. Open and run `main.ipynb` in Python 3 environment to display your stats
