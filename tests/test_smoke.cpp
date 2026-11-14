#include <gtest/gtest.h>

#include <unistd.h>

TEST(Smoke, CompilerAndTestRunnerWork) {
    static_assert(__cplusplus > 202002L, "The workshop requires C++23");
    EXPECT_GT(::getpid(), 0);
}
