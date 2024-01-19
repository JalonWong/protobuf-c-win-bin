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
        ["bazel", "build", "@com_google_protobuf//:protoc"],
        check=True,
    )


def build_protobuf_c() -> None:
    print("---------------------------------------------------------------------------")
    print("---- Build protobuf-c -----------------------------------------------------")
    print("---------------------------------------------------------------------------", flush=True)
    subprocess.run(
        [
            "bazel-bin/external/com_google_protobuf/protoc.exe",
            "-I=protobuf-c",
            "-I=bazel-protobuf-c/external/com_google_protobuf/src",
            "--cpp_out=protobuf-c",
            "protobuf-c.proto",
        ],
        check=True,
    )
    subprocess.run("bazel build all".split(), check=True)


def test_protobuf_c() -> None:
    print("---------------------------------------------------------------------------")
    print("---- Test protobuf-c ------------------------------------------------------")
    print("---------------------------------------------------------------------------", flush=True)
    env = os.environ.copy()
    env["PATH"] = os.path.abspath("./bazel-bin") + ";" + env["PATH"]
    subprocess.run(
        [
            "bazel-bin/external/com_google_protobuf/protoc.exe",
            "-I=t",
            "--c_out=t",
            "test-proto3.proto",
        ],
        check=True,
        env=env,
    )
    subprocess.run("bazel test :test".split(), check=True)


if __name__ == "__main__":
    subprocess.run([PYTHON, "--version"])
    subprocess.run("bazel --version".split(), check=True)

    src = glob("src/*")
    for s in src:
        if os.path.isfile(s):
            shutil.copy(s, "protobuf-c/")

    shutil.copy("src/.bazelrc", "protobuf-c/")
    shutil.copy("src/protobuf-c/BUILD", "protobuf-c/protobuf-c/")

    cwd = os.getcwd()
    os.chdir("protobuf-c")
    build_protoc()
    build_protobuf_c()
    test_protobuf_c()

    os.chdir(cwd)
    with zipfile.ZipFile("protobuf-c-win64.zip", "w", zipfile.ZIP_DEFLATED) as zip_f:
        zip_f.write("protobuf-c/bazel-bin/protoc-gen-c.exe", "bin/protoc-gen-c.exe")
