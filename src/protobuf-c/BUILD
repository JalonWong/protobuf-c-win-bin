package(default_visibility = ["//visibility:public"])

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

cc_library(
    name = "protobuf-c-pb",
    srcs = [
        "protobuf-c.pb.cc",
    ],
    hdrs = [
        "protobuf-c.pb.h",
    ],
    includes = [
        ".",
    ],
    deps = [
        "@com_google_protobuf//:protoc_lib",
    ],
)
