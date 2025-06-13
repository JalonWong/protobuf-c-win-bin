
def _impl(ctx):
    proto = ctx.attr.deps[0][ProtoInfo]

    proto_files = proto.direct_sources
    output_dir = ctx.genfiles_dir.path

    outputs = []
    for proto_file in proto_files:
        base_name = proto_file.basename[:-6]  # remove .proto suffix
        outputs.append(ctx.actions.declare_file(base_name + ".pb-c.h"))
        outputs.append(ctx.actions.declare_file(base_name + ".pb-c.c"))

    protoc_c = ctx.executable._protoc_c

    args = ctx.actions.args()
    args.add("--plugin=protoc-gen-c=" + protoc_c.path)
    args.add("--c_out=" + output_dir)
    args.add_all(["-I" + p for p in proto.transitive_proto_path.to_list()])
    args.add_all([proto_file.path for proto_file in proto_files])
    # print(args)

    ctx.actions.run(
        inputs = proto.transitive_sources,
        outputs = outputs,
        executable = ctx.executable._protoc,
        tools = [protoc_c],
        arguments = [args],
        mnemonic = "ProtoCompile",
        progress_message = "Generating C proto files for %s" % ctx.label,
    )

    return [DefaultInfo(files = depset(outputs))]

_proto_c = rule(
    implementation = _impl,
    attrs = {
        "deps": attr.label_list(
            mandatory = True,
            providers = [ProtoInfo],
        ),
        "_protoc": attr.label(
            default = "@protobuf//:protoc",
            executable = True,
            cfg = "exec",
        ),
        "_protoc_c": attr.label(
            default = "//out:proto_c",
            executable = True,
            cfg = "exec",
        ),
    },
    provides = [DefaultInfo],
)

def c_proto_library(name, deps = []):
    name_pb = name + "_pb"
    _proto_c(
        name = name_pb,
        deps = deps,
    )

    native.cc_library(
        name = name,
        srcs = [name_pb],
        includes = ["."],
        deps = ["//protobuf-c:protobuf-c"],
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
