""" Generate protobuf C code """

load("@bazel_tools//tools/cpp:toolchain_utils.bzl", "find_cpp_toolchain", "use_cpp_toolchain")

def cc_library_func(ctx, name, hdrs, srcs, copts, dep_ccinfos, includes = []):
    compilation_contexts = [info.compilation_context for info in dep_ccinfos]
    linking_contexts = [info.linking_context for info in dep_ccinfos]
    toolchain = find_cpp_toolchain(ctx)
    feature_configuration = cc_common.configure_features(
        ctx = ctx,
        cc_toolchain = toolchain,
        requested_features = ctx.features,
        unsupported_features = ctx.disabled_features,
    )

    (compilation_context, compilation_outputs) = cc_common.compile(
        actions = ctx.actions,
        feature_configuration = feature_configuration,
        cc_toolchain = toolchain,
        name = name,
        srcs = srcs,
        includes = includes,
        public_hdrs = hdrs,
        user_compile_flags = copts,
        compilation_contexts = compilation_contexts,
    )

    # buildifier: disable=unused-variable
    (linking_context, linking_outputs) = cc_common.create_linking_context_from_compilation_outputs(
        actions = ctx.actions,
        name = name,
        feature_configuration = feature_configuration,
        cc_toolchain = toolchain,
        compilation_outputs = compilation_outputs,
        linking_contexts = linking_contexts,
        disallow_dynamic_library = cc_common.is_enabled(feature_configuration = feature_configuration, feature_name = "targets_windows") or not cc_common.is_enabled(feature_configuration = feature_configuration, feature_name = "supports_dynamic_linker"),
    )

    return CcInfo(
        compilation_context = compilation_context,
        linking_context = linking_context,
    )

def c_proto_aspect_impl(target, ctx):
    if ctx.var.get("c_proto_env_protoc", "false") == "true":
        protoc = "protoc"
        use_env_exec = True
    else:
        protoc = ctx.executable._protoc
        plugin = ctx.executable._plugin
        # protoc = ctx.rule.executable._proto_compiler
        use_env_exec = False

    proto_info = target[ProtoInfo]

    proto_files = proto_info.direct_sources
    output_dir = proto_info.proto_source_root
    if output_dir == ".":
        output_dir = ctx.genfiles_dir.path

    srcs = []
    hdrs = []
    for proto_file in proto_files:
        # remove .proto suffix
        base_name = proto_file.basename[:-6]
        hdrs.append(ctx.actions.declare_file(base_name + ".pb-c.h", sibling = proto_file))
        srcs.append(ctx.actions.declare_file(base_name + ".pb-c.c", sibling = proto_file))

    outputs = srcs + hdrs

    if proto_files[0].basename == "protobuf-c.proto":
        for o in outputs:
            ctx.actions.write(o, "// Useless")
    else:
        args = ctx.actions.args()
        if not use_env_exec:
            args.add("--plugin=protoc-gen-c=" + plugin.path)
        args.add("--c_out=" + output_dir)
        args.add_all(["-I" + p for p in proto_info.transitive_proto_path.to_list()])
        args.add_all([proto_file.path for proto_file in proto_files])
        # print(args)

        ctx.actions.run(
            inputs = proto_info.transitive_sources,
            outputs = outputs,
            executable = protoc,
            tools = [plugin],
            arguments = [args],
            mnemonic = "ProtoCompile",
            progress_message = "Generating C proto {}".format(ctx.label),
            use_default_shell_env = use_env_exec,
        )

    if ctx.var.get("C_COMPILER", "") == "msvc-cl":
        copts = ["/utf-8"]
    else:
        copts = []

    dep_ccinfos = [dep[CcInfo] for dep in (ctx.attr._c_deps + ctx.rule.attr.deps)]

    return cc_library_func(
        ctx = ctx,
        name = ctx.label.name,
        hdrs = hdrs,
        srcs = srcs,
        copts = copts,
        dep_ccinfos = dep_ccinfos,
        includes = [output_dir],
    )

_c_proto_aspect = aspect(
    implementation = c_proto_aspect_impl,
    attr_aspects = ["deps"],
    fragments = ["cpp", "proto"],
    required_providers = [ProtoInfo],
    provides = [CcInfo],
    toolchains = use_cpp_toolchain(),
    attrs = {
        "_c_deps": attr.label_list(
            default = ["@protobuf_c//:protobuf_c"],
        ),
        "_protoc": attr.label(
            default = "@get_protoc_//:bin",
            executable = True,
            cfg = "exec",
        ),
        "_plugin": attr.label(
            default = "@protobuf_c//:bin",
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
            aspects = [_c_proto_aspect],
            providers = [ProtoInfo],
            allow_files = False,
        ),
    },
    provides = [CcInfo],
)
