%global debug_package %{nil}

Name:    starship
Version: 1.23.0
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
cargo build --release --lock

%install
install -Dpm 0755 target/release/starship -t %{buildroot}%{_bindir}/

%check
%{buildroot}%{_bindir}/starship --version

%files
%license LICENSE
%doc README.md
%{_bindir}/starship

%changelog
%autochangelog
