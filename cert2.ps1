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