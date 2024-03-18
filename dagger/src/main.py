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

import dagger
from dagger import dag, function, object_type


@object_type
class Daggerverse:
    @function
    async def mypy(self, src: dagger.Directory) -> str:
        return await (
            dag.container()
            .from_("python:alpine")
            .with_mounted_directory("/mnt", src)
            .with_workdir("/mnt")
            .with_exec(["pip", "install", "mypy"])
            .with_exec(
                [
                    "apk",
                    "add",
                    "--no-cache",
                    "gcc",
                    "libc-dev",
                    "linux-headers",
                    "libffi-dev",
                ]
            )
            .with_exec(["python", "--version"])
            .with_exec(["pip", "install", "wheel"])
            .with_exec(["pip", "install", "mypy"])
            .with_exec(["pip", "install", "-U", "-r", "test-requirements.txt"])
            .with_exec(["pip", "install", "-U", "-r", "requirements.txt"])
            .with_exec(["mypy", "--non-interactive", "--install-types", "."])
        ).stdout()
