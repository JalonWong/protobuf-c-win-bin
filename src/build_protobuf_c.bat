protobuf\solution\Release\protoc.exe -I=protobuf-c\protobuf-c -I=protobuf\src --cpp_out=protobuf-c\protobuf-c protobuf-c.proto
cd protobuf-c
bazel build protoc-gen-c
cd ..
protobuf\solution\Release\protoc.exe --plugin=protobuf-c\bazel-bin\protoc-gen-c.exe -I=protobuf-c\t --c_out=protobuf-c\t test-proto3.proto
cd protobuf-c
bazel test test
