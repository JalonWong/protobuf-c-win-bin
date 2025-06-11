
def _impl(ctx):
    proto = ctx.attr.deps[0][ProtoInfo]

    proto_files = proto.direct_sources
    output_dir = ctx.genfiles_dir.path

    outputs = []
    for proto_file in proto_files:
        base_name = proto_file.basename[:-6]  # remove .proto suffix
        outputs.append(ctx.actions.declare_file(base_name + ".pb-c.h"))
        outputs.append(ctx.actions.declare_file(base_name + ".pb-c.c"))

    args = ctx.actions.args()
    args.add("--c_out=" + output_dir)
    args.add_all(["-I" + p for p in proto.transitive_proto_path.to_list()])
    args.add_all([proto_file.path for proto_file in proto_files])
    # print(args)

    ctx.actions.run(
        inputs = proto_files,
        outputs = outputs,
        executable = ctx.executable._protoc,
        arguments = [args],
        mnemonic = "ProtoCompile",
        progress_message = "Generating C proto files for %s" % ctx.label,
        use_default_shell_env = True,
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
