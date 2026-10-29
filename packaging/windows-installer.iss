; Compile after PyInstaller: ISCC.exe packaging\windows-installer.iss
; User data is created by KLAVA under the actual user's profile, never by Setup.
[Setup]
AppId=KLAVA.CurrentUser
AppName=KLAVA
AppVersion=0.3.1-beta.1
AppPublisher=KLAVA
DefaultDirName={code:KlavaInstallDir}
DefaultGroupName=KLAVA
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
UsePreviousAppDir=no
UsePreviousPrivileges=no
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
MinVersion=10.0
OutputDir=..\dist
OutputBaseFilename=KLAVA-Setup-x64
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
Source: "..\data\sentences.klv"; DestDir: "{app}"; DestName: "default-exercises.klv"; Flags: ignoreversion

[Icons]
Name: "{group}\KLAVA"; Filename: "{app}\KLAVA.exe"
Name: "{group}\Edit exercises"; Filename: "{app}\KLAVA.exe"; Parameters: "--edit-exercises"
Name: "{autodesktop}\KLAVA"; Filename: "{app}\KLAVA.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\KLAVA.exe"; Description: "Launch KLAVA"; Flags: nowait postinstall skipifsilent runasoriginaluser

[Code]
function InitializeSetup(): Boolean;
begin
  Result := True;
  // MSI registers this marker for its all-users Start menu component.
  // Never remove MSI data or files automatically: prompt the user instead.
  if RegKeyExists(HKLM64, 'Software\KLAVA\MSI') then
  begin
    MsgBox('KLAVA is already installed using the MSI package. Uninstall the MSI version before running this EXE installer.', mbError, MB_OK);
    Result := False;
  end;
end;

function KlavaInstallDir(Param: String): String;
begin
  if IsAdminInstallMode then
    Result := ExpandConstant('{commonpf}\KLAVA')
  else
    Result := ExpandConstant('{localappdata}\Programs\KLAVA');
end;
