#########################################################################
# Method 1
Connect-VIServer -Server $Vc -Credential $Creds 

$certMgr = Get-View -Id CertificateManager-certificateManager
$certInfos = $certMgr.CertificateInfoList

foreach ($certInfo in $certInfos) {
    [PSCustomObject]@{
        Subject = $certInfo.Subject
        Issuer = $certInfo.Issuer
        Expiration = $certInfo.NotAfter
    }
} | Format-Table -AutoSize

#########################################################################
# Method 2
# Connect to vCenter and use rest API 
Connect-VIServer -Server $Vc -Credential $Creds 

# get certificates >>> REST API
$headers = @{
    "vmware-api-session-id" = $global:DefaultVIServer.SessionSecret
}
$uri = "https://$Vc/api/vcenter/certificate-management/vcenter/tls"

try {
    $response = Invoke-RestMethod -Uri $uri -Method Get -Headers $headers -ContentType "application/json"
    $response | Select-Object issuer, subject, valid_to | Format-Table -AutoSize
} catch {
    Write-Host "Error accessing API: $_"
}

# Get other  certificate via API
$headers = @{
    "Accept" = "application/json"
}

$uri = "https://$Vc/api/vcenter/certificate-management/vcenter/trusted-root-chains"

try {
    $certificates = Invoke-RestMethod -Uri $uri -Headers $headers -Credential $Creds -Method Get
    $certificates | Format-List
} catch {
    Write-Error "Failed to retrieve certificates: $_"
}

Disconnect-VIServer -Server $Vc -Confirm:$false
########################################################
# solution cert 
Connect-VIServer -Server $Vc -Credential $Creds 
# Get all solution certificates
Get-SsoSolutionCertificate

# Get specific solution certificate details
Get-SsoSolutionCertificate -Name "vsphere-webclient"