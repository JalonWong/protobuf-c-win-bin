filegroup(
    name = "proto_c",
    srcs = select({
        "@platforms//os:windows": ["protoc-gen-c.exe"],
        "//conditions:default": ["protoc-gen-c"],
    }),
    visibility = ["//visibility:public"],
)
