load("//:c_proto.bzl", "c_proto_library")

package(default_visibility = ["//visibility:public"])

proto_library(
    name = "issue375_proto",
    srcs = ["issue375.proto"],
)
c_proto_library(
    name = "issue375_c_proto",
    deps = [":issue375_proto"],
)
cc_test(
    name = "issue375",
    srcs = glob(["*.c"]),
    deps = [":issue375_c_proto"],
)
