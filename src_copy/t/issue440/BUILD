load("//:c_proto.bzl", "c_proto_library")

package(default_visibility = ["//visibility:public"])

proto_library(
    name = "issue440_proto",
    srcs = ["issue440.proto"],
)
c_proto_library(
    name = "issue440_c_proto",
    deps = [":issue440_proto"],
)
cc_test(
    name = "issue440",
    srcs = glob(["*.c"]),
    deps = [":issue440_c_proto"],
)
