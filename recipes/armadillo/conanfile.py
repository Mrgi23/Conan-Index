from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.files import copy, get, rmdir
import os

required_conan_version = ">=2.1"

class ArmadilloConan(ConanFile):
    name = "armadillo"
    version = "14.0.2"

    license = "Apache-2.0"
    description = "C++ linear algebra library"
    url = "https://arma.sourceforge.net/"

    package_type = "library"
    settings = "os", "compiler", "build_type", "arch"

    options = {
        "shared": [True, False],
        "use_blas": [True, False],
        "use_lapack": [True, False]
    }

    default_options = {
        "shared": True,
        "use_blas": True,
        "use_lapack": True
    }

    short_paths = True

    def layout(self):
        cmake_layout(self)

    def requirements(self):
        # Use system BLAS/LAPACK by default (safe)
        # If you want OpenBLAS, uncomment:
        # if self.options.use_blas or self.options.use_lapack:
        #     self.requires("openblas/0.3.23")
        pass

    def source(self):
        get(self, url=f"https://sourceforge.net/projects/arma/files/armadillo-{self.version}.tar.xz", strip_root=True)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["ARMA_USE_BLAS"] = "ON" if self.options.use_blas else "OFF"
        tc.variables["ARMA_USE_LAPACK"] = "ON" if self.options.use_lapack else "OFF"
        tc.generate()

        CMakeDeps(self).generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()
        copy(self, "LICENSE.txt", src=self.source_folder, dst=os.path.join(self.package_folder, "licenses"))
        rmdir(self, os.path.join(self.package_folder, "share"))

    def package_info(self):
        self.cpp_info.libs = ["armadillo"]
