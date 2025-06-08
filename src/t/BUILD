package(default_visibility = ["//visibility:public"])

cc_test(
    name = "test",
    srcs = [
        "generated-code/test-generated-code.c",
    ] + glob(["*.pb-c.c"]),
    defines = ["PROTO3"],
    includes = [
        "//protobuf-c",
        ".",
    ],
    deps = [
        "//protobuf-c",
    ],
)
