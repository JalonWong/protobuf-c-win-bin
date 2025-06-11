package(default_visibility = ["//visibility:public"])

cc_binary(
    name = "protoc-gen-c",
    srcs = glob([
        "*.cc",
        "*.h"
    ]),
    includes = ["."],
    deps = [
        "//protobuf-c:protobuf-c",
        "//protobuf-c:protobuf-c_cc_proto",
        "@protobuf//:protoc_lib",
        "//:ver",
    ],
)
