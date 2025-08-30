%global debug_package %{nil}

Name:     topgrade
Version:  16.0.4
Release:  %autorelease
Summary:  Upgrade all the things

License:  GPL-3.0-or-later
URL:      https://github.com/topgrade-rs/topgrade
Source:   https://github.com/topgrade-rs/topgrade/archive/refs/tags/v%{version}.tar.gz

BuildRequires:   rust
BuildRequires:   cargo

%description
Topgrade is a tool that keeps your system up to date 
by invoking multiple package managers. 
It detects which tools you use and runs the appropriate 
commands to update them.

%prep
%autosetup

%build
cargo build --release --locked

# Generate license documentation
cargo tree --workspace --edges no-build,no-dev,no-proc-macro --no-dedupe --prefix none --format '{l}' | sort -u > LICENSE.summary
cargo tree --workspace --edges no-build,no-dev,no-proc-macro --no-dedupe --prefix none --format '{l}: {p}' | sort -u > LICENSE.dependencies

%install
install -Dm755 target/release/topgrade %{buildroot}/usr/bin/topgrade

%check
%{buildroot}%{_bindir}/topgrade --version

%files
%doc README.md
%license LICENSE LICENSE.summary LICENSE.dependencies
%{_bindir}/topgrade

%changelog
%autochangelog
