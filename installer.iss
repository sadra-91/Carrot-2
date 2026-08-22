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
Source: "release\*"; DestDir: "{app}"; Flags: ignoreversion

[Dirs]
Name: "{app}"; Permissions: users-modify

[Icons]
Name: "{group}\PF-Carrot"; Filename: "{app}\PF-Carrot.exe"
Name: "{group}\PF-Carrot Launcher"; Filename: "{app}\Carrot-Launcher.exe"
Name: "{group}\C-Assistant"; Filename: "{app}\C-Assistant.exe"

Name: "{autodesktop}\PF-Carrot"; Filename: "{app}\PF-Carrot.exe"
Name: "{autodesktop}\PF-Carrot Launcher"; Filename: "{app}\Carrot-Launcher.exe"
Name: "{autodesktop}\C-Assistant"; Filename: "{app}\C-Assistant.exe"

[UninstallDelete]
Type: filesandordirs; Name: "{app}"
