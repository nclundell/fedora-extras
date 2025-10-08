%global debug_package %{nil}

Name: bottom
Version: 0.11.2
Release: %autorelease
Summary: Yet another cross-platform graphical process/system monitor

License: MIT
URL: https://github.com/ClementTsang/bottom
Source0: %{url}/archive/%{version}/%{name}-%{version}.tar.gz
Source1: %{url}/releases/download/%{version}/completion.tar.gz

BuildRequires: cargo
BuildRequires: rust

%description
A cross-platform graphical process/system monitor with a customizable
interface and a multitude of features. Supports Linux, macOS, and Windows.
Inspired by both gtop and gotop.

%prep
%setup -q
%setup -qDT -a1

%build
export RUSTFLAGS="%{build_rustflags}"
cargo build --release --locked

# Generate license documentation
cargo tree --workspace --edges no-build,no-dev,no-proc-macro --no-dedupe --prefix none --format '{l}' | sort -u > LICENSE.summary
cargo tree --workspace --edges no-build,no-dev,no-proc-macro --no-dedupe --prefix none --format '{l}: {p}' | sort -u > LICENSE.dependencies

%install
install -Dpm 0755 target/release/btm -t %{buildroot}%{_bindir}/

# Completions
install -Dpm 0644 btm.bash %{buildroot}%{_datadir}/bash-completion/completions/btm
install -Dpm 0644 btm.fish %{buildroot}%{_datadir}/fish/vendor_completions.d/btm.fish
install -Dpm 0644 btm.nu   %{buildroot}%{_datadir}/nushell/completions/btm.nu
install -Dpm 0644 _btm     %{buildroot}%{_datadir}/zsh/site-functions/_btm

%check
%{buildroot}%{_bindir}/btm --version

%files
%doc README.md CHANGELOG.md CONTRIBUTING.md sample_configs/
%license LICENSE LICENSE.summary LICENSE.dependencies
%{_bindir}/btm
%{_datadir}/bash-completion/completions/btm
%{_datadir}/fish/vendor_completions.d/btm.fish
%{_datadir}/nushell/completions/btm.nu
%{_datadir}/zsh/site-functions/_btm
