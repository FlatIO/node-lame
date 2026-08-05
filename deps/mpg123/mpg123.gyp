# This file is used with the GYP meta build system.
# http://code.google.com/p/gyp
# To build try this:
#   svn co http://gyp.googlecode.com/svn/trunk gyp
#   ./gyp/gyp -f make --depth=. mpg123.gyp
#   make
#   ./out/Debug/test

{
  'variables': {
    'target_arch%': 'ia32',
  },
  'target_defaults': {
    'default_configuration': 'Debug',
    'configurations': {
      'Debug': {
        'defines': [ 'DEBUG', '_DEBUG', 'MPG123_INTSYM_H' ],
        'msvs_settings': {
          'VCCLCompilerTool': {
            'RuntimeLibrary': 1, # static debug
          },
        },
      },
      'Release': {
        'defines': [ 'NDEBUG', 'MPG123_INTSYM_H' ],
        'msvs_settings': {
          'VCCLCompilerTool': {
            'RuntimeLibrary': 0, # static release
          },
        },
      }
    },
    'msvs_settings': {
      'VCLinkerTool': {
        'GenerateDebugInformation': 'true',
      },
    },
    'conditions': [
      ['OS=="mac"', {
        'conditions': [
          ['target_arch=="ia32"', { 'xcode_settings': { 'ARCHS': [ 'i386' ] } }],
          ['target_arch=="x64"', { 'xcode_settings': { 'ARCHS': [ 'x86_64' ] } }]
        ],
      }],
      ['OS=="win"', {
        'link_settings': {
          'libraries': [
            '-lshlwapi.lib',
          ],
        },
      }],
    ]
  },

  'targets': [
    {
      'target_name': 'mpg123',
      'product_prefix': 'lib',
      'type': 'static_library',
      'variables': {
        'conditions': [
          # "mpg123_cpu" is the cpu optimization to use
          # Windows uses "i386_fpu" even on x64 to avoid compiling .S asm files
          # (I don't think the 64-bit ASM files are compatible with `ml`/`ml64`...)
          ['OS=="win"', { 'mpg123_cpu%': 'i386_fpu' },
          { 'conditions': [
            ['target_arch=="arm64"', { 'mpg123_cpu%': 'arm64' }],
            ['target_arch=="arm"', { 'mpg123_cpu%': 'arm_nofpu' }],
            ['target_arch=="ia32"', { 'mpg123_cpu%': 'i386_fpu' }],
            ['target_arch=="x87"', { 'mpg123_cpu%': 'i386_fpu' }],
            ['target_arch=="x64"', { 'mpg123_cpu%': 'x86-64' }],
          ]}],
        ]
      },
      'sources': [
        'src/libmpg123/parse.c',
        'src/libmpg123/frame.c',
        'src/libmpg123/format.c',
        'src/libmpg123/dct64.c',
        'src/libmpg123/equalizer.c',
        'src/libmpg123/id3.c',
        'src/libmpg123/optimize.c',
        'src/libmpg123/readers.c',
        'src/libmpg123/lfs_wrap.c',
        'src/libmpg123/tabinit.c',
        'src/libmpg123/libmpg123.c',
        'src/libmpg123/index.c',
        'src/libmpg123/stringbuf.c',
        'src/libmpg123/icy.c',
        'src/libmpg123/icy2utf8.c',
        'src/libmpg123/ntom.c',
        'src/libmpg123/synth.c',
        'src/libmpg123/synth_8bit.c',
        'src/libmpg123/layer1.c',
        'src/libmpg123/layer2.c',
        'src/libmpg123/layer3.c',
        'src/libmpg123/feature.c',
	'src/compat/compat.c',
	'src/compat/compat_str.c'
      ],
      'include_dirs': [
        'src/include',
        'src/libmpg123',
        'src/compat',
        'src/common',
        'src',
        # platform and arch-specific headers
        'config/<(OS)/<(target_arch)',
      ],
      'defines': [
        'PIC',
        'NOXFERMEM',
        'HAVE_CONFIG_H',
      ],
      'direct_dependent_settings': {
        'defines': [
          'MPG123_NO_LARGENAME',
        ],
        'include_dirs': [
          'src/include',
          'src/libmpg123',
          'src/common',
          # platform and arch-specific headers
          'config/<(OS)/<(target_arch)',
        ]
      },
      'conditions': [
        ['mpg123_cpu=="arm64"', {
          'defines': [
            'OPT_NEON64',
            'REAL_IS_FLOAT',
          ],
          'sources': [
		  'src/libmpg123/dct36_neon64.S',
		  'src/libmpg123/dct64_neon64_float.S',
		  'src/libmpg123/synth_neon64_float.S',
		  'src/libmpg123/synth_neon64_s32.S',
		  'src/libmpg123/synth_stereo_neon64_float.S',
		  'src/libmpg123/synth_stereo_neon64_s32.S',
		  'src/libmpg123/dct64_neon64.S',
		  'src/libmpg123/synth_neon64.S',
		  'src/libmpg123/synth_stereo_neon64.S',
		  'src/libmpg123/synth_s32.c',
		  'src/libmpg123/synth_real.c',
          ],
        }],
        ['mpg123_cpu=="arm_nofpu"', {
          'defines': [
            'OPT_ARM',
            'REAL_IS_FIXED',
            'NEWOLD_WRITE_SAMPLE',
          ],
          'sources': [
            'src/libmpg123/synth_arm.S',
          ],
        }],
        ['mpg123_cpu=="i386_fpu"', {
          'defines': [
            'OPT_I386',
            'REAL_IS_FLOAT',
            'NEWOLD_WRITE_SAMPLE',
          ],
          'sources': [
            'src/libmpg123/synth_s32.c',
            'src/libmpg123/synth_real.c',
            'src/libmpg123/dct64_i386.c',
          ],
        }],
        ['mpg123_cpu=="x86-64"', {
          'defines': [
            'OPT_X86_64',
            'REAL_IS_FLOAT',
          ],
          'sources': [
            'src/libmpg123/dct64_x86_64.S',
            'src/libmpg123/dct64_x86_64_float.S',
            'src/libmpg123/dct36_x86_64.S',
            'src/libmpg123/synth_s32.c',
            'src/libmpg123/synth_real.c',
            'src/libmpg123/synth_stereo_x86_64.S',
            'src/libmpg123/synth_stereo_x86_64_float.S',
            'src/libmpg123/synth_stereo_x86_64_s32.S',
            'src/libmpg123/synth_x86_64.S',
            'src/libmpg123/synth_x86_64_s32.S',
            'src/libmpg123/synth_x86_64_float.S',
          ],
        }],
      ],
    }
  ]
}
