import subprocess
import argparse
import os
import shutil
import zipfile
from glob import glob


def build_protobuf(cmake: bool) -> None:
    if cmake:
        os.makedirs("protobuf/solution", exist_ok=True)
        os.chdir("protobuf/solution")
        subprocess.run(
            'cmake -G "Visual Studio 16 2019" -Dprotobuf_BUILD_TESTS=OFF -DCMAKE_INSTALL_PREFIX=out ..',
            shell=True,
            check=True,
        )
        subprocess.run("msbuild protoc.vcxproj /property:Configuration=Release".split(), check=True)
    else:
        os.chdir("protobuf")
        subprocess.run("bazel build --enable_bzlmod=false :protoc".split(), check=True)


def build_protobuf_c(cmake: bool) -> None:
    if cmake:
        p = os.path.abspath("protobuf/solution/out/bin")
        os.makedirs("protobuf-c/build-cmake/build", exist_ok=True)
        os.chdir("protobuf-c/build-cmake/build")
        env = os.environ.copy()
        env["PATH"] = p + ";" + env["PATH"]
        subprocess.run("cmake -DCMAKE_INSTALL_PREFIX=out ..", shell=True, check=True)
        subprocess.run("msbuild INSTALL.vcxproj /property:Configuration=Release".split(), check=True)
    else:
        src = glob("src/*")
        for s in src:
            if os.path.isfile(s):
                shutil.copy(s, "protobuf-c/")

        shutil.copy("src/.bazelrc", "protobuf-c/")
        shutil.copy("src/protobuf-c/BUILD", "protobuf-c/protobuf-c/")

        subprocess.run(
            [
                "protobuf/solution/Release/protoc.exe",
                "-I=protobuf-c/protobuf-c",
                "-I=protobuf/src",
                "--cpp_out=protobuf-c/protobuf-c",
                "protobuf-c.proto",
            ],
            check=True,
        )
        os.chdir("protobuf-c")
        subprocess.run("bazel build all".split(), check=True)


def test_protobuf_c() -> None:
    subprocess.run(
        [
            "protobuf/solution/Release/protoc.exe",
            "--plugin=protobuf-c/bazel-bin/protoc-gen-c.exe",
            "-I=protobuf-c/t",
            "--c_out=protobuf-c/t",
            "test-proto3.proto",
        ],
        check=True,
    )
    os.chdir("protobuf-c")
    subprocess.run("bazel test :test".split(), check=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze .config to config.h")
    parser.add_argument("mode")
    parser.add_argument("--project", required=True, type=str)
    parser.add_argument("--cmake", action="store_true")
    args = parser.parse_args()

    if args.mode == "build":
        if args.project == "protobuf":
            build_protobuf(args.cmake)
        elif args.project == "protobuf-c":
            build_protobuf_c(args.cmake)
        else:
            raise ValueError("Unknown project")
    elif args.mode == "test":
        if args.project == "protobuf-c":
            test_protobuf_c()
        else:
            raise ValueError("Unknown project")
    elif args.mode == "pack":
        with zipfile.ZipFile("protobuf-c-win64.zip", "w", zipfile.ZIP_DEFLATED) as zip_f:
            zip_f.write("protobuf-c/bazel-bin/protoc-gen-c.exe", "bin/protoc-gen-c.exe")
    else:
        raise ValueError("Unknown mode")
