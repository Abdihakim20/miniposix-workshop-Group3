#include "miniposix/pipe.hpp"

#include <cerrno>
#include <system_error>
#include <unistd.h>

namespace miniposix {

Pipe Pipe::create() {
    int ends[2];
    if(::pipe(ends) != 0) {
        throw std::system_error(errno, std::generic_category(), "pipe");
    }

    Pipe created;
    created.read_end().reset(ends[0]);
    created.write_end().reset(ends[1]);
    return created;
}

} // namespace miniposix
