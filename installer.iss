[Setup]
AppName=PF-Carrot
AppVersion=1.0.0
DefaultDirName={autopf}\PF-Carrot
DefaultGroupName=PF-Carrot
OutputDir=installer-output
OutputBaseFilename=Carrot-Installer
Compression=lzma
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64
PrivilegesRequired=admin
UninstallDisplayName=PF-Carrot

[Files]
Source: "app\dist\PF-Carrot.exe"; DestDir: "{app}\PF-Carrot"; Flags: ignoreversion
Source: "assistant d\dist\C-Assistant.exe"; DestDir: "{app}\C-Assistant"; Flags: ignoreversion
Source: "launcher d\dist\Carrot-Launcher.exe"; DestDir: "{app}\Carrot-Launcher"; Flags: ignoreversion
Source: "launcher d\Settings.ini"; DestDir: "{app}\Carrot-Launcher"; Flags: ignoreversion

[Icons]
Name: "{group}\PF-Carrot"; Filename: "{app}\PF-Carrot\PF-Carrot.exe"
Name: "{group}\PF-Carrot Launcher"; Filename: "{app}\Carrot-Launcher\Carrot-Launcher.exe"
Name: "{group}\C-Assistant"; Filename: "{app}\C-Assistant\C-Assistant.exe"

Name: "{autodesktop}\PF-Carrot"; Filename: "{app}\PF-Carrot\PF-Carrot.exe"
Name: "{autodesktop}\PF-Carrot Launcher"; Filename: "{app}\Carrot-Launcher\Carrot-Launcher.exe"
Name: "{autodesktop}\C-Assistant"; Filename: "{app}\C-Assistant\C-Assistant.exe"

[UninstallDelete]
Type: filesandordirs
Name: "{app}"
