from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.files import copy, get, rmdir
import os
from textwrap import dedent

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
    copy(self, "LICENSE", src=self.source_folder, dst=os.path.join(self.package_folder, "licenses"))
    rmdir(self, os.path.join(self.package_folder, "share"))

  def package_info(self):
    self.cpp_info.set_property("cmake_file_name", f"{self.name}")
    self.cpp_info.set_property("cmake_target_name", f"{self.name}::{self.name}")

    self.cpp_info.includedirs = ["include"]
    self.cpp_info.libs = ["armadillo"]

    self.cpp_info.description = dedent(f"""
      conanfile.txt Usage:
        [requires]
        {self.name}/{self.version}@mrgi/release

        [generators]
        CMakeDeps
        CMakeToolchain

        [layout]
        cmake_layout

      CMake Usage:
        find_package(Armadillo REQUIRED)
        target_link_libraries(<target> Armadillo::Armadillo)

      Include:
        #include <armadillo>
    """)
