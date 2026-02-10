%global debug_package %{nil}

Name:    starship
Version: 1.24.2
Release: %autorelease
Summary: The minimal, blazing-fast, and infinitely customizable prompt for any shell!
License: ISC
URL:     https://github.com/starship/%{name}
Source:  %{url}/archive/refs/tags/v%{version}.tar.gz

BuildRequires: cargo
BuildRequires: rust

%description
Starship is a minimal, blazing-fast, and infinitely customizable prompt for any shell!

%prep
%autosetup -n %{name}-%{version}

%build
export RUSTFLAGS="%{build_rustflags}"
cargo build --release --locked

# Generate license documentation
cargo tree --workspace --edges no-build,no-dev,no-proc-macro --no-dedupe --prefix none --format '{l}' | sort -u > LICENSE.summary
cargo tree --workspace --edges no-build,no-dev,no-proc-macro --no-dedupe --prefix none --format '{l}: {p}' | sort -u > LICENSE.dependencies

%install
install -Dpm 0755 target/release/starship -t %{buildroot}%{_bindir}/

%check
%{buildroot}%{_bindir}/starship --version

%files
%doc README.md
%license LICENSE LICENSE.summary LICENSE.dependencies
%{_bindir}/starship

%changelog
%autochangelog
