cd protobuf-c\build-cmake
mkdir build
cd build
set PATH=..\..\..\protobuf\cmake\build\solution\out\bin;%PATH%
cmake -DCMAKE_INSTALL_PREFIX=.\out\ ..\
msbuild INSTALL.vcxproj /property:Configuration=Release
