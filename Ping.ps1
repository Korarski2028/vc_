#Set-Location -Path "C:temp\"

# Define the path to your host list file
cd C:\temp

# Define the path to the text file containing the server names
$ServerListFile = "Server_list.txt" 

# Read the server names from the text file
$Servers = Get-Content -Path $ServerListFile

# Loop through each server and ping it
foreach ($Server in $Servers) {
    Write-Host "Pinging $Server..."

    # Test the connection to the server
    # -Count 1 sends a single ping packet
    # -ErrorAction SilentlyContinue suppresses errors if the server is unreachable
    $PingResult = ping $Server -Count 1 -ErrorAction SilentlyContinue

    # Check if the ping was successful
    if ($PingResult) {
        Write-Host "$Server is UP" -ForegroundColor Green
    } else {
        Write-Host "$Server is DOWN" -ForegroundColor Red
    }
}

