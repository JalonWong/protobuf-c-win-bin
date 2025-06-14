load("//:c_proto.bzl", "c_proto_library")

package(default_visibility = ["//visibility:public"])

proto_library(
    name = "issue330_proto",
    srcs = ["issue330.proto"],
)
c_proto_library(
    name = "issue330_c_proto",
    deps = [":issue330_proto"],
)
cc_test(
    name = "issue330",
    srcs = glob(["*.c"]),
    deps = [
        ":issue330_c_proto",
        "//t/issue389:issue389_c_proto",
    ],
)
