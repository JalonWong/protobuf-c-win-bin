package(default_visibility = ["//visibility:public"])

cc_proto_library(
    name = "protobuf-c_cc_proto",
    deps = [":protobuf-c_proto"],
)
proto_library(
    name = "protobuf-c_proto",
    srcs = ["protobuf-c.proto"],
    deps = ["@protobuf//:descriptor_proto"],
)

cc_library(
    name = "protobuf-c",
    srcs = [
        "protobuf-c.c",
    ],
    hdrs = [
        "protobuf-c.h",
    ],
    includes = [
        ".",
    ],
)
