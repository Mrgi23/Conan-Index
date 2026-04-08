# Conan Index

A private Conan index for hosting custom, experimental, or packages not available in public remotes.
This repository acts as a centralized location for recipes and prebuilt binaries used across multiple projects.

## Structure

- `recipes/<pkg>/conanfile.py`
  Package recipes stored in a simple, predictable layout.

- `profiles/`
  Conan profiles for different build/host configurations.

- `.github/workflows/`
  CI pipelines responsible for building packages and uploading binaries to the configured Conan remote.

## Purpose

This repository provides:

- A private, controlled Conan index for internal packages.
- A place to maintain custom or patched recipes not available in public remotes.
- Automated CI workflows for building and publishing binaries.
- Reproducible builds across different platforms and configurations.
- A unified remote for distributing packages across multiple projects.

## Notes

- Recipes are stored in a format compatible with Conan 2.
- CI workflows can be extended to support additional architectures, compilers, or build configurations.
- This index is intended for private use and can be connected to any Conan remote (GitHub Packages, Artifactory, etc.).
