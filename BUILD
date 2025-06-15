package(default_visibility = ["//visibility:public"])

config_setting(
    name = "msvc",
    flag_values = {"@bazel_tools//tools/cpp:compiler": "msvc-cl"},
)

config_setting(
    name = "env_protoc",
    define_values = {"c_proto_env_protoc": "true"},
)
