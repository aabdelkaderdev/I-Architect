## ADDED Requirements

### Requirement: os-architecture-detection
The system must be able to detect the host OS and architecture to resolve the correct `planturl` binary path.

#### Scenario: Windows
- **WHEN** the OS is detected as Windows (any architecture)
- **THEN** it resolves the path to `tools/planturl/Bin/windows-msvc/planturl.exe`

#### Scenario: macOS ARM64
- **WHEN** the OS is macOS and architecture is ARM64
- **THEN** it resolves the path to `tools/planturl/Bin/aarch64-apple-darwin/planturl`

#### Scenario: macOS x86_64
- **WHEN** the OS is macOS and architecture is x86_64
- **THEN** it resolves the path to `tools/planturl/Bin/apple-darwin/planturl`

#### Scenario: Linux glibc
- **WHEN** the OS is Linux and the libc is glibc
- **THEN** it resolves the path to `tools/planturl/Bin/linux-gnu/planturl`

#### Scenario: Linux musl
- **WHEN** the OS is Linux and the libc is musl
- **THEN** it resolves the path to `tools/planturl/Bin/linux-musl/planturl`
