%undefine _debugsource_packages
%define module ruff
%define oname ruff

# NOTE	Run create_vendored_crate_archive.sh script to create vendor archive-
# NOTE	when you update this package, submit archive to to abf and update-
# NOTE	Source1 & yml.

Name:		python-ruff
Version:	0.11.3
Release:	1
Summary:	An extremely fast Python linter and code formatter, written in Rust
URL:		https://pypi.org/project/ruff/
License:	MIT
Group:		Development/Python
Source0:	https://files.pythonhosted.org/packages/source/r/ruff/%{oname}-%{version}.tar.gz
Source1:	ruff-0.11.3-vendor.tar.xz
BuildSystem:	python

BuildRequires:	python
BuildRequires:	pkgconfig(python3)
BuildRequires:	python%{pyver}dist(pip)
BuildRequires:	python%{pyver}dist(maturin)
BuildRequires:	python%{pyver}dist(wheel)
BuildRequires:	cargo
BuildRequires:	rust-packaging

%description
An extremely fast Python linter and code formatter, written in Rust.

Ruff aims to be orders of magnitude faster than alternative tools while
integrating more functionality behind a single, common interface.


%prep
%autosetup -n %{module}-%{version} -p1 -a1
%cargo_prep -v vendor

cat >>.cargo/config <<EOF
[source.crates-io]
replace-with = "vendored-sources"

[source."git+https://github.com/astral-sh/lsp-types.git?rev=3512a9f"]
git = "https://github.com/astral-sh/lsp-types.git"
rev = "3512a9f"
replace-with = "vendored-sources"

[source."git+https://github.com/salsa-rs/salsa.git?rev=d758691ba17ee1a60c5356ea90888d529e1782ad"]
git = "https://github.com/salsa-rs/salsa.git"
rev = "d758691ba17ee1a60c5356ea90888d529e1782ad"
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "vendor"

EOF

%build
%py_build

%install
%py3_install

%files
%{_bindir}/%{module}
%{python3_sitearch}/%{module}
%{python3_sitearch}/%{module}-%{version}.dist-info
%license LICENSE
