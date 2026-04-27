#define MyAppName      "ANON V — Doc Anonymizer"
#define MyAppVersion   "1.1.0"
#define MyAppPublisher "Antigravity"
#define MyAppExeName   "AnonymizerPro.exe"
#define MyOutputDir    "..\dist\AnonymizerPro"

[Setup]
AppId={{E7B3A2C1-4F8D-4E9A-B2C3-D5E6F7A8B9C0}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\DocAnonymizer
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
OutputDir=..\dist
OutputBaseFilename=Setup_DocAnonymizer
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
ArchitecturesInstallIn64BitMode=x64compatible

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
Source: "{#MyOutputDir}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#MyAppName}}"; Flags: nowait postinstall skipifsilent

[Code]
procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
var
  AppDataDir: String;
  Response: Integer;
begin
  if CurUninstallStep = usPostUninstall then
  begin
    AppDataDir := ExpandConstant('{userappdata}\doc-anonymizer');
    if DirExists(AppDataDir) then
    begin
      Response := MsgBox(
        '¿Deseas eliminar también tus configuraciones personales y la base de datos de anonimización?' +
        Chr(13) + Chr(10) + '(' + AppDataDir + ')',
        mbConfirmation, MB_YESNO
      );
      if Response = IDYES then
        DelTree(AppDataDir, True, True, True);
    end;
  end;
end;
