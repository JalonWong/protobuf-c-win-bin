import subprocess
import sys
import os
import platform
import shutil
from glob import glob


PYTHON = sys.executable
SYSTEM = platform.system().lower()
EXT = ".exe" if SYSTEM == "windows" else ""


def build_protobuf_c() -> None:
    print("---------------------------------------------------------------------------")
    print("---- Build protobuf-c -----------------------------------------------------")
    print("---------------------------------------------------------------------------", flush=True)
    subprocess.run(f"bazel build --config={SYSTEM} //protoc-gen-c:protoc-gen-c".split(), check=True)
    shutil.copy("bazel-bin/protoc-gen-c/protoc-gen-c" + EXT, "./t/")


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
        "\"t/issue251/issue251.pb-c.h\"",
        "\"t/issue204/issue204.pb-c.h\"",
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
    subprocess.run(f"bazel test --config={SYSTEM} //t/...".split(), check=True)


if __name__ == "__main__":
    subprocess.run([PYTHON, "--version"])
    subprocess.run("bazel --version".split(), check=True)
    if SYSTEM == "windows":
        subprocess.run("clang-cl --version".split(), check=True)

    print("---- Copy files ------------------------------------------------------")
    src = glob("src/**", recursive=True, include_hidden=True)
    for s in src:
        if os.path.isfile(s):
            print(s)
            shutil.copy(s, s.replace("src", "protobuf-c"))

    cwd = os.getcwd()
    os.chdir("protobuf-c")
    build_protobuf_c()
    test_protobuf_c()

    os.chdir(cwd)
    if SYSTEM == "windows":
        import zipfile
        with zipfile.ZipFile("protobuf-c-windows-amd64.zip", "w", zipfile.ZIP_DEFLATED) as zip_f:
            zip_f.write("protobuf-c/t/protoc-gen-c.exe", "bin/protoc-gen-c.exe")
            zip_f.write("protobuf-c/protobuf-c/protobuf-c.c", "src/protobuf-c.c")
            zip_f.write("protobuf-c/protobuf-c/protobuf-c.h", "src/protobuf-c.h")
    elif SYSTEM == "linux":
        import tarfile
        with tarfile.open("protobuf-c-linux-amd64.tar.gz", "w:gz") as tar:
            tar.add("protobuf-c/t/protoc-gen-c", arcname="bin/protoc-gen-c")
            tar.add("protobuf-c/protobuf-c/protobuf-c.c", arcname="src/protobuf-c.c")
            tar.add("protobuf-c/protobuf-c/protobuf-c.h", arcname="src/protobuf-c.h")
