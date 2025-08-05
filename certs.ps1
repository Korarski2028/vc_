# Load VMware PowerCLI module
Import-Module VMware.PowerCLI

# Connect to vCenter Server
$vcServer = "your-vcenter-server.domain.com"
Connect-VIServer -Server $vcServer

# Get vCenter certificate from the API endpoint
$certInfo = @()

# Function to extract certificate from a given URL
function Get-CertificateInfo {
    param (
        [string]$hostname,
        [int]$port = 443
    )

    try {
        $tcpClient = New-Object System.Net.Sockets.TcpClient($hostname, $port)
        $sslStream = New-Object System.Net.Security.SslStream($tcpClient.GetStream(), $false, ({ $true }))
        $sslStream.AuthenticateAsClient($hostname)
        $cert = $sslStream.RemoteCertificate
        $cert2 = New-Object System.Security.Cryptography.X509Certificates.X509Certificate2 $cert

        return [PSCustomObject]@{
            Hostname     = $hostname
            Port         = $port
            Subject      = $cert2.Subject
            Issuer       = $cert2.Issuer
            Expiration   = $cert2.NotAfter
            Thumbprint   = $cert2.Thumbprint
        }
    } catch {
        Write-Warning "Failed to retrieve certificate from $hostname:$port"
        return $null
    }
}

# List of common vCenter services and ports
$services = @(
    @{ Name = "vCenter Web Client"; Host = $vcServer; Port = 443 },
    @{ Name = "vCenter SSO"; Host = $vcServer; Port = 7444 },
    @{ Name = "vCenter MOB"; Host = $vcServer; Port = 9443 },
    @{ Name = "vCenter PSC"; Host = $vcServer; Port = 5480 }
)

# Gather certificates
foreach ($svc in $services) {
    $info = Get-CertificateInfo -hostname $svc.Host -port $svc.Port
    if ($info) {
        $info | Add-Member -MemberType NoteProperty -Name Service -Value $svc.Name
        $certInfo += $info
    }
}

# Output results
$certInfo | Format-Table Service, Hostname, Port, Subject, Issuer, Expiration, Thumbprint -AutoSize

# Disconnect from vCenter
Disconnect-VIServer -Server $vcServer -Confirm:$false
