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
cargo build --release

%install
install -Dpm 0755 target/release/ya -t %{buildroot}%{_bindir}/
install -Dpm 0755 target/release/yazi -t %{buildroot}%{_bindir}/

%check
%{buildroot}%{_bindir}/ya   --version
%{buildroot}%{_bindir}/yazi --version

%files
%license LICENSE
%doc README.md
%{_bindir}/ya
%{_bindir}/yazi

%changelog
%autochangelog
