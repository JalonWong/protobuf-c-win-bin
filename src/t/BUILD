package(default_visibility = ["//visibility:public"])

cc_test(
    name = "test1-3",
    srcs = [
        "generated-code/test-generated-code.c",
        "test-proto3.pb-c.c",
    ],
    defines = ["PROTO3"],
    includes = ["."],
    deps = ["//protobuf-c"],
)

cc_test(
    name = "test1-2",
    srcs = [
        "generated-code/test-generated-code.c",
        "test.pb-c.c",
    ],
    includes = ["."],
    deps = ["//protobuf-c"],
)

cc_proto_library(
    name = "test-full_cc_proto",
    deps = [":test-full_proto"],
)
proto_library(
    name = "test-full_proto",
    srcs = ["test-full.proto"],
    deps = ["//protobuf-c:protobuf-c_proto"],
)

cc_binary(
    name = "gen2",
    srcs = [
        "generated-code2/cxx-generate-packed-data.cc",
    ],
    includes = ["."],
    deps = [":test-full_cc_proto"],
)

cc_test(
    name = "test2",
    srcs = [
        "generated-code2/test-generated-code2.c",
        "test-full.pb-c.c",
        "test-optimized.pb-c.c",
    ],
    includes = [
        ".",
        "generated-code2",
    ],
    deps = ["//protobuf-c"],
)
