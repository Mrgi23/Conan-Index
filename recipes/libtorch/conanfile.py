from conan import ConanFile
from conan.tools.files import copy, get
from conan.tools.layout import basic_layout
from textwrap import dedent

required_conan_version = ">=2.1"

class LibTorchConan(ConanFile):
  name = "libtorch"
  version = "2.8.0-cu128"

  package_type = "library"
  settings = "os", "arch"

  options = {
    "shared": [True, False],
  }
  default_options = {
    "shared": True,
  }

  short_paths = True

  def configure(self):
    if self.settings.os != "Linux":
      raise Exception("libtorch is Linux-only")
    if self.settings.arch != "x86_64":
      raise Exception("libtorch is x86_64-only")
    if not self.options.shared:
      raise Exception("libtorch is only available as a shared library")

  def source(self):
    url = f"https://s3.mrgi23.com/builds/{self.name}/{self.version}/{self.name}.tar.gz"
    get(self, url, strip_root=True)

  def build(self):
    pass

  def package(self):
    copy(self, "*", src=self.source_folder, dst=self.package_folder)

  def package_info(self):
    self.cpp_info.set_property("cmake_file_name", "LibTorch")
    self.cpp_info.set_property("cmake_target_name", "LibTorch::LibTorch")

    self.cpp_info.includedirs = [
      "include",
      "include/torch/csrc/api/include",
    ]
    self.cpp_info.libs = [
      "torch",
      "torch_cpu",
      "torch_cuda",
      "c10",
      "c10_cuda",
      "torch_global_deps"
    ]

    self.cpp_info.description = dedent(f"""
    conanfile.txt Usage:
      [requires]
      {self.name}/{self.version}@mrgi/release

    CMake Usage:
      find_package(LibTorch REQUIRED)
      target_link_libraries(<target> LibTorch::LibTorch)

    Include:
      #include <torch/torch.h>
    """)
