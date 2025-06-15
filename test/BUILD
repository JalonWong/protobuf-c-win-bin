load("@rules_c_proto//:base.bzl", "c_proto_library")

package(default_visibility = ["//visibility:public"])

proto_library(
    name = "test_proto",
    srcs = ["test.proto"],
    deps = [
        "//test/msg:msg_proto",
    ],
)
c_proto_library(
    name = "test_c_proto",
    deps = [":test_proto"],
)
cc_test(
    name = "test",
    srcs = ["test.cc"],
    deps = [
        ":test_c_proto",
        "@googletest//:gtest_main",
    ],
)

proto_library(
    name = "test2_proto",
    srcs = ["test2.proto"],
    deps = [
        ":test_proto",
        "//test/msg:msg_proto",
        "//test/base:types_proto",
    ],
)
c_proto_library(
    name = "test2_c_proto",
    deps = [":test2_proto"],
)
cc_test(
    name = "test2",
    srcs = ["test2.cc"],
    deps = [
        ":test2_c_proto",
        "@googletest//:gtest_main",
    ],
)

proto_library(
    name = "test-full_proto",
    srcs = ["test-full.proto"],
    deps = ["@protobuf_c//:protobuf-c_proto"],
)
c_proto_library(
    name = "test-full_c_proto",
    deps = [":test-full_proto"],
)
cc_test(
    name = "test-full",
    srcs = ["test-full.cc"],
    deps = [
        ":test-full_c_proto",
        "@googletest//:gtest_main",
    ],
)

test_suite(
    name = "tests",
    tests = [
        ":test",
        ":test2",
        ":test-full",
    ],
)
