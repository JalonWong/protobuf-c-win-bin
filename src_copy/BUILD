load("//:c_proto.bzl", "get_compiler_info")

package(default_visibility = ["//visibility:public"])

cc_library(
    name = "base",
    defines = [
        'PACKAGE_VERSION=\\"1.5.2\\"',
        'PACKAGE_STRING=\\"protobuf-c_1.5.2\\"',
    ],
)

get_compiler_info(
    name = "compiler_info"
)
