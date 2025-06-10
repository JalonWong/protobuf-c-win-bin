load("//:c_proto.bzl", "c_proto_library")

package(default_visibility = ["//visibility:public"])

proto_library(
    name = "issue204_proto",
    srcs = ["issue204.proto"],
    deps = ["//protobuf-c:protobuf-c_proto"],
)
c_proto_library(
    name = "issue204_c_proto",
    deps = [":issue204_proto"],
)
cc_test(
    name = "issue204",
    srcs = glob(["*.c"]),
    deps = [":issue204_c_proto"],
)
