load("//:c_proto.bzl", "c_proto_library")

package(default_visibility = ["//visibility:public"])

proto_library(
    name = "issue389_proto",
    srcs = ["issue389.proto"],
)
c_proto_library(
    name = "issue389_c_proto",
    deps = [":issue389_proto"],
)
