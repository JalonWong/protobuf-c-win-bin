load("//:c_proto.bzl", "c_proto_library")

package(default_visibility = ["//visibility:public"])

proto_library(
    name = "issue251_proto",
    srcs = ["issue251.proto"],
)
c_proto_library(
    name = "issue251_c_proto",
    deps = [":issue251_proto"],
)
cc_test(
    name = "issue251",
    srcs = glob(["*.c"]),
    deps = [":issue251_c_proto"],
)
