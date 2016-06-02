## Wwise Plugin Solution Generator

Supports Windows (x86/x64), XB1 and PS4.

### Argument Overview

```
--plugin_name ( -p )
```
- Sets the plugin name. The Wwise convention is to start with a captial letter,
e.g. Delay.
- This will also name various parts of the code and the solutions, e.g DelayFX
would be the name of the projects generated for each platform and DelayPlugin
would be the name of the authoring plugin project.

```
--output_directory ( -o )
```
- Sets the location ( relative paths are ok ) to generate the project.
- Important if you use don't the default Wwise sdk location ( see below ).

```
--company_id ( -c )
```
- Sets the company id used identify a range of effect ids.
- Note, this must be unique. At time of writing these are in use
0, 1, 256, 257, 258, 259, 260, 261, 262, 263, 264.
- You can always check the currently in use company ids in
AK\SoundEngine\Common\AkTypes.h

```
--company_name ( -n )
```
- Used to name a define in all caps like so - AKCOMPANYID_$(COMPANY_NAME_CAPS),
e.g. AKCOMPANYID_COOLPLUGINS.

```
--effect_id ( -e )
```
- Used to identify this effect, must be unique for a given company id.

```
--wwise_sdk_root ( -w )
```
- Sets the location ( relative paths are ok, but see --output_directory above )
of the Wwise sdk to compile against.
- By the default we use the $(WWISE_SDK_ROOT) env variable set by the Wwise
- e.g. "C:\Users\me\Links\Wwise".

### Format files
Format files and the directory structure they live in define how the tool
should create your plugin based on the input parameters. The tool looks for
specific strings, e.g. $(PLUGIN_NAME), and replaces those.

### Generating for a specific compiler toolchain
By default the tool generates solutions/projects for Visual Studio 2012.
It's easy to get visual studio to upgrade the solutions/projects for the version
you use, just run the solution with a newer version. Compilation for
consoles should be painless as long as your sdk installs have defined
$(SCE_ORBIS_SDK_DIR) for ps4 and $(Console_SdkIncludeRoot),
$(Console_SdkLibPath) and $(Console_SdkWindowsMetadataPath) for XB1.
