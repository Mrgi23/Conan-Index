from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout
from conan.tools.files import get, rmdir
from conan.tools.build import check_min_cppstd
from conan.tools.files import collect_libs
import os

required_conan_version = ">=2.1"


class OpenCVAarch64Conan(ConanFile):
    name = "opencv-aarch64"
    version = "4.13.0"

    license = "Apache-2.0"
    homepage = "https://opencv.org"
    description = "OpenCV (minimal, aarch64-optimized build: core+imgproc+imgcodecs+highgui+video)"
    url = "https://github.com/Mrgi23/Conan-Index/"
    topics = ("computer-vision", "image-processing", "aarch64", "neon")

    package_type = "library"
    settings = "os", "arch", "compiler", "build_type"

    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "parallel": ["tbb", "openmp"],
        "with_jpeg": [True, False],
        "with_png": [True, False],
        "with_dnn": [True, False],
    }

    default_options = {
        "shared": True,
        "fPIC": True,
        "parallel": "openmp",
        "with_jpeg": True,
        "with_png": True,
        "with_dnn": True,
    }

    short_paths = True

    def layout(self):
        cmake_layout(self)

    def configure(self):
        if self.settings.os != "Linux":
            raise Exception("opencv-aarch64 is Linux-only")
        if self.settings.arch != "armv8":
            raise Exception("opencv-aarch64 is aarch64-only (arch=armv8)")
        if self.settings.compiler.get_safe("cppstd"):
            check_min_cppstd(self, 11)

    def requirements(self):
        self.requires("zlib/[>=1.2.11 <2]")
        if self.options.with_jpeg:
            self.requires("libjpeg/[>=9e]")
        if self.options.with_png:
            self.requires("libpng/[>=1.6 <2]")
        if self.options.parallel == "tbb":
            self.requires("onetbb/2021.10.0")
        if self.options.with_dnn:
            self.requires("protobuf/3.21.12", transitive_libs=True)

    def source(self):
        # Minimal: fetch OpenCV + contrib if you need it; here core repo only
        get(self,
            url="https://github.com/opencv/opencv/archive/refs/tags/4.13.0.tar.gz",
            strip_root=True)

    def generate(self):
        tc = CMakeToolchain(self)

        # Install layout
        tc.variables["OPENCV_CONFIG_INSTALL_PATH"] = "cmake"
        tc.variables["OPENCV_BIN_INSTALL_PATH"] = "bin"
        tc.variables["OPENCV_LIB_INSTALL_PATH"] = "lib"
        tc.variables["OPENCV_3P_LIB_INSTALL_PATH"] = "lib"
        tc.variables["OPENCV_OTHER_INSTALL_PATH"] = "res"
        tc.variables["OPENCV_LICENSES_INSTALL_PATH"] = "licenses"

        tc.variables["BUILD_DOCS"] = False
        tc.variables["BUILD_EXAMPLES"] = False
        tc.variables["BUILD_TESTS"] = False
        tc.variables["BUILD_PERF_TESTS"] = False
        tc.variables["BUILD_opencv_apps"] = False
        tc.variables["BUILD_opencv_java"] = False
        tc.variables["BUILD_opencv_js"] = False
        tc.variables["BUILD_opencv_python2"] = False
        tc.variables["BUILD_opencv_python3"] = False
        tc.variables["BUILD_opencv_ts"] = False
        tc.variables["OPENCV_PYTHON_SKIP_DETECTION"] = True

        tc.variables["CPU_BASELINE"] = "NEON"
        tc.variables["CPU_DISPATCH"] = "VFPV4"

        tc.variables["WITH_OPENGL"] = True
        tc.variables["WITH_GTK"] = False
        tc.variables["WITH_GTK_2_X"] = False

        tc.variables["WITH_TBB"] = self.options.parallel == "tbb"
        tc.variables["WITH_OPENMP"] = self.options.parallel == "openmp"

        tc.variables["WITH_OPENCL"] = False
        tc.variables["WITH_V4L"] = False
        tc.variables["WITH_FFMPEG"] = False
        tc.variables["WITH_GSTREAMER"] = False
        tc.variables["WITH_VULKAN"] = False
        tc.variables["WITH_QT"] = False
        tc.variables["WITH_WAYLAND"] = False

        tc.variables["WITH_JPEG"] = bool(self.options.with_jpeg)
        tc.variables["WITH_PNG"] = bool(self.options.with_png)
        tc.variables["WITH_TIFF"] = False
        tc.variables["WITH_WEBP"] = False
        tc.variables["WITH_OPENEXR"] = False
        tc.variables["WITH_JASPER"] = False
        tc.variables["WITH_OPENJPEG"] = False
        tc.variables["WITH_GDAL"] = False
        tc.variables["WITH_GDCM"] = False

        tc.variables["BUILD_opencv_dnn"] = bool(self.options.with_dnn)
        tc.variables["WITH_PROTOBUF"] = bool(self.options.with_dnn)
        tc.variables["WITH_OPENVINO"] = False
        tc.variables["OPENCV_DNN_CUDA"] = False

        tc.variables["BUILD_opencv_core"] = True
        tc.variables["BUILD_opencv_imgproc"] = True
        tc.variables["BUILD_opencv_imgcodecs"] = True
        tc.variables["BUILD_opencv_highgui"] = True
        tc.variables["BUILD_opencv_video"] = True

        disable_modules = [
            "calib3d", "features2d", "flann", "ml", "objdetect",
            "photo", "stitching", "videoio",
            "aruco", "bgsegm", "bioinspired", "ccalib", "datasets",
            "face", "freetype", "fuzzy", "hdf", "hfs", "img_hash",
            "line_descriptor", "optflow", "ovis", "phase_unwrapping",
            "plot", "quality", "reg", "rgbd", "saliency", "sfm",
            "shape", "stereo", "structured_light", "superres",
            "surface_matching", "text", "tracking", "videostab",
            "viz", "wechat_qrcode", "xfeatures2d", "ximgproc",
            "xobjdetect", "xphoto",
        ]
        for m in disable_modules:
            tc.variables[f"BUILD_opencv_{m}"] = False

        tc.variables["BUILD_SHARED_LIBS"] = bool(self.options.shared)
        tc.variables["ENABLE_PIC"] = bool(self.options.fPIC)

        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()
        rmdir(self, os.path.join(self.package_folder, "share"))

    def package_info(self):
        self.cpp_info.libs = collect_libs(self)
