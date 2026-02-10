%global debug_package %{nil}
%global crate resvg

Name:     resvg
Version: 0.47.0
Release:  %autorelease
Summary:  SVG rendering library
License:  Apache-2.0 OR MIT
URL:      https://github.com/linebender/resvg
Source:   %{url}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  cargo
buildRequires:  rust

%description
An SVG rendering library.

%prep
%autosetup -n %{crate}-%{version}

%build
export RUSTFLAGS="%{build_rustflags}"
cargo build --release --locked

# Generate license documentation
cargo tree --workspace --edges no-build,no-dev,no-proc-macro --no-dedupe --prefix none --format '{l}' | sort -u > LICENSE.summary
cargo tree --workspace --edges no-build,no-dev,no-proc-macro --no-dedupe --prefix none --format '{l}: {p}' | sort -u > LICENSE.dependencies

%install
install -Dpm 0755 target/release/resvg -t %{buildroot}%{_bindir}/

%check
%{buildroot}%{_bindir}/resvg --version

%files -n %{crate}
%license LICENSE-APACHE
%license LICENSE-MIT
%license LICENSE.dependencies
%license LICENSE.summary
%doc README.md
%{_bindir}/resvg

%changelog
%autochangelog
