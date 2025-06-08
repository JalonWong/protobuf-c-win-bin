package(default_visibility = ["//visibility:public"])

cc_binary(
    name = "protoc-gen-c",
    srcs = glob(["*.cc"]),
    defines = ["PACKAGE_STRING=\\\"protobuf-c\\\""],
    includes = [
        "//protobuf-c",
        ".",
    ],
    deps = [
        "//protobuf-c:protobuf-c-pb",
    ],
)
