cd protobuf
mkdir solution
cd solution
cmake -G "Visual Studio 16 2019" -Dprotobuf_BUILD_TESTS=OFF -DCMAKE_INSTALL_PREFIX=.\out\ ..
msbuild protoc.vcxproj /property:Configuration=Release
