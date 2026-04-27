## Why

Generating a single executable with PyInstaller (`--onefile`) results in a very slow startup time because it needs to extract a massive temporary folder (including huge SpaCy models). This process also triggers false positive antivirus warnings. By utilizing an installer via Inno Setup on top of PyInstaller's `--onedir` mode, the application can extract all necessary capabilities permanently, ensuring instant startup times and providing a native Windows installation experience (Start menu shortcuts, Uninstaller).

## What Changes

- Modify our current build process or add a new script to call PyInstaller with `--onedir` instead of `--onefile`, bundling the application and its dependencies into a folder.
- Create an Inno Setup configuration script (`.iss`) that targets this output directory to generate `Setup_DocAnonymizer.exe`.
- Provide automated steps or documentation to execute the build-then-install packaging process.

## Capabilities

### New Capabilities
- `windows-installer`: The capability specifically governing the generation of a native Windows installer to package the standalone frozen application directory, including an uninstaller and shortcuts.

### Modified Capabilities
- (None)

## Impact

- The build pipeline will include an additional tool (Inno Setup) and command step.
- PyInstaller setup hooks/commands might be adjusted to run in `--onedir` mode.
- Users will execute an installer rather than a standalone CLI/GUI executable, reducing start-time friction immensely.
