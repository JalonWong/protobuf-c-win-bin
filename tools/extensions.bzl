load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")
load("//tools:tools_reg.bzl", "PROTOC", "PROTOC_C")

def get_tool(ctx, tools):
    if "windows" in ctx.os.name:
        key = "windows"
    elif "mac" in ctx.os.name:
        key = "macos"
    else:
        key = ctx.os.name

    if ctx.os.arch == "x86_64":
        key = key + "-amd64"
    else:
        key = key + "-" + ctx.os.arch

    if key not in tools:
        key = "linux-amd64"

    return tools[key]

def _get_protoc_impl(ctx):
    t = get_tool(ctx, PROTOC)
    http_archive(
        name = "get_protoc_",
        url = t["url"],
        sha256 = t["sha256"],
        build_file = "//:tools/bin.BUILD",
    )

get_protoc = module_extension(
    implementation = _get_protoc_impl,
)

def _get_protoc_c_impl(ctx):
    t = get_tool(ctx, PROTOC_C)
    http_archive(
        name = "get_protoc_c_",
        url = t["url"],
        sha256 = t["sha256"],
        build_file = "//:tools/bin.BUILD",
    )

get_protoc_c = module_extension(
    implementation = _get_protoc_c_impl,
)
