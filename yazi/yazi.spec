%global debug_package %{nil}

Name:    yazi
Version: 25.5.31
Release: %autorelease
Summary: Blazing Fast Terminal File Manager
License: MIT
URL:     https://github.com/sxyazi/%{name}
Source:  %{url}/archive/refs/tags/v%{version}.tar.gz

BuildRequires: cargo
BuildRequires: rust

Requires: file
Requires: jq
Requires: ffmpeg
Requires: fd-find
Requires: ripgrep
Requires: fzf

%description
Yazi is a blazing fast terminal file manager written in Rust.

%prep
%autosetup -n %{name}-%{version}

%build
export RUSTFLAGS="%{build_rustflags}"
cargo build --release --locked

# Generate license documentation
cargo tree --workspace --edges no-build,no-dev,no-proc-macro --no-dedupe --prefix none --format '{l}' | sort -u > LICENSE.summary
cargo tree --workspace --edges no-build,no-dev,no-proc-macro --no-dedupe --prefix none --format '{l}: {p}' | sort -u > LICENSE.dependencies

%install
install -Dpm 0755 target/release/ya -t %{buildroot}%{_bindir}/
install -Dpm 0755 target/release/yazi -t %{buildroot}%{_bindir}/

%check
%{buildroot}%{_bindir}/ya   --version
%{buildroot}%{_bindir}/yazi --version

%files
%doc README.md
%license LICENSE LICENSE.summary LICENSE.dependencies
%{_bindir}/ya
%{_bindir}/yazi

%changelog
%autochangelog
