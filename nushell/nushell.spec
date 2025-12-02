%global debug_package %{nil}

Name:    nushell
Version: 0.109.0
Release: %autorelease
Summary: A new type of shell
License: MIT
URL:     https://github.com/nushell/%{name}
Source:  %{url}/archive/refs/tags/%{version}.tar.gz

Provides: nu

BuildRequires: cargo
BuildRequires: rust
BuildRequires: libxcb
BuildRequires: openssl-devel
BuildRequires: libX11-devel

%description

%prep
%autosetup -n %{name}-%{version}

%build
export RUSTFLAGS="%{build_rustflags}"
cargo build --release --locked

# Generate license documentation
cargo tree --workspace --edges no-build,no-dev,no-proc-macro --no-dedupe --prefix none --format '{l}' | sort -u > LICENSE.summary
cargo tree --workspace --edges no-build,no-dev,no-proc-macro --no-dedupe --prefix none --format '{l}: {p}' | sort -u > LICENSE.dependencies

%install
install -Dpm 0755 target/release/nu -t %{buildroot}%{_bindir}/

%check
%{buildroot}%{_bindir}/nu --version

%files
%doc README.md
%license LICENSE LICENSE.summary LICENSE.dependencies
%{_bindir}/nu

%changelog
%autochangelog
