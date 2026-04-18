from conan import ConanFile
from conan.tools.files import copy, get
from textwrap import dedent

required_conan_version = ">=2.1"

class OpencvARMV8Conan(ConanFile):
  name = "opencv-armv8"
  version = "4.13.0"

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
      raise Exception("opencv-armv8 is Linux-only")
    if self.settings.arch != "armv8":
      raise Exception("opencv-armv8 is armv8-only")
    if not self.options.shared:
      raise Exception("opencv-armv8 is only available as a shared library")

  def source(self):
    url = f"https://s3.mrgi23.com/builds/opencv/{self.version}/{self.name}.tar.gz"
    get(self, url, strip_root=True)

  def build(self):
    pass

  def package(self):
    copy(self, "*", src=self.source_folder, dst=self.package_folder)

  def package_info(self):
    self.cpp_info.set_property("cmake_file_name", "OpenCV-armv8")
    self.cpp_info.set_property("cmake_target_name", "OpenCV-armv8::OpenCV-armv8")

    self.cpp_info.includedirs = ["include/opencv4"]
    self.cpp_info.libs = ["opencv_world"]

    self.cpp_info.description = dedent(f"""
    conanfile.txt Usage:
      [requires]
      {self.name}/{self.version}@mrgi/release

    CMake Usage:
      find_package(OpenCV REQUIRED)
      target_link_libraries(<target> OpenCV::OpenCV)

    Include:
      #include <opencv2/opencv.hpp>
    """)
