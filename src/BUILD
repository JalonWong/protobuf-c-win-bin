package(default_visibility = ["//visibility:public"])

cc_binary(
    name = "protoc-gen-c",
    srcs = glob(["protoc-c/*.cc"]),
    copts = [
        "/wd4267",
        "/wd4244",
    ],
    defines = ["PACKAGE_STRING=\\\"protobuf-c\\\""],
    includes = [
        "protobuf-c",
        "protoc-c",
    ],
    deps = [
        "//protobuf-c:protobuf-c-pb",
    ],
)

filegroup(
    name = "all",
    srcs = [
        ":protoc-gen-c",
    ],
)

cc_test(
    name = "test",
    srcs = [
        "t/generated-code/test-generated-code.c",
    ] + glob(["t/*.pb-c.c"]),
    defines = ["PROTO3"],
    includes = [
        "protobuf-c",
        "t",
    ],
    deps = [
        "//protobuf-c",
    ],
)
