MKDIR = mkdir build
COPY = cp source/* ./build
all: build source
source: build
	${COPY}
build: 
	${MKDIR} && cp sample_puzzels/* ./build
clean:
	rm -rf build

	
