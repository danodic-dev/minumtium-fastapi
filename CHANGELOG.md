# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres
to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.1.0] - 2022-06-08

### Changed

- Changed the Dependency Injection system to allow for multiple application instances.
- Changed the way routes are created to allow for multiple route instances.
- Disabled the SQLite adapter in tests because using SQLite in memory is a nightmare.

## [1.0.1] - 2022-05-26

### Fixed

- Error in dependency injection was causing a null issue using the authentication adapter.

## [1.0.0] - 2022-04-14

### Added

- Added posts routes.
- Added users routes.
- Added auth routes.