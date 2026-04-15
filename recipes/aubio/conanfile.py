from conan import ConanFile
from conan.tools.files import chdir, copy, download, get, rmdir
import os
from textwrap import dedent

required_conan_version = ">=2.1"

class AubioConan(ConanFile):
  name = "aubio"
  version = "0.4.9"

  license = "GPL-3.0-or-later"
  homepage = "https://aubio.org/"
  description = "A library for audio and music analysis"
  url = "https://github.com/Mrgi23/Conan-Index/"
  topics = ("audio", "dsp", "onset", "pitch", "beat")

  package_type = "library"
  settings = "os", "arch", "compiler", "build_type"

  options = {
    "shared": [True, False],
    "fftw": [True, False],
    "samplerate": [True, False],
    "sndfile": [True, False]
  }

  default_options = {
    "shared": True,
    "fftw": False,
    "samplerate": False,
    "sndfile": False
  }

  short_paths = True

  def layout(self):
    self.folders.source = "."
    self.folders.build = "build"

  def configure(self):
    if self.settings.os != "Linux":
      raise Exception("aubio is Linux-only")
    if not self.options.shared:
      raise Exception("aubio must be built as a shared library")

  def requirements(self):
    if self.options.fftw:
      self.requires("fftw/3.3.10")
    if self.options.samplerate:
      self.requires("libsamplerate/0.2.2")
    if self.options.sndfile:
      self.requires("libsndfile/1.2.2")

  def source(self):
    get(self, url=f"https://github.com/aubio/aubio/archive/refs/tags/{self.version}.tar.gz", strip_root=True)

    waf_url = "https://waf.io/waf-2.0.25"
    waf_path = os.path.join(self.source_folder, "waf")
    download(self, waf_url, waf_path)
    os.chmod(waf_path, 0o755)

  def build(self):
    with chdir(self, self.source_folder):
      self.run("make configure PREFIX=/usr")
      self.run("make -j{}".format(self.conf.get('tools.build:jobs', 1)))

  def package(self):
    with chdir(self, self.source_folder):
      self.run("make install DESTDIR={}".format(self.package_folder))

    mappings = [
      ("usr/local/bin", "bin"),
      ("usr/local/include", "include"),
      ("usr/local/lib", "lib"),
    ]

    for src_rel, dst_rel in mappings:
      src = os.path.join(self.package_folder, src_rel)
      dst = os.path.join(self.package_folder, dst_rel)
      if os.path.exists(src):
        os.makedirs(dst, exist_ok=True)
        copy(self, "*", src=src, dst=dst)

    usr_dir = os.path.join(self.package_folder, "usr")
    rmdir(self, usr_dir)

    copy(self, "LICENSE", dst=os.path.join(self.package_folder, "licenses"), src=self.source_folder)

  def package_info(self):
    self.cpp_info.set_property("cmake_file_name", f"{self.name}")
    self.cpp_info.set_property("cmake_target_name", f"{self.name}::{self.name}")

    self.cpp_info.includedirs = ["include"]
    self.cpp_info.libs = ["aubio"]

    self.cpp_info.description = dedent(f"""
    conanfile.txt Usage:
      [requires]
      {self.name}/{self.version}@mrgi/release

    CMake Usage:
      find_package(Aubio REQUIRED)
      target_link_libraries(<target> Aubio::Aubio)

    Include:
      #include <aubio/aubio.h>
    """)
