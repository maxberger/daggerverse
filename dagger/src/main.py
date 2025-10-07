"""A generated module for Daggerverse functions

This module has been generated via dagger init and serves as a reference to
basic module structure as you get started with Dagger.

Two functions have been pre-created. You can modify, delete, or add to them,
as needed. They demonstrate usage of arguments and return types using simple
echo and grep commands. The functions can be called from the dagger CLI or
from one of the SDKs.

The first line in this comment block is a short description line and the
rest is a long description with more detail on the module's purpose or usage,
if appropriate. All modules should have a short description.
"""

import os
import sys

import dagger
from dagger import dag, function, object_type


@object_type
class Daggerverse:

    @function
    def python_container(self, src: dagger.Directory) -> dagger.Container:
        return (
            dag.container()
            .from_("python:alpine")
            .with_mounted_directory("/mnt", src)
            .with_workdir("/mnt")
            .with_exec(
                [
                    "apk",
                    "add",
                    "--no-cache",
                    "gcc",
                    "git",
                    "libc-dev",
                    "linux-headers",
                    "libffi-dev",
                ]
            )
            .with_exec(["python", "--version"])
            .with_exec(["pip", "install", "wheel", "mypy"])
        )

    @function
    def python_test_container(self, src: dagger.Directory) -> dagger.Container:
        return (
            self.python_container(src)
            .with_env_variable("CFLAGS", "-Wno-int-conversion")
            .with_exec(["pip", "install", "-U", "-r", "test-requirements.txt"])
            .with_exec(["pip", "install", "-U", "-r", "requirements.txt"])
        )

    @function
    def python_prod_container(self, src: dagger.Directory) -> dagger.Container:
        return self.python_container(src).with_exec(
            ["pip", "install", "-U", "-r", "requirements.txt"]
        )

    @function
    async def mypy(self, src: dagger.Directory) -> str:
        return (
            await self.python_test_container(src)
            .with_exec(["mypy", "--non-interactive", "--install-types", "."])
            .stdout()
        )

    @function
    async def pytest(self, src: dagger.Directory) -> str:
        return (
            await self.python_test_container(src)
            .with_exec(["python", "-m", "pytest", "tests/unit", "-rA"])
            .stdout()
        )

    @function
    async def python_test(self, src: dagger.Directory) -> str:
        return await self.mypy(src) + await self.pytest(src)

    @function
    async def python_release(
        self,
        src: dagger.Directory,
        twine_username: dagger.Secret,
        twine_password: dagger.Secret,
    ) -> str:
        return (
            await self.python_prod_container(src)
            .with_exec(["pip", "install", "-U", "build", "twine"])
            .with_exec(["python", "-m", "build"])
            .with_secret_variable("TWINE_PASSWORD", twine_password)
            .with_secret_variable("TWINE_USERNAME", twine_username)
            .with_exec(
                [
                    "python",
                    "-m",
                    "twine",
                    "upload",
                    "--repository-url",
                    "https://gitea.bergernet.de/api/packages/max/pypi",
                    "dist/*",
                ]
            )
            .stdout()
        )
