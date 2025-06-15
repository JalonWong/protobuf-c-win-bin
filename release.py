import os
import platform
import shutil
import subprocess
import sys
from glob import glob

PYTHON = sys.executable
SYSTEM = platform.system().lower()
EXT = ".exe" if SYSTEM == "windows" else ""
if SYSTEM == "darwin":
    SYSTEM = "osx"
ARCH = platform.machine().lower()


def show_compiler_info() -> None:
    subprocess.run(f"bazel build --config={SYSTEM} //:compiler_info".split(), check=True)
    with open("bazel-bin/compiler_info.txt", "r") as f:
        cc = f.read().split(" ", maxsplit=1)[1].strip()
        if cc.startswith("external"):
            cc = "bazel-protobuf-c/" + cc
        print("---- Compiler info --------------------------------------------------", flush=True)
        subprocess.run([cc, "--version"], check=True)


def build_protobuf_c() -> None:
    print("---------------------------------------------------------------------------")
    print("---- Build protobuf-c -----------------------------------------------------")
    print("---------------------------------------------------------------------------", flush=True)
    subprocess.run(f"bazel build --config={SYSTEM} //protoc-gen-c:protoc-gen-c".split(), check=True)
    shutil.copy(f"bazel-bin/protoc-gen-c/protoc-gen-c{EXT}", "./out/")


def file_replace(file_path: str, old: str, new: str) -> None:
    with open(file_path, "r") as f:
        text = f.read()
        text = text.replace(old, new)
        with open(file_path, "w") as f:
            f.write(text)


def test_generate_file() -> None:
    file_replace(
        "t/generated-code2/cxx-generate-packed-data.cc",
        "if defined(_MSC_VER)",
        "ifndef INT32_MIN",
    )
    file_replace(
        "t/issue204/issue204.c",
        '"t/issue251/issue251.pb-c.h"',
        '"t/issue204/issue204.pb-c.h"',
    )

    subprocess.run(f"bazel build --config={SYSTEM} //t:gen2".split(), check=True)
    ret = subprocess.run("bazel-bin/t/gen2".split(), check=True, capture_output=True)
    with open("t/generated-code2/test-full-cxx-output.inc", "wb") as f:
        f.write(ret.stdout)


def test_protobuf_c() -> None:
    print("---------------------------------------------------------------------------")
    print("---- Test protobuf-c ------------------------------------------------------")
    print("---------------------------------------------------------------------------", flush=True)
    test_generate_file()
    subprocess.run(f"bazel test --config={SYSTEM} //t:tests".split(), check=True)


if __name__ == "__main__":
    print("machine:", ARCH, flush=True)
    subprocess.run([PYTHON, "--version"])
    subprocess.run("bazel --version".split(), check=True)

    print("---- Copy files ------------------------------------------------------", flush=True)
    os.makedirs("protobuf-c/out", exist_ok=True)
    src = glob("src_copy/**", recursive=True, include_hidden=True)
    for s in src:
        if os.path.isfile(s):
            print(s)
            shutil.copy(s, s.replace("src_copy", "protobuf-c"))

    cwd = os.getcwd()
    os.chdir("protobuf-c")
    with open(".gitignore", "a") as f:
        f.write("\n/bazel-*")
    if ARCH == "arm64":
        file_replace(".bazelrc", "x86_64", "arm64")
    show_compiler_info()
    build_protobuf_c()
    test_protobuf_c()

    os.chdir(cwd)
    if SYSTEM == "windows" or SYSTEM == "osx":
        import zipfile

        arch = "arm64" if ARCH == "arm64" else "amd64"
        with zipfile.ZipFile(f"protobuf-c-{SYSTEM}-{arch}.zip", "w", zipfile.ZIP_DEFLATED) as zip_f:
            zip_f.write(f"protobuf-c/out/protoc-gen-c{EXT}", f"bin/protoc-gen-c{EXT}")
            files = glob("pack_protobuf_c/**", recursive=True, include_hidden=True)
            for file in files:
                zip_f.write(file, file[len("pack_protobuf_c/"):])
    elif SYSTEM == "linux":
        import tarfile

        with tarfile.open("protobuf-c-linux-amd64.tar.gz", "w:gz") as tar:
            tar.add("protobuf-c/out/protoc-gen-c", "bin/protoc-gen-c")
            files = glob("pack_protobuf_c/*")
            for file in files:
                tar.add(file, file[len("pack_protobuf_c/"):])
