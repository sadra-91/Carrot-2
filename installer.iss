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

; PF-Carrot
Source: "app\dist\PF-Carrot.exe"; DestDir: "{app}\app"; Flags: ignoreversion

; C-Assistant
Source: "assistant d\dist\C-Assistant.exe"; DestDir: "{app}\assistant d"; Flags: ignoreversion

; Carrot Launcher
Source: "launcher d\dist\Carrot-Launcher.exe"; DestDir: "{app}\launcher d"; Flags: ignoreversion

; Launcher settings
Source: "launcher d\Settings.ini"; DestDir: "{app}\launcher d"; Flags: ignoreversion

[Icons]

Name: "{group}\PF-Carrot"; Filename: "{app}\app\PF-Carrot.exe"
Name: "{group}\PF-Carrot Launcher"; Filename: "{app}\launcher d\Carrot-Launcher.exe"
Name: "{group}\C-Assistant"; Filename: "{app}\assistant d\C-Assistant.exe"

Name: "{autodesktop}\PF-Carrot"; Filename: "{app}\app\PF-Carrot.exe"
Name: "{autodesktop}\PF-Carrot Launcher"; Filename: "{app}\launcher d\Carrot-Launcher.exe"
Name: "{autodesktop}\C-Assistant"; Filename: "{app}\assistant d\C-Assistant.exe"

[UninstallDelete]
Type: filesandordirs; Name: "{app}"
