package(default_visibility = ["//visibility:public"])

config_setting(
    name = "msvc",
    flag_values = {"@bazel_tools//tools/cpp:compiler": "msvc-cl"},
)

config_setting(
    name = "no_std",
    define_values = {"c_proto_no_std": "true"},
)

config_setting(
    name = "env_protoc",
    define_values = {"c_proto_env_protoc": "true"},
)

alias(
    name = "protobuf_c",
    actual = "//src:protobuf_c",
)

alias(
    name = "protobuf-c_proto",
    actual = "//proto/protobuf-c:protobuf-c_proto",
)
