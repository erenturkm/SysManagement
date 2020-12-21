# RoboLocalBackup
# By Murat Cudi Erenturk
param(
	[string]$SourceFolder,
	[string]$DestinationFolder,
	[string]$LogsFolder='./'
	)
function GetLogFolderName([string]$LogFolder)
{
	if ($LogFolder.substring($LogFolder.Length-1) -ne '/')
	{
		$LogFolder+='/'
	}
	return $LogFolder
}
function GetLogFileName([string]$LogFolder)
{
	[DateTime]$Now=(get-date)
	return $LogFolder+$Now.ToString('yyyyMMdd-HHmmss')+$ToolName+".log" 
}
function WriteError([string]$msg)
{
	WriteLog 'Error' $msg
}

function WriteWarning([string]$msg)
{
	WriteLog 'Warning' $msg
}

function WriteInfo([string]$msg)
{
	WriteLog 'Info' $msg
}
function WriteLog([string]$Severity, [string]$Message) 
{    
	$Time = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
	$EM=$Time+","+$Severity+","+$Message
	$EM | Out-File -Path $LogFileName -Append
}

function PurgeOldLogs([string] $LogFolder,[string]$FileSuffix,[int]$AgeLimit)
{
	$limit = (Get-Date).AddDays(-$AgeLimit)
	$OldLogs=Get-ChildItem -Directory -Path '*'+$ToolName+'.log' | Where-Object {$_.CreationTime -lt $limit } 
	if ($OldLogs.count -gt 0)
	{
		WriteInfo("Found $oldlogs.count old log files, deleting...") 
		Remove-item -force $OldLogs
	}
}
function StripName([string]$str)
{
	$str=$str.Replace(" ","")
	return $str
}
#Global Variables
$ToolName="RoboLocalBackup"
$ToolVersion="0.5.20201221.1"
$PurgeLogOlderThanDays=7
$SourcePatternRegEx='^[0-9][0-9][0-9]'
#Global Variables


$LogFolder=GetLogFolderName $LogsFolder
$LogFileName=GetLogFileName $LogFolder
WriteInfo "$ToolName+" "+$ToolVersion"
WriteInfo "Logging Started" 
PurgeOldLogs $LogFolder $ToolName $PurgeLogOlderThanDays
if ($SourceFolder.Length -eq 0 -and  ((Test-Path $SourceFolder -PathType Container) -eq $false))
{
	WriteError "Source $SourceFolder does not exist"
	exit $LASTEXITCODE
}
WriteInfo "Source:$SourceFolder"
if ($DestinationFolder.Length -eq 0 -and ((Test-Path $SourceFolder -PathType Container) -eq $false))
{
	WriteError "Destination $DestinationFolder does not exist"
	exit $LASTEXITCODE
}
WriteInfo "Destination:$DestinationFolder"
WriteInfo "Source Pattern:$SourcePatternRegEx"
$SourceDir=Get-ChildItem -Path $SourceFolder -Directory -Force -ErrorAction SilentlyContinue
$TargetDir=Get-ChildItem -Path $DestinationFolder -Directory -Force -ErrorAction SilentlyContinue
foreach($Dir in $SourceDir) 
{
	if ($Dir.Name -match $SourcePatternRegEx)
	{
		$SN=StripName($Dir.Name)
		$cmd="robocopy """+$Dir.FullName +""" """+$DestinationFolder+"/"+$Dir.Name+ """ *.* /MIR /log:"+$LogFolder+$SN+".log"
		Invoke-Expression $cmd
		$Res="Copying "+ $Dir.Name+" returned "+$LASTEXITCODE
		WriteInfo $Res
	}
}
