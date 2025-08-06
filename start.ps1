# Load PowerCLI module
Import-Module VMware.PowerCLI

# Source the helper function
. .\Get-VCSACertificate.ps1  # Adjust path if needed

# Connect to vCenter using domain credentials
Connect-CisServer -Server "your-vcenter.domain.com" -User "DOMAIN\youruser" -Password "yourpassword"

# Get all vCenter certificates
$certs = Get-VCSACertificate

# Export to CSV
$certs | Select-Object Type, Subject, Issuer, NotBefore, NotAfter, Thumbprint |
    Export-Csv -Path "vCenter_Solution_Certificates.csv" -NoTypeInformation

Write-Host " Exported all vCenter certificates to vCenter_Solution_Certificates.csv" -ForegroundColor Green
