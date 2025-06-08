import subprocess
import sys
import os
import shutil
import zipfile
import platform
from glob import glob


PYTHON = sys.executable


def build_protoc() -> None:
    print("---------------------------------------------------------------------------")
    print("---- Build protoc ---------------------------------------------------------")
    print("---------------------------------------------------------------------------", flush=True)
    subprocess.run(
        "bazel build @protobuf//:protoc".split(),
        check=True,
    )


def build_protobuf_c() -> None:
    print("---------------------------------------------------------------------------")
    print("---- Build protobuf-c -----------------------------------------------------")
    print("---------------------------------------------------------------------------", flush=True)
    subprocess.run(
        [
            "bazel-bin/external/protobuf+/protoc.exe",
            "-I=protobuf-c",
            "-I=bazel-protobuf-c/external/protobuf+/src",
            "--cpp_out=protobuf-c",
            "protobuf-c.proto",
        ],
        check=True,
    )
    subprocess.run("bazel build //protoc-gen-c:protoc-gen-c".split(), check=True)


def test_protobuf_c() -> None:
    print("---------------------------------------------------------------------------")
    print("---- Test protobuf-c ------------------------------------------------------")
    print("---------------------------------------------------------------------------", flush=True)
    env = os.environ.copy()
    env["PATH"] = os.path.abspath("./bazel-bin/protoc-gen-c") + ";" + env["PATH"]
    subprocess.run(
        [
            "bazel-bin/external/protobuf+/protoc.exe",
            "-I=t",
            "--c_out=t",
            "test-proto3.proto",
        ],
        check=True,
        env=env,
    )
    subprocess.run("bazel test //t:test".split(), check=True)


if __name__ == "__main__":
    subprocess.run([PYTHON, "--version"])
    subprocess.run("clang-cl --version".split(), check=True)
    subprocess.run("bazel --version".split(), check=True)

    print("---- Copy files ------------------------------------------------------")
    src = glob("src/**", recursive=True, include_hidden=True)
    for s in src:
        if os.path.isfile(s):
            print(s)
            shutil.copy(s, s.replace("src", "protobuf-c"))

    cwd = os.getcwd()
    os.chdir("protobuf-c")
    build_protoc()
    build_protobuf_c()
    test_protobuf_c()

    os.chdir(cwd)
    with zipfile.ZipFile("protobuf-c-win64.zip", "w", zipfile.ZIP_DEFLATED) as zip_f:
        zip_f.write("protobuf-c/bazel-bin/protoc-gen-c/protoc-gen-c.exe", "bin/protoc-gen-c.exe")
