# Copyright 2012 the V8 project authors. All rights reserved.
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#     * Neither the name of Google Inc. nor the names of its
#       contributors may be used to endorse or promote products derived
#       from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# Shared definitions for all V8-related targets.

{
  'variables': {
    'use_system_v8%': 0,
    'msvs_use_common_release': 0,
    'gcc_version%': 'unknown',
    'v8_compress_startup_data%': 'off',
    'v8_target_arch%': '<(target_arch)',

    # Setting 'v8_can_use_unaligned_accesses' to 'true' will allow the code
    # generated by V8 to do unaligned memory access, and setting it to 'false'
    # will ensure that the generated code will always do aligned memory
    # accesses. The default value of 'default' will try to determine the correct
    # setting. Note that for Intel architectures (ia32 and x64) unaligned memory
    # access is allowed for all CPUs.
    'v8_can_use_unaligned_accesses%': 'default',

    # Setting 'v8_can_use_vfp2_instructions' to 'true' will enable use of ARM VFP
    # instructions in the V8 generated code. VFP instructions will be enabled
    # both for the snapshot and for the ARM target. Leaving the default value
    # of 'false' will avoid VFP instructions in the snapshot and use CPU feature
    # probing when running on the target.
    'v8_can_use_vfp2_instructions%': 'false',
    'v8_can_use_vfp3_instructions%': 'false',

    # Similar to vfp but on MIPS.
    'v8_can_use_fpu_instructions%': 'true',

    # Setting v8_use_arm_eabi_hardfloat to true will turn on V8 support for ARM
    # EABI calling convention where double arguments are passed in VFP
    # registers. Note that the GCC flag '-mfloat-abi=hard' should be used as
    # well when compiling for the ARM target.
    'v8_use_arm_eabi_hardfloat%': 'false',

    # Similar to the ARM hard float ABI but on MIPS.
    'v8_use_mips_abi_hardfloat%': 'true',

    # Default arch variant for MIPS.
    'mips_arch_variant%': 'mips32r2',

    'v8_enable_debugger_support%': 1,

    'v8_enable_disassembler%': 0,

    'v8_object_print%': 0,

    'v8_enable_gdbjit%': 0,

    # Enable profiling support. Only required on Windows.
    'v8_enable_prof%': 0,

    # Some versions of GCC 4.5 seem to need -fno-strict-aliasing.
    'v8_no_strict_aliasing%': 0,

    # Chrome needs this definition unconditionally. For standalone V8 builds,
    # it's handled in build/standalone.gypi.
    'want_separate_host_toolset%': 1,

    'v8_use_snapshot%': 'true',
    'host_os%': '<(OS)',
    'v8_use_liveobjectlist%': 'false',
    'werror%': '-Werror',

    # With post mortem support enabled, metadata is embedded into libv8 that
    # describes various parameters of the VM for use by debuggers. See
    # tools/gen-postmortem-metadata.py for details.
    'v8_postmortem_support%': 'false',

    # For a shared library build, results in "libv8-<(soname_version).so".
    'soname_version%': '',
  },
  'target_defaults': {
    'conditions': [
      ['v8_enable_debugger_support==1', {
        'defines': ['ENABLE_DEBUGGER_SUPPORT',],
      }],
      ['v8_enable_disassembler==1', {
        'defines': ['ENABLE_DISASSEMBLER',],
      }],
      ['v8_object_print==1', {
        'defines': ['OBJECT_PRINT',],
      }],
      ['v8_enable_gdbjit==1', {
        'defines': ['ENABLE_GDB_JIT_INTERFACE',],
      }],
      ['v8_target_arch=="arm"', {
        'defines': [
          'V8_TARGET_ARCH_ARM',
        ],
        'conditions': [
          [ 'v8_can_use_unaligned_accesses=="true"', {
            'defines': [
              'CAN_USE_UNALIGNED_ACCESSES=1',
            ],
          }],
          [ 'v8_can_use_unaligned_accesses=="false"', {
            'defines': [
              'CAN_USE_UNALIGNED_ACCESSES=0',
            ],
          }],
          [ 'v8_can_use_vfp2_instructions=="true"', {
            'defines': [
              'CAN_USE_VFP2_INSTRUCTIONS',
            ],
          }],
          [ 'v8_can_use_vfp3_instructions=="true"', {
            'defines': [
              'CAN_USE_VFP3_INSTRUCTIONS',
            ],
          }],
          [ 'v8_use_arm_eabi_hardfloat=="true"', {
            'defines': [
              'USE_EABI_HARDFLOAT=1',
              'CAN_USE_VFP2_INSTRUCTIONS',
            ],
            'target_conditions': [
              ['_toolset=="target"', {
                'cflags': ['-mfloat-abi=hard',],
              }],
            ],
          }, {
            'defines': [
              'USE_EABI_HARDFLOAT=0',
            ],
          }],
        ],
      }],  # v8_target_arch=="arm"
      ['v8_target_arch=="ia32"', {
        'defines': [
          'V8_TARGET_ARCH_IA32',
        ],
      }],  # v8_target_arch=="ia32"
      ['v8_target_arch=="mips"', {
        'defines': [
          'V8_TARGET_ARCH_MIPS',
        ],
        'variables': {
          'mipscompiler': '<!($(echo ${CXX:-$(which g++)}) -v 2>&1 | grep -q "^Target: mips-" && echo "yes" || echo "no")',
        },
        'conditions': [
          ['mipscompiler=="yes"', {
            'target_conditions': [
              ['_toolset=="target"', {
                'cflags': ['-EL'],
                'ldflags': ['-EL'],
                'conditions': [
                  [ 'v8_use_mips_abi_hardfloat=="true"', {
                    'cflags': ['-mhard-float'],
                    'ldflags': ['-mhard-float'],
                  }, {
                    'cflags': ['-msoft-float'],
                    'ldflags': ['-msoft-float'],
                  }],
                  ['mips_arch_variant=="mips32r2"', {
                    'cflags': ['-mips32r2', '-Wa,-mips32r2'],
                  }],
                  ['mips_arch_variant=="loongson"', {
                    'cflags': ['-mips3', '-Wa,-mips3'],
                  }, {
                    'cflags': ['-mips32', '-Wa,-mips32'],
                  }],
                ],
              }],
            ],
          }],
          [ 'v8_can_use_fpu_instructions=="true"', {
            'defines': [
              'CAN_USE_FPU_INSTRUCTIONS',
            ],
          }],
          [ 'v8_use_mips_abi_hardfloat=="true"', {
            'defines': [
              '__mips_hard_float=1',
              'CAN_USE_FPU_INSTRUCTIONS',
            ],
          }, {
            'defines': [
              '__mips_soft_float=1'
            ],
          }],
          ['mips_arch_variant=="mips32r2"', {
            'defines': ['_MIPS_ARCH_MIPS32R2',],
          }],
          ['mips_arch_variant=="loongson"', {
            'defines': ['_MIPS_ARCH_LOONGSON',],
          }],
        ],
      }],  # v8_target_arch=="mips"
      ['v8_target_arch=="x64"', {
        'defines': [
          'V8_TARGET_ARCH_X64',
        ],
        'xcode_settings': {
          'ARCHS': [ 'x86_64' ],
        },
        'msvs_settings': {
          'VCLinkerTool': {
            'StackReserveSize': '2097152',
          },
        },
      }],  # v8_target_arch=="x64"
      ['v8_use_liveobjectlist=="true"', {
        'defines': [
          'ENABLE_DEBUGGER_SUPPORT',
          'INSPECTOR',
          'OBJECT_PRINT',
          'LIVEOBJECTLIST',
        ],
      }],
      ['v8_compress_startup_data=="bz2"', {
        'defines': [
          'COMPRESS_STARTUP_DATA_BZ2',
        ],
      }],
      ['OS=="win"', {
        'defines': [
          'WIN32',
        ],
        'msvs_configuration_attributes': {
          'OutputDirectory': '<(DEPTH)\\build\\$(ConfigurationName)',
          'IntermediateDirectory': '$(OutDir)\\obj\\$(ProjectName)',
          'CharacterSet': '1',
        },
      }],
      ['OS=="win" and v8_enable_prof==1', {
        'msvs_settings': {
          'VCLinkerTool': {
            'GenerateMapFile': 'true',
          },
        },
      }],
      ['OS=="linux" or OS=="freebsd" or OS=="openbsd" or OS=="solaris" \
         or OS=="netbsd"', {
        'conditions': [
          [ 'v8_no_strict_aliasing==1', {
            'cflags': [ '-fno-strict-aliasing' ],
          }],
        ],  # conditions
      }],
      ['OS=="solaris"', {
        'defines': [ '__C99FEATURES__=1' ],  # isinf() etc.
      }],
      ['(OS=="linux" or OS=="freebsd" or OS=="openbsd" or OS=="solaris" \
         or OS=="netbsd" or OS=="mac" or OS=="android") and \
        (v8_target_arch=="arm" or v8_target_arch=="ia32" or \
         v8_target_arch=="mips")', {
        # Check whether the host compiler and target compiler support the
        # '-m32' option and set it if so.
        'target_conditions': [
          ['_toolset=="host"', {
            'variables': {
              'm32flag': '<!((echo | $(echo ${CXX_host:-$(which g++)}) -m32 -E - > /dev/null 2>&1) && echo -n "-m32" || true)',
            },
            'cflags': [ '<(m32flag)' ],
            'ldflags': [ '<(m32flag)' ],
            'xcode_settings': {
              'ARCHS': [ 'i386' ],
            },
          }],
          ['_toolset=="target"', {
            'variables': {
              'm32flag': '<!((echo | $(echo ${CXX_target:-${CXX:-$(which g++)}}) -m32 -E - > /dev/null 2>&1) && echo -n "-m32" || true)',
            },
            'cflags': [ '<(m32flag)' ],
            'ldflags': [ '<(m32flag)' ],
            'xcode_settings': {
              'ARCHS': [ 'i386' ],
            },
          }],
        ],
      }],
      ['OS=="freebsd" or OS=="openbsd"', {
        'cflags': [ '-I/usr/local/include' ],
      }],
      ['OS=="netbsd"', {
        'cflags': [ '-I/usr/pkg/include' ],
      }],
    ],  # conditions
    'configurations': {
      'Debug': {
        'defines': [
          'DEBUG',
          'ENABLE_DISASSEMBLER',
          'V8_ENABLE_CHECKS',
          'OBJECT_PRINT',
        ],
        'msvs_settings': {
          'VCCLCompilerTool': {
            'Optimization': '0',

            'conditions': [
              ['OS=="win" and component=="shared_library"', {
                'RuntimeLibrary': '3',  # /MDd
              }, {
                'RuntimeLibrary': '1',  # /MTd
              }],
            ],
          },
          'VCLinkerTool': {
            'LinkIncremental': '2',
          },
        },
        'conditions': [
          ['OS=="linux" or OS=="freebsd" or OS=="openbsd" or OS=="netbsd"', {
            'cflags': [ '-Wall', '<(werror)', '-W', '-Wno-unused-parameter',
                        '-Wnon-virtual-dtor', '-Woverloaded-virtual' ],
          }],
        ],
      },  # Debug
      'Release': {
        'conditions': [
          ['OS=="linux" or OS=="freebsd" or OS=="openbsd" or OS=="netbsd" \
            or OS=="android"', {
            'conditions': [
              [ 'gcc_version==44 and clang==0', {
                'cflags': [
                  # Avoid crashes with gcc 4.4 in the v8 test suite.
                  '-fno-tree-vrp',
                ],
              }],
            ],
          }],
          ['OS=="mac"', {
            'xcode_settings': {
              'GCC_OPTIMIZATION_LEVEL': '3',  # -O3

              # -fstrict-aliasing.  Mainline gcc
              # enables this at -O2 and above,
              # but Apple gcc does not unless it
              # is specified explicitly.
              'GCC_STRICT_ALIASING': 'YES',
            },
          }],  # OS=="mac"
          ['OS=="win"', {
            'msvs_settings': {
              'VCCLCompilerTool': {
                'Optimization': '2',
                'InlineFunctionExpansion': '2',
                'EnableIntrinsicFunctions': 'true',
                'FavorSizeOrSpeed': '0',
                'OmitFramePointers': 'true',
                'StringPooling': 'true',

                'conditions': [
                  ['OS=="win" and component=="shared_library"', {
                    'RuntimeLibrary': '2',  #/MD
                  }, {
                    'RuntimeLibrary': '0',  #/MT
                  }],
                ],
              },
              'VCLinkerTool': {
                'LinkIncremental': '1',
                'OptimizeReferences': '2',
                'EnableCOMDATFolding': '2',
              },
            },
          }],  # OS=="win"
        ],  # conditions
      },  # Release
    },  # configurations
  },  # target_defaults
}
