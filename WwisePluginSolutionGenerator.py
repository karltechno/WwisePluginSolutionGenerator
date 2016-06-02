import argparse
import re
import os

#------------------------------------------------------------------------------
arg_parser = argparse.ArgumentParser(
    description = 'WwisePluginSolutionGenerator' )
arg_parser.add_argument( '-p', '--plugin_name', nargs = 1,
    help = 'the plugin name to use when naming files - \
            recommened that you use CamelCase',
    dest = 'plugin_name', required = True )
arg_parser.add_argument( '-o', '--output_directory', nargs = 1,
    help = 'a directory called --plugin_name will be created here',
    dest = 'output_directory', required = True )
arg_parser.add_argument( '-c', '--company_id', nargs = 1,
    help = 'id used to identify a range of effect ids',
    dest = 'company_id', required = True )
arg_parser.add_argument( '-n', '--company_name', nargs = 1,
    help = 'name used to create macro plugin factory',
    dest = 'company_name', required = True )
arg_parser.add_argument( '-e', '--effect_id', nargs = 1,
    help = 'id used to identify this effect',
    dest = 'effect_id', required = True )
arg_parser.add_argument( '-w', '--wwise_sdk_root', nargs = 1,
    help = 'location of the wwise sdk root to compile with',
    dest = 'wwise_sdk_root', required = False )
args = arg_parser.parse_args()
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# required information
# $(PLUGIN_NAME) - example AkDelay
PLUGIN_NAME = args.plugin_name[ 0 ]
# $(PLUGIN_NAME_CAPS) - example AKDELAY
PLUGIN_NAME_CAPS = PLUGIN_NAME.upper()
# $(AUTHORING_PLUGIN_NAME) - example DelayPlugin
AUTHORING_PLUGIN_NAME = PLUGIN_NAME + 'Plugin'
# $(COMPANY_ID) - id used to identify a range of effect ids
COMPANY_ID = args.company_id[ 0 ]
# $(COMPANY_NAME_CAPS) - name used to create macro for plugin factory
COMPANY_NAME_CAPS = args.company_name[ 0 ].upper()
# $(EFFECT_ID) - id used to identiy this effect
EFFECT_ID = args.effect_id[ 0 ]
# $(OUTPUT_DIRECTORY) - example ..\libssrc\WwisePlugins
OUTPUT_DIRECTORY = args.output_directory[ 0 ]
# $(WWISE_SDK_ROOT) - example C:\Program Files (x86)\Audiokinetic\Wwise v2015.1.3 build 5488\SDK
WWISE_SDK_ROOT = ''
if args.wwise_sdk_root:
    WWISE_SDK_ROOT = args.wwise_sdk_root[ 0 ]
else:
    WWISE_SDK_ROOT = os.environ[ 'WWISESDK' ]
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# regex expressions
REGEX_PLUGIN_NAME = re.compile( '\$\(PLUGIN_NAME\)' )
REGEX_PLUGIN_NAME_CAPS = re.compile( '\$\(PLUGIN_NAME_CAPS\)' )
REGEX_AUTHORING_PLUGIN_NAME = re.compile( '\$\(AUTHORING_PLUGIN_NAME\)' )
REGEX_COMPANY_ID = re.compile( '\$\(COMPANY_ID\)' )
REGEX_COMPANY_NAME_CAPS = re.compile( '\$\(COMPANY_NAME_CAPS\)' )
REGEX_EFFECT_ID = re.compile( '\$\(EFFECT_ID\)' )
REGEX_WWISE_SDK_ROOT = re.compile( '\$\(WWISE_SDK_ROOT\)' )
#------------------------------------------------------------------------------

# output directory structure
# Dir: $(PLUGIN_NAME)
#   Dir: Sources
#       Dir: AudioEngineFX
#           Dir: PS4
#               File: $(PLUGIN_NAME)FXPS4_vc110.vcxproj
#           Dir: Win32
#               File: $(PLUGIN_NAME)FXWindows_vc110.vcxproj
#           Dir: XboxOne
#               File: $(PLUGIN_NAME)FXXboxOne_vc110.vcxproj
#           File: $(PLUGIN_NAME)FX.cpp
#           File: $(PLUGIN_NAME)FX.h
#           File: $(PLUGIN_NAME)FXDSP.cpp
#           File: $(PLUGIN_NAME)FXDSP.h
#           File: $(PLUGIN_NAME)FXParams.cpp
#           File: $(PLUGIN_NAME)FXParams.h
#       Dir: WwisePlugin
#           Dir: res
#               File: $(PLUGIN_NAME).xml
#           File: $(PLUGIN_NAME).cpp
#           File: $(PLUGIN_NAME).def
#           File: $(PLUGIN_NAME).h
#           File: $(PLUGIN_NAME).rc
#           File: $(PLUGIN_NAME)_vc110.vcxproj
#           File: $(PLUGIN_NAME)_vc110.vcxproj.filters
#           File: $(PLUGIN_NAME)_vc110.vcxproj.user
#           File: $(AUTHORING_PLUGIN_NAME).cpp
#           File: $(AUTHORING_PLUGIN_NAME).h
#           File: resource.h
#           File: stdafx.cpp
#           File: stdafx.h
#   File: $(PLUGING_NAME)FXWindows_vc110.sln

#------------------------------------------------------------------------------
# directories
FORMAT_DIRECTORY = '.\Format'
OUTPUT_ROOT_DIRECTORY = OUTPUT_DIRECTORY + '\\' + PLUGIN_NAME
SOURCES_DIRECTORY = '\\Sources'
AUDIO_ENGINE_FX_DIRECTORY = SOURCES_DIRECTORY + '\\AudioEngineFX'
PS4_DIRECTORY = AUDIO_ENGINE_FX_DIRECTORY + '\\PS4'
WIN32_DIRECTORY = AUDIO_ENGINE_FX_DIRECTORY + '\\Win32'
XBOX_ONE_DIRECTORY = AUDIO_ENGINE_FX_DIRECTORY + '\\XboxOne'
WWISE_PLUGIN_DIRECTORY = SOURCES_DIRECTORY + '\\WwisePlugin'
RES_DIRECTORY = WWISE_PLUGIN_DIRECTORY + '\\res'
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
def validate_arguments():
    assert( PLUGIN_NAME != AUTHORING_PLUGIN_NAME )

    # known company ids in use at this time
    #(0)   ///< Audiokinetic inc.
    #(1)   ///< Audiokinetic inc.
    #(256) ///< McDSP
    #(257) ///< WaveArts
    #(258) ///< Phonetic Arts
    #(259) ///< iZotope
    #(260) ///< GenAudio
    #(261) ///< Crankcase Audio
    #(262) ///< IOSONO
    #(263) ///< Auro Technologies
    #(264) ///< Dolby
    company_ids = [ 0, 1, 256, 257, 258, 259, 260, 261, 262, 263, 264 ]
    assert( int( COMPANY_ID ) not in company_ids )

    assert( os.path.exists( args.output_directory[ 0 ] ) )
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
def explain_actions():
    print( '\ncreating wwise plug-in "' + PLUGIN_NAME + '" ( authoring name: "' + AUTHORING_PLUGIN_NAME + '" )' )
    print( 'output: "' + OUTPUT_ROOT_DIRECTORY + '"' )
    print( 'company id: ' + COMPANY_ID + ' effect id: ' + EFFECT_ID )
    print( 'wwise sdk root: "' + WWISE_SDK_ROOT + '"' )
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
def create_directory( directory ):
    if not os.path.exists( directory ):
        os.mkdir( directory )
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
def create_directory_structure():
    create_directory( OUTPUT_ROOT_DIRECTORY )
    create_directory( OUTPUT_ROOT_DIRECTORY + SOURCES_DIRECTORY )
    create_directory( OUTPUT_ROOT_DIRECTORY + AUDIO_ENGINE_FX_DIRECTORY )
    create_directory( OUTPUT_ROOT_DIRECTORY + PS4_DIRECTORY )
    create_directory( OUTPUT_ROOT_DIRECTORY + WIN32_DIRECTORY )
    create_directory( OUTPUT_ROOT_DIRECTORY + XBOX_ONE_DIRECTORY )
    create_directory( OUTPUT_ROOT_DIRECTORY + WWISE_PLUGIN_DIRECTORY )
    create_directory( OUTPUT_ROOT_DIRECTORY + RES_DIRECTORY )
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
def create_file_from_format_file( format_file, output_file ):
    with open( format_file, 'r' ) as format_file:
        lines = format_file.readlines()
        with open( output_file, 'w' ) as output_file:
            for line in lines:
                formatted_line = line
                formatted_line = re.sub( REGEX_PLUGIN_NAME, PLUGIN_NAME, formatted_line )
                formatted_line = re.sub( REGEX_PLUGIN_NAME_CAPS, PLUGIN_NAME_CAPS, formatted_line )
                formatted_line = re.sub( REGEX_AUTHORING_PLUGIN_NAME, AUTHORING_PLUGIN_NAME, formatted_line )
                formatted_line = re.sub( REGEX_COMPANY_ID, COMPANY_ID, formatted_line )
                formatted_line = re.sub( REGEX_COMPANY_NAME_CAPS, COMPANY_NAME_CAPS, formatted_line )
                formatted_line = re.sub( REGEX_EFFECT_ID, EFFECT_ID, formatted_line )
                formatted_line = re.sub( REGEX_WWISE_SDK_ROOT, WWISE_SDK_ROOT, formatted_line )
                output_file.write( formatted_line )
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
def create_project_files():
    create_file_from_format_file( FORMAT_DIRECTORY + PS4_DIRECTORY +
        '\\$(PLUGIN_NAME)FXPS4_vc110.vcxproj.filters.format',
        OUTPUT_ROOT_DIRECTORY + PS4_DIRECTORY +
        '\\' + PLUGIN_NAME + 'FXPS4_vc110.vcxproj.filters' )

    create_file_from_format_file( FORMAT_DIRECTORY + PS4_DIRECTORY +
        '\\$(PLUGIN_NAME)FXPS4_vc110.vcxproj.format',
        OUTPUT_ROOT_DIRECTORY + PS4_DIRECTORY +
        '\\' + PLUGIN_NAME + 'FXPS4_vc110.vcxproj' )

    create_file_from_format_file( FORMAT_DIRECTORY + WIN32_DIRECTORY +
        '\\$(PLUGIN_NAME)FXWindows_vc110.vcxproj.filters.format',
        OUTPUT_ROOT_DIRECTORY + WIN32_DIRECTORY +
        '\\' + PLUGIN_NAME + 'FXWindows_vc110.vcxproj.filters' )

    create_file_from_format_file( FORMAT_DIRECTORY + WIN32_DIRECTORY +
        '\\$(PLUGIN_NAME)FXWindows_vc110.vcxproj.format',
        OUTPUT_ROOT_DIRECTORY + WIN32_DIRECTORY +
        '\\' + PLUGIN_NAME + 'FXWindows_vc110.vcxproj' )

    create_file_from_format_file( FORMAT_DIRECTORY + XBOX_ONE_DIRECTORY +
        '\\$(PLUGIN_NAME)FXXboxOne_vc110.vcxproj.filters.format',
        OUTPUT_ROOT_DIRECTORY + XBOX_ONE_DIRECTORY +
        '\\' + PLUGIN_NAME + 'FXXboxOne_vc110.vcxproj.filters' )

    create_file_from_format_file( FORMAT_DIRECTORY + XBOX_ONE_DIRECTORY +
        '\\$(PLUGIN_NAME)FXXboxOne_vc110.vcxproj.format',
        OUTPUT_ROOT_DIRECTORY + XBOX_ONE_DIRECTORY +
        '\\' + PLUGIN_NAME + 'FXXboxOne_vc110.vcxproj' )

    create_file_from_format_file( FORMAT_DIRECTORY + AUDIO_ENGINE_FX_DIRECTORY +
        '\\$(PLUGIN_NAME)FX.cpp.format',
        OUTPUT_ROOT_DIRECTORY + AUDIO_ENGINE_FX_DIRECTORY +
        '\\' + PLUGIN_NAME + 'FX.cpp' )

    create_file_from_format_file( FORMAT_DIRECTORY + AUDIO_ENGINE_FX_DIRECTORY +
        '\\$(PLUGIN_NAME)FX.h.format',
        OUTPUT_ROOT_DIRECTORY + AUDIO_ENGINE_FX_DIRECTORY +
        '\\' + PLUGIN_NAME + 'FX.h' )

    create_file_from_format_file( FORMAT_DIRECTORY + AUDIO_ENGINE_FX_DIRECTORY +
        '\\$(PLUGIN_NAME)FXDSP.cpp.format',
        OUTPUT_ROOT_DIRECTORY + AUDIO_ENGINE_FX_DIRECTORY +
        '\\' + PLUGIN_NAME + 'FXDSP.cpp' )

    create_file_from_format_file( FORMAT_DIRECTORY + AUDIO_ENGINE_FX_DIRECTORY +
        '\\$(PLUGIN_NAME)FXDSP.h.format',
        OUTPUT_ROOT_DIRECTORY + AUDIO_ENGINE_FX_DIRECTORY +
        '\\' + PLUGIN_NAME + 'FXDSP.h' )

    create_file_from_format_file( FORMAT_DIRECTORY + AUDIO_ENGINE_FX_DIRECTORY +
        '\\$(PLUGIN_NAME)FXFactory.h.format',
        OUTPUT_ROOT_DIRECTORY + AUDIO_ENGINE_FX_DIRECTORY +
        '\\' + PLUGIN_NAME + 'FXFactory.h' )

    create_file_from_format_file( FORMAT_DIRECTORY + AUDIO_ENGINE_FX_DIRECTORY +
        '\\$(PLUGIN_NAME)FXParams.cpp.format',
        OUTPUT_ROOT_DIRECTORY + AUDIO_ENGINE_FX_DIRECTORY +
        '\\' + PLUGIN_NAME + 'FXParams.cpp' )

    create_file_from_format_file( FORMAT_DIRECTORY + AUDIO_ENGINE_FX_DIRECTORY +
        '\\$(PLUGIN_NAME)FXParams.h.format',
        OUTPUT_ROOT_DIRECTORY + AUDIO_ENGINE_FX_DIRECTORY +
        '\\' + PLUGIN_NAME + 'FXParams.h' )

    create_file_from_format_file( FORMAT_DIRECTORY + WWISE_PLUGIN_DIRECTORY +
        '\\$(PLUGIN_NAME).cpp.format',
        OUTPUT_ROOT_DIRECTORY + WWISE_PLUGIN_DIRECTORY +
        '\\' + PLUGIN_NAME + '.cpp' )

    create_file_from_format_file( FORMAT_DIRECTORY + WWISE_PLUGIN_DIRECTORY +
        '\\$(PLUGIN_NAME).def.format',
        OUTPUT_ROOT_DIRECTORY + WWISE_PLUGIN_DIRECTORY +
        '\\' + PLUGIN_NAME + '.def' )

    create_file_from_format_file( FORMAT_DIRECTORY + WWISE_PLUGIN_DIRECTORY +
        '\\$(PLUGIN_NAME).h.format',
        OUTPUT_ROOT_DIRECTORY + WWISE_PLUGIN_DIRECTORY +
        '\\' + PLUGIN_NAME + '.h' )

    create_file_from_format_file( FORMAT_DIRECTORY + WWISE_PLUGIN_DIRECTORY +
        '\\$(AUTHORING_PLUGIN_NAME).cpp.format',
        OUTPUT_ROOT_DIRECTORY + WWISE_PLUGIN_DIRECTORY +
        '\\' + AUTHORING_PLUGIN_NAME + '.cpp' )

    create_file_from_format_file( FORMAT_DIRECTORY + WWISE_PLUGIN_DIRECTORY +
        '\\$(AUTHORING_PLUGIN_NAME).h.format',
        OUTPUT_ROOT_DIRECTORY + WWISE_PLUGIN_DIRECTORY +
        '\\' + AUTHORING_PLUGIN_NAME + '.h' )

    create_file_from_format_file( FORMAT_DIRECTORY + WWISE_PLUGIN_DIRECTORY +
        '\\resource.h.format',
        OUTPUT_ROOT_DIRECTORY + WWISE_PLUGIN_DIRECTORY +
        '\\resource.h' )

    create_file_from_format_file( FORMAT_DIRECTORY + WWISE_PLUGIN_DIRECTORY +
        '\\$(PLUGIN_NAME).rc.format',
        OUTPUT_ROOT_DIRECTORY + WWISE_PLUGIN_DIRECTORY +
        '\\' + PLUGIN_NAME + '.rc' )

    create_file_from_format_file( FORMAT_DIRECTORY + WWISE_PLUGIN_DIRECTORY +
        '\\stdafx.cpp.format',
        OUTPUT_ROOT_DIRECTORY + WWISE_PLUGIN_DIRECTORY +
        '\\stdafx.cpp' )

    create_file_from_format_file( FORMAT_DIRECTORY + WWISE_PLUGIN_DIRECTORY +
        '\\stdafx.h.format',
        OUTPUT_ROOT_DIRECTORY + WWISE_PLUGIN_DIRECTORY +
        '\\stdafx.h' )

    create_file_from_format_file( FORMAT_DIRECTORY + RES_DIRECTORY +
        '\\$(PLUGIN_NAME).xml.format',
        OUTPUT_ROOT_DIRECTORY + RES_DIRECTORY +
        '\\' + PLUGIN_NAME + '.xml' )

    create_file_from_format_file( FORMAT_DIRECTORY + WWISE_PLUGIN_DIRECTORY +
        '\\$(PLUGIN_NAME)_vc110.vcxproj.filters.format',
        OUTPUT_ROOT_DIRECTORY + WWISE_PLUGIN_DIRECTORY +
        '\\' + PLUGIN_NAME + '_vc110.vcxproj.filters' )

    create_file_from_format_file( FORMAT_DIRECTORY + WWISE_PLUGIN_DIRECTORY +
        '\\$(PLUGIN_NAME)_vc110.vcxproj.format',
        OUTPUT_ROOT_DIRECTORY + WWISE_PLUGIN_DIRECTORY +
        '\\' + PLUGIN_NAME + '_vc110.vcxproj' )

    create_file_from_format_file( FORMAT_DIRECTORY +
        '\\$(PLUGIN_NAME)FXPS4_vc110.sln.format',
        OUTPUT_ROOT_DIRECTORY +
        '\\' + PLUGIN_NAME + 'FXPS4_vc110.sln' )

    create_file_from_format_file( FORMAT_DIRECTORY +
        '\\$(PLUGIN_NAME)FXWindows_vc110.sln.format',
        OUTPUT_ROOT_DIRECTORY +
        '\\' + PLUGIN_NAME + 'FXWindows_vc110.sln' )

    create_file_from_format_file( FORMAT_DIRECTORY +
        '\\$(PLUGIN_NAME)FXXboxOne_vc110.sln.format',
        OUTPUT_ROOT_DIRECTORY +
        '\\' + PLUGIN_NAME + 'FXXBoxOne_vc110.sln' )
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
if __name__ == "__main__":
    validate_arguments()
    explain_actions()
    create_directory_structure()
    create_project_files()
#------------------------------------------------------------------------------
