# protobuf-c Release

## protoc-gen-c Release
The compiled product of the [protobuf-c](https://github.com/protobuf-c/protobuf-c). See [Release](https://github.com/JalonWong/protobuf-c-release/releases)

### current submodule
- protobuf `v31.1`
- protobuf-c `v1.5.2`

## Getting Started with Bazel rules

`MODULE.bazel`
```py
bazel_dep(name = "rules_c_proto")
git_override(
    module_name="rules_c_proto",
    remote="https://github.com/JalonWong/protobuf-c-release.git",
    branch="main",
)
```

`BUILD`
```py
load("@rules_c_proto//:base.bzl", "c_proto_library")

proto_library(
    name = "test_proto",
    srcs = ["test.proto"],
)
c_proto_library(
    name = "test_c_proto",
    deps = [":test_proto"],
)
cc_binary(
    name = "app",
    deps = [":test_c_proto"],
)
```

### Options
It will download `protoc` and `protoc-gen-c` by default. If you want to use your pre-installed binary, add the following to your `.bazelrc`. You can also use it in the command line.
```sh
build --define=c_proto_env_protoc=true
```

If you don't want to use the heap in the std lib with your source code, for example embedded software, use the following.
```sh
build --define=c_proto_no_std=true
```
