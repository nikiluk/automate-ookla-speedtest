# Automate ookla speedtest
1. Download Speedtest CLI from [here](https://www.speedtest.net/apps/cli)
2. Open powershell in your terminal in this folder and type `.\test`
3. Make sure that `internetspeed.JSON` has the standard format of the object list of tests, wrapped in `[ ]`

> Attention: PowerShell 5.1 and 6 save in UTF8 with BOM Encoding, so need to reconvert or install PowerShell 7+. 
> 
> To do that, Fire up PowerShell and copy/paste the following cmdlet into the window:

```powershell
iex "& { $(irm https://aka.ms/install-powershell.ps1) } -UseMSI"
```