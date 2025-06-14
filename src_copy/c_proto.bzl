load("@bazel_tools//tools/cpp:toolchain_utils.bzl", "find_cpp_toolchain", "use_cpp_toolchain")
load("@rules_c_proto//:base.bzl", "c_proto_aspect_impl")

__c_proto_aspect = aspect(
    implementation = c_proto_aspect_impl,
    attr_aspects = ["deps"],
    fragments = ["cpp", "proto"],
    required_providers = [ProtoInfo],
    provides = [CcInfo],
    toolchains = use_cpp_toolchain(),
    attrs = {
        "_c_deps": attr.label_list(
            default = ["@protobuf_c//protobuf-c:protobuf-c"],
        ),
        "_protoc": attr.label(
            default = "@protobuf//:protoc",
            executable = True,
            cfg = "exec",
        ),
        "_plugin": attr.label(
            default = "@protobuf_c//out:proto_c",
            executable = True,
            cfg = "exec",
        ),
    },
)

def _impl(ctx):
    return [ctx.attr.deps[0][CcInfo]]

c_proto_library = rule(
    implementation = _impl,
    attrs = {
        "deps": attr.label_list(
            # use aspect to avoid generating conflict
            aspects = [__c_proto_aspect],
            providers = [ProtoInfo],
            allow_files = False,
        ),
    },
    provides = [CcInfo],
)

def _get_compiler_info_impl(ctx):
    toolchain = ctx.toolchains["@bazel_tools//tools/cpp:toolchain_type"]
    compiler = toolchain.cc.compiler_executable
    output_file = ctx.actions.declare_file(ctx.label.name + ".txt")
    ctx.actions.write(
        output = output_file,
        content = "Compiler: {}".format(compiler),
    )
    return [DefaultInfo(files = depset([output_file]))]

get_compiler_info = rule(
    implementation = _get_compiler_info_impl,
    toolchains = ["@bazel_tools//tools/cpp:toolchain_type"],
)
