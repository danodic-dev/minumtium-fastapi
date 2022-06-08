## minumtium-fastapi 1.1.0

### Changed

- Changed the Dependency Injection system to allow for multiple application instances.
- Changed the way routes are created to allow for multiple route instances.
- Disabled the SQLite adapter in tests because using SQLite in memory is a nightmare.