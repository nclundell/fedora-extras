%global debug_package %{nil}

Name:    csvlens
Version: 0.15.1
Release: %autorelease
Summary: Command-line CSV viewer
License: MIT
URL:     https://github.com/YS-L/%{name}
Source:  %{url}/archive/refs/tags/v%{version}.tar.gz

BuildRequires: cargo
BuildRequires: rust

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
install -Dpm 0755 target/release/csvlens -t %{buildroot}%{_bindir}/

%check
%{buildroot}%{_bindir}/csvlens --version

%files
%doc README.md
%license LICENSE LICENSE.summary LICENSE.dependencies
%{_bindir}/csvlens

%changelog
%autochangelog
