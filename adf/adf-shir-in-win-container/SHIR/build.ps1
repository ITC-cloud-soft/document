$DmgcmdPath = "C:\Program Files\Microsoft Integration Runtime\5.0\Shared\dmgcmd.exe"

function Write-Log($Message) {
    function TS { Get-Date -Format 'MM/dd/yyyy hh:mm:ss' }
    Write-Host "[$(TS)] $Message"
}

function Set-Local-Dispaly() {
    # 地域は日本に変更する（変更しない場合、TiDBに日時項目の登録はエラーになる）
    Set-ItemProperty -Path "HKCU:\Control Panel\International" -Name sShortDate -Value "yyyy/MM/dd";
    Set-ItemProperty -Path "HKCU:\Control Panel\International" -Name sShortTime -Value "HH:mm";
    Set-ItemProperty -Path "HKCU:\Control Panel\International" -Name sTimeFormat -Value "HH:mm:ss";
    Set-ItemProperty -Path "HKCU:\Control Panel\International" -Name Locale -Value "00000411";
    Set-ItemProperty -Path "HKCU:\Control Panel\International" -Name LocaleName -Value "ja-JP";
    Set-ItemProperty -Path "HKCU:\Control Panel\International" -Name iDate -Value "2";
    Set-ItemProperty -Path "HKCU:\Control Panel\International" -Name iTime -Value "1";
    Set-ItemProperty -Path "HKCU:\Control Panel\International" -Name iCountry -Value "81";

    Set-Culture -CultureInfo ja-JP;
}

function Install-MySql-Connector() {
    Write-Log "Install the MySql Connector in the Windows container"

    $MsiFiles = (Get-ChildItem -Path C:\SHIR | Where-Object { $_.Name -match [regex] "mysql-connector-odbc-.*-winx64.msi" })
    if ($MsiFiles) {
        $MsiFileName = $MsiFiles[0].Name
        Write-Log "Using MySql Connector MSI file: $MsiFileName"
    }
    else {
        Write-Log "Downloading latest version of  MySql Connector MSI file"
        $MsiFileName = 'mysql-connector-odbc-latest-winx64.msi'

        # Temporarily disable progress updates to speed up the download process. (See https://stackoverflow.com/questions/69942663/invoke-webrequest-progress-becomes-irresponsive-paused-while-downloading-the-fil)
        $ProgressPreference = 'SilentlyContinue'
        Invoke-WebRequest -Uri 'https://dev.mysql.com/get/Downloads/Connector-ODBC/8.2/mysql-connector-odbc-8.2.0-winx64.msi' -OutFile "C:\SHIR\$MsiFileName"
        $ProgressPreference = 'Continue'
    }

    Write-Log "Installing VC_redist.x64"
    Start-Process "C:\SHIR\VC_redist.x64.exe" -Wait -ArgumentList "/install /quiet"
    if (!$?) {
        Write-Log " VC_redist Install Failed"
    }

    Write-Log "Installing MySql Connector"
    Start-Process msiexec.exe -Wait -ArgumentList "/i C:\SHIR\$MsiFileName /qn"
    if (!$?) {
        Write-Log " MySql Connector MSI Install Failed"
    }

    Write-Log " MySql Connector MSI Install Successfully"
    Write-Log "Will remove C:\SHIR\$MsiFileName"
    Remove-Item "C:\SHIR\$MsiFileName"
    Write-Log "Will remove C:\SHIR\VC_redist.x64.exe"
    Remove-Item "C:\SHIR\VC_redist.x64.exe"
    Write-Log "Removed C:\SHIR\$MsiFileName"
    Write-Log "Removed C:\SHIR\VC_redist.x64.exe"
}

function Install-SHIR() {
    Write-Log "Install the Self-hosted Integration Runtime in the Windows container"

    $MsiFiles = (Get-ChildItem -Path C:\SHIR | Where-Object { $_.Name -match [regex] "IntegrationRuntime.*.msi" })
    if ($MsiFiles) {
        $MsiFileName = $MsiFiles[0].Name
        Write-Log "Using SHIR MSI file: $MsiFileName"
    }
    else {
        Write-Log "Downloading latest version of SHIR MSI file"
        $MsiFileName = 'IntegrationRuntime.latest.msi'

        # Temporarily disable progress updates to speed up the download process. (See https://stackoverflow.com/questions/69942663/invoke-webrequest-progress-becomes-irresponsive-paused-while-downloading-the-fil)
        $ProgressPreference = 'SilentlyContinue'
        Invoke-WebRequest -Uri 'https://go.microsoft.com/fwlink/?linkid=839822&clcid=0x409' -OutFile "C:\SHIR\$MsiFileName"
        $ProgressPreference = 'Continue'
    }

    Write-Log "Installing SHIR"
    Start-Process msiexec.exe -Wait -ArgumentList "/i C:\SHIR\$MsiFileName /qn"
    if (!$?) {
        Write-Log "SHIR MSI Install Failed"
    }

    Write-Log "SHIR MSI Install Successfully"
    Write-Log "Will remove C:\SHIR\$MsiFileName"
    Remove-Item "C:\SHIR\$MsiFileName"
    Write-Log "Removed C:\SHIR\$MsiFileName"
}

function Install-MSFT-JDK() {
    Write-Log "Install the Microsoft OpenJDK in the Windows container"

    Write-Log "Downloading Microsoft OpenJDK 11 LTS msi"
    $JDKMsiFileName = 'microsoft-jdk-11-windows-x64.msi'

    # Temporarily disable progress updates to speed up the download process. (See https://stackoverflow.com/questions/69942663/invoke-webrequest-progress-becomes-irresponsive-paused-while-downloading-the-fil)
    $ProgressPreference = 'SilentlyContinue'
    Invoke-WebRequest -Uri "https://aka.ms/download-jdk/$JDKMsiFileName" -OutFile "C:\SHIR\$JDKMsiFileName"
    $ProgressPreference = 'Continue'

    Write-Log "Installing Microsoft OpenJDK"
    # Arguments pulled from https://learn.microsoft.com/en-us/java/openjdk/install#install-via-msi
    Start-Process msiexec.exe -Wait -ArgumentList "/i C:\SHIR\$JDKMsiFileName ADDLOCAL=FeatureMain,FeatureEnvironment,FeatureJarFileRunWith,FeatureJavaHome INSTALLDIR=`"c:\Program Files\Microsoft\`" /quiet"
    if (!$?) {
        Write-Log "Microsoft OpenJDK MSI Install Failed"
    }
    Write-Log "Microsoft OpenJDK MSI Install Successfully"
    Write-Log "Will remove C:\SHIR\$JDKMsiFileName"
    Remove-Item "C:\SHIR\$JDKMsiFileName"
    Write-Log "Removed C:\SHIR\$JDKMsiFileName"
}

function SetupEnv() {
    Write-Log "Begin to Setup the SHIR Environment"
    Start-Process $DmgcmdPath -Wait -ArgumentList "-Stop -StopUpgradeService -TurnOffAutoUpdate"
    Write-Log "SHIR Environment Setup Successfully"
}

Set-Local-Dispaly
Install-MySql-Connector
Install-SHIR
if ([bool]::Parse($env:INSTALL_JDK)) {
    Install-MSFT-JDK
}

exit 0
