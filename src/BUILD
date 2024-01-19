package(default_visibility = ["//visibility:public"])

cc_binary(
    name = "protoc-gen-c",
    srcs = glob(["protoc-c/*.cc"]) + [
        "protobuf-c/protobuf-c.pb.cc",
    ],
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
        "@com_google_protobuf//:protoc_lib",
    ],
)

cc_test(
    name = "test",
    srcs = [
        "protobuf-c/protobuf-c.c",
        "t/generated-code/test-generated-code.c",
    ] + glob(["t/*.pb-c.c"]),
    defines = ["PROTO3"],
    includes = [
        "protobuf-c",
        "t",
    ],
)
