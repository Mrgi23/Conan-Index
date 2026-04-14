from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.files import get, copy, rmdir
import os

class LiquidDSPConan(ConanFile):
    name = "liquid-dsp"
    version = "1.7.0"

    license = "MIT"
    description = "Digital signal processing library for software-defined radios"
    url = "https://github.com/jgaeddert/liquid-dsp"

    package_type = "library"
    settings = "os", "arch", "compiler", "build_type"

    options = {
        "shared": [True, False],
        "enable_simd": [True, False],
        "enable_logging": [True, False],
        "enable_color": [True, False],
        "find_fftw": [True, False]
    }

    default_options = {
        "shared": True,
        "enable_simd": True,
        "enable_logging": True,
        "enable_color": True,
        "find_fftw": False
    }

    short_paths = True

    def layout(self):
        cmake_layout(self)

    def requirements(self):
        if self.options.find_fftw:
            self.requires("fftw/3.3.10")

    def source(self):
        get(self, url=f"https://github.com/jgaeddert/liquid-dsp/archive/refs/tags/v{self.version}.tar.gz", strip_root=True)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["ENABLE_SIMD"] = self.options.enable_simd
        tc.variables["ENABLE_LOGGING"] = self.options.enable_logging
        tc.variables["ENABLE_COLOR"] = self.options.enable_color
        tc.variables["FIND_FFTW"] = self.options.find_fftw
        tc.variables["BUILD_EXAMPLES"] = False
        tc.variables["BUILD_AUTOTESTS"] = False
        tc.variables["BUILD_BENCHMARKS"] = False
        tc.variables["BUILD_SANDBOX"] = False
        tc.variables["BUILD_DOC"] = False
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
        self.cpp_info.libs = ["liquid"]
