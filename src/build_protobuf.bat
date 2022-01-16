cd protobuf\cmake
mkdir build\solution
cd build\solution
cmake -G "Visual Studio 16 2019" -Dprotobuf_BUILD_TESTS=OFF -DCMAKE_INSTALL_PREFIX=.\out\ ..\..
msbuild INSTALL.vcxproj /property:Configuration=Release
