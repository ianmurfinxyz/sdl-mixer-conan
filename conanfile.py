from conans import ConanFile, CMake, tools
import os, shutil

class SDLMixerConan(ConanFile):
	name = "sdl-mixer"
	version = "2.0.4"
	description = "SDL_mixer is a sample multi-channel audio mixer library"
	homepage = "https://www.libsdl.org/projects/SDL_mixer/"
	license = "Zlib https://www.libsdl.org/license.php"
	url="https://github.com/ianmurfinxyz/sdl-mixer-conan"
	settings = "os", "compiler", "arch", "build_type"
	options = {"shared": [True, False]}
	default_options = {"shared": False}
	generators = "cmake"
	exports_sources = ["CMakeLists.txt", "CMakeLists-sdl-mixer.txt"]
	zip_folder_name = f"SDL2_mixer-{version}"
	zip_name = f"{zip_folder_name}.tar.gz"
	build_subfolder = "build"
	source_subfolder = "source"
	user = "ianmurfinxyz"
	channel = "stable"

	def requirements(self):
		self.requires("sdl/2.0.20@ianmurfinxyz/stable")
		self.requires("vorbis/1.3.7")

	def source(self):
		tools.get(f"https://www.libsdl.org/projects/SDL_mixer/release/{self.zip_name}")
		os.rename(self.zip_folder_name, self.source_subfolder)
		shutil.move("CMakeLists-sdl-mixer.txt", os.path.join(self.source_subfolder, "CMakeLists.txt"))

	def build(self):
		cmake = CMake(self)
		cmake.configure(build_folder=self.build_subfolder)
		cmake.build()

	def package(self):
		self.copy("SDL_mixer.h", dst="include", src=self.source_subfolder)
		self.copy("*.lib", dst="lib", keep_path=False)
		self.copy("*.a", dst="lib", keep_path=False)
		self.copy("*.pdb", dst="lib", keep_path=False)
		self.copy("*.exp", dst="lib", keep_path=False)
		self.copy("*.dll", dst="bin",keep_path=False)
		self.copy("*.so", dst="bin", keep_path=False)
		self.copy("*.pdb", dst="bin", keep_path=False)

	def package_info(self):
		self.cpp_info.includedirs = ['include']
		
		build_type = self.settings.get_safe("build_type", default="Release")
		postfix = "d" if build_type == "Debug" else ""
		
		if self.settings.os == "Windows":
			static = "-static" if self.options.shared else ""
			self.cpp_info.libs = [
				f"SDL2_mixer{static}{postfix}.lib"
			]
		elif self.settings.os == "Linux":
			extension = "so" if self.options.shared else "a"
			self.cpp_info.libs = [
				f"SDL2_mixer{static}{postfix}.{extension}"
			]
		
		self.cpp_info.libdirs = ['lib']
		self.cpp_info.bindirs = ['bin']
