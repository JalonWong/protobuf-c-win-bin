package(default_visibility = ["//visibility:public"])

cc_library(
    name = "protobuf_c",
    srcs = ["protobuf-c/protobuf-c.c"],
    hdrs = ["protobuf-c/protobuf-c.h"],
    includes = ["."],
    defines = select({
        "//:no_std": ["PROTOBUF_C_NO_STD"],
        "//conditions:default": [],
    }),
)
