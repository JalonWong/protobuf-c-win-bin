load("//:c_proto.bzl", "c_proto_library")

package(default_visibility = ["//visibility:public"])

proto_library(
    name = "test-full_proto",
    srcs = ["test-full.proto"],
    deps = ["//protobuf-c:protobuf-c_proto"],
)
cc_proto_library(
    name = "test-full_cc_proto",
    deps = [":test-full_proto"],
)
cc_binary(
    name = "gen2",
    srcs = [
        "generated-code2/cxx-generate-packed-data.cc",
        "generated-code2/common-test-arrays.h",
    ],
    includes = ["."],
    deps = [":test-full_cc_proto"],
)

proto_library(
    name = "test-proto3_proto",
    srcs = ["test-proto3.proto"],
)
c_proto_library(
    name = "test-proto3_c_proto",
    deps = [":test-proto3_proto"],
)
cc_test(
    name = "test1-3",
    srcs = ["generated-code/test-generated-code.c"],
    defines = ["PROTO3"],
    deps = [":test-proto3_c_proto"],
)

proto_library(
    name = "test_proto",
    srcs = ["test.proto"],
    deps = ["//protobuf-c:protobuf-c_proto"],
)
c_proto_library(
    name = "test_c_proto",
    deps = [":test_proto"],
)
cc_test(
    name = "test1-2",
    srcs = ["generated-code/test-generated-code.c"],
    deps = [":test_c_proto"],
)

proto_library(
    name = "test-optimized_proto",
    srcs = ["test-optimized.proto"],
)
c_proto_library(
    name = "test-optimized_c_proto",
    deps = [":test-optimized_proto"],
)
c_proto_library(
    name = "test-full_c_proto",
    deps = [":test-full_proto"],
)
cc_test(
    name = "test2",
    srcs = [
        "generated-code2/test-generated-code2.c",
        "generated-code2/test-full-cxx-output.inc",
        "generated-code2/common-test-arrays.h",
    ],
    deps = [
        ":test-full_c_proto",
        ":test-optimized_c_proto",
    ],
)

test_suite(
    name = "tests",
    tests = [
        ":test1-3",
        ":test1-2",
        ":test2",
        "//t/issue204",
        "//t/issue220",
        "//t/issue251",
        "//t/issue330",
        "//t/issue375",
        "//t/issue440",
        "//t/issue745",
        "//t/version",
    ],
)
