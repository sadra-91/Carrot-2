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
Name: "{autodesktop}\PF-Carrot Launcher"; Filename: "{app}\Carrot-Launcher.exe"; IconFilename: "{app}\12icon.ico"

Name: "{group}\PF-Carrot"; Filename: "{app}\PF-Carrot.exe"
Name: "{group}\PF-Carrot Launcher"; Filename: "{app}\Carrot-Launcher.exe"; IconFilename: "{app}\12icon.ico"
Name: "{group}\C-Assistant"; Filename: "{app}\C-Assistant.exe"

[Registry]
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "PF-Carrot Launcher"; ValueData: """{app}\Carrot-Launcher.exe"""; Flags: uninsdeletevalue

[UninstallDelete]
Type: filesandordirs; Name: "{app}"
