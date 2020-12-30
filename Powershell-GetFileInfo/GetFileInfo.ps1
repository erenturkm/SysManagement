#GetFileInfo
#By Murat Cudi Erenturk

param ($FolderName = $(throw "FolderName is required."))
$ToolVersion="1.0.20200727.1"
$OutputName="FolderInfo.csv"
$LogFileName="GetFileInfo.Log"
$ErrorLogFileName="Errors.Log"
if ([System.IO.File]::Exists($OutputName)) {Remove-item $OutputName}
if ([System.IO.File]::Exists($LogFileName)) {Remove-item $LogFileName}
if ([System.IO.File]::Exists($ErrorLogFileName)) {Remove-item $ErrorLogFileName}
$ST=[System.DateTime]::Now
$Dirs=get-childitem -Path $FolderName -Recurse -Directory 2>> $ErrorLogFileName
$DirCount=$Dirs.Count
$TS1=([System.DateTime]::Now).Subtract($ST)
$LogLine="Discovered "+ $DirCount +" Folders in "+ $TS1.TotalSeconds + " seconds"
Add-Content $LogFileName $LogLine
$ProcessCount=1
$TotalFileSize=0
$TotalFileCount=0
[int]$CompletedOld=0
$LogLine="Starting Counting inside Folders"
Add-Content $LogFileName $LogLine
foreach($Dir in $Dirs)
{
	$Line=""
	$DirName=$Dir.Fullname
	$Files=$Dir.EnumerateFiles() 2>> $ErrorLogFileName
	$MO=$Files | Measure-Object -Property Length -Sum
	$Count=$MO.Count
	$Size=$MO.Sum
	$TotalFileCount=$TotalFileCount+$Count
	$TotalFileSize=$TotalFileSize+$Size
	$Line=$DirName+ "," + $Count + "," + $Size
	Add-Content $OutputName $Line
	$Completed=[int]($ProcessCount*100/$DirCount)
#	[string]$DebugLine=[string]$Completed+","+[string]$CompletedOld+","+[string]$ProcessCount+"/"+[string]$DirCount
#	Add-Content $LogFileName $DebugLine
	if ($Completed -gt $CompletedOld)
	{
		$TS=([System.DateTime]::Now).Subtract($ST)
		$LogLine="Completed %"+[int]($Completed)+" ," + $ProcessCount + " folders in "+ $TS.TotalSeconds + " seconds"
		$CompletedOld=$Completed
		Add-Content $LogFileName $LogLine
	}
	$ProcessCount=$ProcessCount+1
}
$TS2=([System.DateTime]::Now).Subtract($ST)
$TFSMB=$TotalFileSize/1024/1024
$LogLine="Counted " + $TotalFileCount + " files with size " + [string]$TFSMB + " MB" 
Add-Content $LogFileName $LogLine
$LogLine="Finished " + $ProcessCount + " folders in " + $TS2.Hours + ":" + $TS2.Minutes + ":"+$TS2.Seconds
Add-Content $LogFileName $LogLine
Write-Output $LogLine