#include "miniposix/unique_fd.hpp"

#include <unistd.h>

namespace miniposix {

UniqueFd::UniqueFd(int fd) noexcept {
    // TODO: Adopt fd, including descriptor 0. Only -1 means empty.
    (void)fd;
}

UniqueFd::~UniqueFd() noexcept {
    // TODO: Close the owned descriptor, if any.
}

UniqueFd::UniqueFd(UniqueFd&& other) noexcept {
    // TODO: Transfer ownership from other; leave other empty.
    (void)other;
}

UniqueFd& UniqueFd::operator=(UniqueFd&& other) noexcept {
    // TODO: Release any descriptor currently owned by *this, then transfer
    // other. Self move assignment must be safe.
    (void)other;
    return *this;
}

int UniqueFd::get() const noexcept {
    return fd_;
}

int UniqueFd::release() noexcept {
    // TODO: Return the descriptor without closing it; leave *this empty.
    return -1;
}

void UniqueFd::reset(int fd) noexcept {
    // TODO: Close the current descriptor and adopt fd. Handle reset(get()).
    (void)fd;
}

} // namespace miniposix
