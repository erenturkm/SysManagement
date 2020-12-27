#Create Azure Web-App
#requirements
#	This script requires Az Powershell Module and can be installed using
#	Install-Module -Name Az -AllowClobber -Scope AllUsers

#Required Parameters
$ResourceGroupName="TestRG"
$ServiceLocation="North Europe"
$AppServicePlanName="TestAppPlan"
$AppServiceTier="Free"
$AppServiceInstanceSize="Small"
$AppServiceInstanceCount=1
$WordpressAppName="egeerenturk"
$ContainerImageName="wordpress"
$newAppsettings=@{"WEBSITE_MYSQL_ENABLED"="1";"WEBSITE_MYSQL_GENERAL_LOG"="0";"WEBSITE_MYSQL_SLOW_QUERY_LOG"="0";"WEBSITE_MYSQL_ARGUMENTS"="--max_allowed_packet=16M"}


#Login to Azure
Connect-AzAccount

# Create Resouce group to hold the Site
$ResGroup=Get-AzResourceGroup | Where-Object {$_.ResourceGroupName -eq $ResourceGroupName}
if (-not $ResGroup)
{
	out-host "Resource Group does not exist, creating..."
	$ResGroup=New-AzResourceGroup -Name $ResourceGroupName -Location $ServiceLocation
	if (-not $ResGroup)
	{
		out-host "Resource Group was not created,aborted"
		exit
	}
}
#Create an app service plan to host our web app
$AppServicePlan=Get-AzAppServicePlan | Where-Object {$_.Name -eq $AppServicePlanName}
if (-not $AppServicePlan)
{
	out-host "AppServicePlan does not exist, creating..."
	$AppServicePlan=New-AzAppServicePlan -ResourceGroupName $ResourceGroupName -Name $AppServicePlanName -Location $ServiceLocation -Tier $AppServiceTier -NumberofWorkers $AppServiceInstanceCount -WorkerSize $AppServiceInstanceSize
	if (-not $AppServicePlan)
	{
		out-host "App Service Plan was not created,aborted"
		exit
	}
}
#Create an app from Docker Image to host our Wordpress Site
$App=Get-AzWebApp -ResourceGroupName $ResourceGroupName -Name $WordpressAppName
if ($App)
{
	out-host "Web App with name " + $WordpressAppName + " exists, aborted"
	exit
}
else
{
	$App=New-AzWebApp -ResourceGroupName $ResourceGroupName -Name $WordpressAppName -Location $ServiceLocation -AppServicePlan $AppServicePlanName -ContainerImageName $ContainerImageName
}
$App.SiteConfig.LocalMySqlEnabled=$True
Set-AzWebApp  -ResourceGroupName $ResourceGroupName -Name $WordpressAppName -AppSettings  $newAppsettings

