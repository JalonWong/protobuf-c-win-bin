package(default_visibility = ["//visibility:public"])

filegroup(
    name = "bin",
    srcs = glob(["bin/*"]),
)

config_setting(
    name = "no_std",
    define_values = {"protobuf_c_no_std": "true"},
)

alias(
    name = "protobuf_c",
    actual = "//src:protobuf_c",
)

alias(
    name = "protobuf-c_proto",
    actual = "//proto/protobuf-c:protobuf-c_proto",
)
