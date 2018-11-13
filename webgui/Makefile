RM_COMMAND = rm -f

STD_FLAG = -std=c++14
CPP_FLAGS = -c
LD_LIBS = -L/usr/local/lib -lwthttp -lwt -lboost_system -lboost_thread \
					-lboost_filesystem -lboost_program_options
INCLUDE_FLAGS= -I/usr/local/include

SRCS = $(wildcard src/*.cpp)
OBJS = $(subst src/,build/,$(subst .cpp,.o,$(SRCS)))

all : radifi_gui

radifi_gui : $(OBJS)
	@echo $(OBJS)
	g++ $(STD_FLAG) -o radifi_gui $(OBJS) $(INCLUDE_FLAGS) \
	$(LD_LIBS)

build/%.o : src/%.cpp
	g++ -c $< $(CPP_FLAGS) -Iinclude $(STD_FLAG) -o $@

clean:
	$(RM_COMMAND) build/*.o

distclean : clean
	$(RM_COMMAND) radifi_gui
