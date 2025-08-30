%global debug_package %{nil}

Name:    bluetui
Version: 0.6
Release: %autorelease
Summary: TUI for managing bluetooth on Linux
License: GPL-3.0-or-later
URL:     https://github.com/pythops/%{name}
Source:  %{url}/archive/refs/tags/v%{version}.tar.gz

BuildRequires: cargo
BuildRequires: rust
BuildRequires: dbus-devel
BuildRequires: pkgconf-pkg-config

%description
TUI for managing bluetooth on Linux

%prep
%autosetup -n %{name}-%{version}

%build
export RUSTFLAGS="%{build_rustflags}"
cargo build --release --locked

# Generate license documentation
cargo tree --workspace --edges no-build,no-dev,no-proc-macro --no-dedupe --prefix none --format '{l}' | sort -u > LICENSE.summary
cargo tree --workspace --edges no-build,no-dev,no-proc-macro --no-dedupe --prefix none --format '{l}: {p}' | sort -u > LICENSE.dependencies

%install
install -Dpm 0755 target/release/bluetui -t %{buildroot}%{_bindir}/

%check
%{buildroot}%{_bindir}/bluetui --version

%files
%doc Readme.md
%license LICENSE LICENSE.summary LICENSE.dependencies
%{_bindir}/bluetui

%changelog
%autochangelog
