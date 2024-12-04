# Script creates the following Azure resources using Azure CLI commands:
# Resource Group, Storage Account, Function App, App Service Plan (Consumption Plan), 
# Application Insights (and an Action Group and Smart Detector Alert Rule used with Application Insights)


# Resource Names and Location
$ResourceGroupName = 'rgmyfunction201420142015'
$StorageAccountName = 'samystorageaccount2015'
$FunctionAppName = 'famyfunctionapp201420142015'
$Location = 'eastus' # To see a list of all locations use: az account list-locations


# Create resource group 
az group create --name $ResourceGroupName --location $Location


# Create general-purpose storage account
az storage account create --name $StorageAccountName --location $Location --resource-group $ResourceGroupName --sku Standard_LRS


# Create function app
az functionapp create --resource-group $ResourceGroupName --consumption-plan-location $Location --runtime python --runtime-version 3.11 --functions-version 4 --name $FunctionAppName --os-type linux --storage-account $StorageAccountName


# To delete the resource group and all resources in it
# az group delete --name $ResourceGroupName