load("//:c_proto.bzl", "c_proto_library")

package(default_visibility = ["//visibility:public"])

proto_library(
    name = "issue745_proto",
    srcs = ["issue745.proto"],
)
c_proto_library(
    name = "issue745_c_proto",
    deps = [":issue745_proto"],
)
cc_test(
    name = "issue745",
    srcs = glob(["*.c"]),
    deps = [":issue745_c_proto"],
)
