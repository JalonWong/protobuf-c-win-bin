load("//:c_proto.bzl", "c_proto_library")

package(default_visibility = ["//visibility:public"])

proto_library(
    name = "issue220_proto",
    srcs = ["issue220.proto"],
)
c_proto_library(
    name = "issue220_c_proto",
    deps = [":issue220_proto"],
)
cc_test(
    name = "issue220",
    srcs = glob(["*.c"]),
    deps = [":issue220_c_proto"],
)
