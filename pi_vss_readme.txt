VSS Setup on Raspberry Pi

Connect with Pi
ssh pi@raspberrypi.local

Copy folder
scp -rv <folder> pi@raspberrypi.local
:~/

To run VSS server on Pi follow:

sudo apt update
sudo apt install -y build-essential cmake git wget curl sqlite3 libsqlite3-dev nlohmann-json3-dev libcjson-dev

Install Cyclone DDS:

cd ~
git clone https://github.com/eclipse-cyclonedds/cyclonedds.git

cd cyclonedds
cmake ..
make
sudo make install

If "which idlc" does not give anything, run:
export PATH=$PATH:/usr/local/bin

Go to vss_topics.idl directory:

idlc -l c vss_topics.idl
(This generates vss_topics.c and vss_topics.h)

In the same directory:
mkdir build
cd build
cmake ..
make

Install Kuzu:

cd ~
git clone https://github.com/kuzudb/kuzu.git

cd kuzu
mkdir build
cd build
cmake .. -DENABLE_MALLOC_BUFFER_MANAGER=ON -DCMAKE_BUILD_TYPE=Release
make -j4
sudo make install
sudo ldconfig

Copy kuzu.hpp and kuzu.h to VSS_databroker/include:
cp kuzu.hpp ~/VSS_pi/VSS_databroker/include
cp kuzu.h ~/VSS_pi/VSS_databroker/include

Copy libkuzu.so to VSS_databroker/lib:
cp libkuzu.so ~/VSS_pi/VSS_databroker/lib

In the same directory build:
cmake -S . -B build
cmake --build build
