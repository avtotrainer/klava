; Compile after PyInstaller: ISCC.exe packaging\windows-installer.iss
; User data is created by KLAVA under the actual user's profile, never by Setup.
[Setup]
AppId=KLAVA.CurrentUser
AppName=KLAVA
AppVersion=0.3.1-alpha
AppPublisher=KLAVA
DefaultDirName={localappdata}\Programs\KLAVA
DefaultGroupName=KLAVA
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
MinVersion=10.0
OutputDir=..\dist
OutputBaseFilename=KLAVA-User-Setup-x64
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
SetupIconFile=..\\resources\\branding\\generated\\KLAVA.ico
UninstallDisplayIcon={app}\KLAVA.exe
CloseApplications=yes
RestartApplications=no

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Shortcuts:"; Flags: unchecked

[Files]
Source: "..\dist\KLAVA.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\data\sentences.txt"; DestDir: "{app}"; DestName: "default-exercises.txt"; Flags: ignoreversion

[Icons]
Name: "{group}\KLAVA"; Filename: "{app}\KLAVA.exe"
Name: "{group}\Edit exercises"; Filename: "{app}\KLAVA.exe"; Parameters: "--edit-exercises"
Name: "{autodesktop}\KLAVA"; Filename: "{app}\KLAVA.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\KLAVA.exe"; Description: "Launch KLAVA"; Flags: nowait postinstall skipifsilent runasoriginaluser
